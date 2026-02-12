import asyncio
import questionary

from pathlib import Path
from address.address import Address
from address.custom_address import CustomAddress
from address.index import Index
from common.console import print_info
from project.client import Client
from project.deployment_record import DeploymentRecord
from project.merkle_root import MerkleRoot
from project.project import Project
from validation.validators import iso8601_str_is_valid, striped_str_is_not_empty
from datetime import datetime


class CommandLine:
    address_index: Index

    def __init__(self):
        """
        Initializes the CommandLine instance and loads the address index.

        :param self: Instance of CommandLine
        """
        self.address_index = Index()

    def show(self):
        """
        Displays a form to enter record data.

        :param self: Instance of CommandLine
        """
        address = self._select_key()

        if not address:
            return

        path = self._select_project_path()

        if not path:
            return

        metadata = self._get_metadata()

        if not metadata:
            return

        project = Project(path)
        merkle_root = MerkleRoot(project)

        if address:
            print_info(
                f"""Data of the deployment record:

{''.join(f'\t{key}: {value}\n' for key, value in metadata.items())}
                
\tAddress: {address.get_address()}
\tMerkle root: {merkle_root.get_merkle_root()}

\tFiles included in the Merkle tree:

{''.join(f'\t- {file}\n' for file in merkle_root.get_files())}"""
            )

        self._deploy(address, merkle_root, metadata)

    def _select_key(self) -> Address | None:
        """
        Prompt the user to select a key from the address index.

        :return: The selected Address instance or None if the user cancels the selection
        :rtype: Address | None
        """
        address_names = self.address_index.get_all()

        if not address_names:
            print_info("No addresses found. Please generate an address first.")
            return None

        choices = [questionary.Choice(name, value=name) for name in address_names] + [
            questionary.Choice(
                "Cancel", value="Cancel"
            )  # None does not work with questionary, so we use a specific value to represent cancellation
        ]

        selected_key = questionary.select(
            "Select a key:", choices=choices, use_shortcuts=True
        ).ask()

        if selected_key is None or selected_key == "Cancel":
            return None

        return CustomAddress.load(selected_key)

    def _select_project_path(self) -> Path | None:
        """
        Prompt the user to input the project directory path.

        :return: The path to the project directory
        :rtype: Path | None
        """
        directory_path = questionary.path(
            "What's the path to the project?", only_directories=True
        ).ask()

        if not directory_path:
            return None

        return Path(directory_path)

    def _get_metadata(self):
        """
        Prompt the user to input the metadata for the deployment record.

        :param self: Instance of CommandLine
        """
        return questionary.form(
            author=questionary.text(
                "Who is the author of the deployment?",
                validate=striped_str_is_not_empty,
            ),
            contact_info=questionary.text(
                "What is the contact information of the author?",
                validate=striped_str_is_not_empty,
            ),
            software_name=questionary.text(
                "What software do you deploy?", validate=striped_str_is_not_empty
            ),
            version=questionary.text(
                "What version do you deploy?", validate=striped_str_is_not_empty
            ),
            commit_hash=questionary.text(
                "What is the commit hash of the deployed code?",
                validate=striped_str_is_not_empty,
            ),
            repository_url=questionary.text(
                "What is the url to commit in the repository?",
                validate=striped_str_is_not_empty,
            ),
            timestamp=questionary.text(
                "What was the local time of the deployment? (ISO 8601 format: YYYY-MM-DDTHH:MM:SS)",
                validate=iso8601_str_is_valid,
                default=datetime.now().isoformat(timespec="seconds"),
            ),
        ).ask()

    # TODO: Test that the deployment record is created and signed correctly when the user confirms the deployment.
    def _deploy(self, address: Address, merkle_root: MerkleRoot, metadata: dict):
        """
        Prompt the user to confirm the deployment and create, sign, and send the deployment record to the service if confirmed.

        :param self: Instance of CommandLine
        :param address: The Address instance representing the address involved in the deployment
        :type address: Address
        :param merkle_root: The MerkleRoot instance representing the Merkle root of the deployed project
        :type merkle_root: MerkleRoot
        :param metadata: Dictionary containing metadata about the deployment
        :type metadata: dict
        """
        if questionary.confirm(
            "Do you want to create the deployment record, sign it and send it to the network?"
        ).ask():
            payload, signature = DeploymentRecord(
                address, merkle_root, metadata
            ).serialize()

            # TODO: Test that the payload and signature are sent to the service correctly.
            asyncio.run(Client()._deploy_to_service(payload, signature))
