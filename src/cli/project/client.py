import json
import config.config as config
import asyncio

from config.console import console


# TODO: Tests
class Client:
    async def _deploy_to_service(self, payload: bytes, signature: bytes):
        """
        Deploy the given payload and signature to the service.
        The client will connect to the service, send the deployment record, and print the response from the service.

        :param self: Instance of Client
        :param payload: The deployment record payload in bytes
        :type payload: bytes
        :param signature: The signature of the deployment record in bytes
        :type signature: bytes
        """
        console.print(f"Deploying to the service {config.SERVICE_ADDRESS}...")
        host, port = config.SERVICE_ADDRESS.split(":")
        reader, writer = await asyncio.open_connection(host, int(port))
        await self._send_record(writer, payload, signature)
        data = await reader.readline()
        msg = json.loads(data.decode())

        if msg["status"] == "success":
            console.print("Deployment record added successfully to the service.")
        else:
            console.print(
                "Failed to add the deployment record to the service.",
                style="bold red",
            )

        writer.close()

    async def _send_record(
        self, writer: asyncio.StreamWriter, payload: bytes, signature: bytes
    ):
        """
        Send the deployment record to the service in the expected JSON format.
        The message is sent as a single line with a newline character at the end to signal the end of the message.

        :param self: Instance of Client
        :param writer: The StreamWriter object to send data to the service
        :type writer: asyncio.StreamWriter
        :param payload: The deployment record payload in bytes
        :type payload: bytes
        :param signature: The signature of the deployment record in bytes
        :type signature: bytes
        """
        writer.write(
            (
                json.dumps(
                    {
                        "type": "add_deployment_record",
                        "record": payload.hex(),
                        "signature": signature.hex(),
                    }
                )
                + "\n"  # Note: the newline is important to signal the end of the message for readline()
            ).encode()
        )

        await writer.drain()
