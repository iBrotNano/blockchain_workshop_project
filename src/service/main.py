import asyncio
import traceback
import argparse

from peer_node import PeerNode

# TODO: Tests
try:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--host", help="Host address of the peer node", default="127.0.0.1"
    )

    parser.add_argument(
        "--port", type=int, help="Port number of the peer node", default=5000
    )

    parser.add_argument("--bootstrap", help="Bootstrap peer in the format host:port")

    args = parser.parse_args()

    if args.bootstrap:
        peer = PeerNode(args.host, args.port, args.bootstrap)
        # TODO: Should connect and exchange peer lists now and then, not just at startup.
        asyncio.run(peer.connect_to_peer(args.bootstrap))
    else:
        peer = PeerNode(args.host, args.port)

    asyncio.run(peer.start())
except KeyboardInterrupt:
    print("Shutting down...")
    exit(0)
except:
    traceback.print_exc()
