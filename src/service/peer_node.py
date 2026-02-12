import asyncio
import json

from asyncio import StreamReader, StreamWriter
from datetime import datetime
from block import Block
from blockchain import Blockchain


# TODO: Tests
# TODO: Remove all prints and replace with proper logging. This is just for quick debugging and demonstration purposes.
class PeerNode:
    host: str
    port: int
    peers: set[str]  # unique set of known peer addresses
    connected_peers: set[str]  # peers we have already contacted
    log_file: str  # TODO: Remove when we have proper logging
    blockchain: Blockchain

    mempool: list[
        tuple[bytes, bytes]
    ]  # List of (payload, signature) tuples representing deployment records to be processed

    def __init__(self, host: str, port: int, bootstrap: str = None):
        """
        Initialize the PeerNode with the given host, port, and optional bootstrap peer.

        :param self: Instance of PeerNode
        :param host: Host address of the peer node
        :type host: str
        :param port: Port number of the peer node
        :type port: int
        :param bootstrap: Optional bootstrap peer address to connect to when starting the node
        :type bootstrap: str
        """
        self.host = host
        self.port = int(port)
        self.peers = set()  # unique set of peer addresses
        self.connected_peers = set()  # peers we have already contacted
        self.mempool = []
        # self.blockchain = Blockchain()

        self.log_file = (
            f"peer_communication.log"  # TODO: Remove when we have proper logging
        )

        if bootstrap:
            self.peers.add(bootstrap)
            print(f"Bootstrapping to {bootstrap}...")

    async def start(self):
        """
        Start the peer node and listen for incoming connections. The node will handle incoming messages.

        :param self: Instance of PeerNode
        """
        print(f"Starting peer node on {self.host}:{self.port}...")
        server = await asyncio.start_server(self.handle_client, self.host, self.port)

        async with server:
            await server.serve_forever()

    async def handle_client(self, reader: StreamReader, writer: StreamWriter):
        """
        Handles an incoming client connection. The node will read a message from the client, process it, and respond accordingly.
        :param self: Instance of PeerNode
        :param reader: StreamReader object to read data from the client
        :type reader: StreamReader
        :param writer: StreamWriter object to send data to the client
        :type writer: StreamWriter
        """
        data = await reader.readline()
        msg = json.loads(data.decode())

        if msg["type"] == "hello":
            await self._handle_hello_message(msg, writer)

        if msg["type"] == "add_deployment_record":
            await self._handle_add_deployment_record(msg, writer)

        writer.close()

    async def _handle_hello_message(self, msg: dict, writer: StreamWriter):
        """
        Handle a "hello" message from a peer. The node will update its known peers, and respond with its own peer list.

        :param self: Instance of PeerNode
        :param msg: The "hello" message received from a peer, containing the sender's address and their known peers
        :type msg: dict
        :param writer: StreamWriter object to send data to the client
        :type writer: StreamWriter
        """
        print(f"Hi {msg['me']}. Nice to meet you. 👋")

        self._log_greeting(
            f"{self.host}:{self.port}",
            msg["me"],
            f"Hi {msg['me']}. Nice to meet you. 👋",
        )

        peers_without_sender = [p for p in self.peers if p != msg["me"]]

        print(
            f"I know these peers: {peers_without_sender}"
            if peers_without_sender
            else "I don't know any peers yet."
        )

        self._update_own_peer_list(msg)

        await self._send_own_peer_list(
            writer, "peer_list", list(self.peers), f"{self.host}:{self.port}"
        )

        await self._broadcast_new_peer(msg)

    async def _handle_add_deployment_record(self, msg: dict, writer: StreamWriter):
        # TODO: The signature is not used for now. We should verify the signature and only add the record to the mempool if the signature is valid.
        self.mempool.append(
            (bytes.fromhex(msg["record"]), bytes.fromhex(msg["signature"]))
        )

        # TODO: The mempool is not used for reorgs right now.
        record = self.mempool[0]
        # TODO: Fix getting last block.
        # latest_block = self.blockchain.get_latest_block()
        # previous_hash = Block.calculate_hash(latest_block) if latest_block else None
        # print(previous_hash)
        # block = Block(record[0], record[1], previous_hash).build()
        block = Block(record[0], record[1]).build()
        print(block)
        # self.blockchain.add_block(block)
        self.mempool.pop(0)

        writer.write(
            (
                json.dumps(
                    {
                        "type": "add_deployment_record_response",
                        "status": "success",
                    }
                )
                + "\n"  # Note: the newline is important to signal the end of the message for readline()
            ).encode()
        )

        await writer.drain()

    def _update_own_peer_list(self, msg: dict):
        """
        Update the node's known peer list with the peers received in the "hello" message, excluding itself.

        :param self: Instance of PeerNode
        :param msg: The "hello" message received from a peer, containing the sender's address and their known peers
        :type msg: dict
        """
        self.peers.update(
            [peer for peer in msg["peers"] if peer != f"{self.host}:{self.port}"]
            + [msg["me"]]
        )  # We don't want to add ourselfs as a peer but we want to add the sender

    async def _send_own_peer_list(
        self, writer: StreamWriter, type: str, peers: list[str], me: str
    ):
        """
        Send the node's own peer list back to the sender of the "hello" message.

        :param self: Instance of PeerNode
        :param writer: StreamWriter object to send data to the client
        :type writer: StreamWriter
        :param type: The type of the message to send (e.g., "peer_list" or "hello")
        :type type: str
        :param peers: The list of known peers to include in the message
        :type peers: list[str]
        :param me: The address of the current node to include in the message
        :type me: str
        """
        writer.write(
            (
                json.dumps(
                    {
                        "type": type,
                        "peers": peers,
                        "me": me,
                    }
                )
                + "\n"  # Note: the newline is important to signal the end of the message for readline()
            ).encode()
        )

        await writer.drain()

    async def _broadcast_new_peer(self, msg: dict):
        """
        Broadcast the new peer to all known peers except the sender and already contacted peers.

        :param self: Instance of PeerNode
        :param msg: The "hello" message received from a peer, containing the sender's address and their known peers
        :type msg: dict
        """
        for peer in self.peers - {
            msg["me"]
        }:  # We don't want to contact the sender again. He already has received our peer list.
            if (
                peer not in self.connected_peers
            ):  # We don't contact peers we have already contacted. This prevents infinite loops of contacting the same peers again and again.
                await self.connect_to_peer(peer)

    async def connect_to_peer(self, peer: str):
        """
        Connect to a peer and exchange peer lists.

        :param self: Instance of PeerNode
        :param peer: The address of the peer to connect to
        :type peer: str
        """
        print(f"Hello {peer} 👋")
        self._log_greeting(f"{self.host}:{self.port}", peer, f"Hello {peer} 👋")

        peers_without_target_peer = [p for p in self.peers if p != peer]

        print(
            f"I also know these peers: {peers_without_target_peer}"
            if peers_without_target_peer
            else "I don't know any peers yet."
        )

        host, port = peer.split(":")
        reader, writer = await asyncio.open_connection(host, int(port))
        me = f"{self.host}:{self.port}"
        await self._send_own_peer_list(writer, "hello", peers_without_target_peer, me)
        data = await reader.readline()
        msg = json.loads(data.decode())
        old_peers = self.peers.copy()

        self.peers.update(
            p for p in msg["peers"] if p != me
        )  # We don't want to add ourselfs as a peer

        writer.close()
        self.connected_peers.add(peer)

        # Connect to newly discovered peers
        new_peers = self.peers - old_peers

        for new_peer in new_peers:
            if new_peer not in self.connected_peers:
                print(f"Hello {new_peer} 👋")
                await self.connect_to_peer(new_peer)

    def close(self):
        """Close resources like the LevelDB handle."""
        # self.blockchain.close()
        # TODO: Activate the code

    # TODO: Remove this logging method. It is only for demonstration purposes to show the greetings in the log files.
    def _log_greeting(self, sender: str, receiver: str, message: str):
        """Log all Hi and Hello messages to file"""
        with open(self.log_file, "a", encoding="utf-8") as f:
            timestamp = datetime.now().isoformat()
            f.write(f"[{timestamp}] {sender} --> {receiver}: {message}\n")
            # f.write(
            #    f"[{timestamp}] {sender.split(':')[1]}{'->>' if message.startswith('Hello') else '-->>'}{receiver.split(':')[1]}: {message}\n"
            # )
