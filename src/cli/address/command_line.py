import questionary

from address.custom_address import CustomAddress
from address.index import Index
from config.console import console
from common.console import print_rule_separated, print_info
from validation.validators import striped_str_is_not_empty


class CommandLine:
    EXIT_COMMAND = "EXIT"
    GENERATE_COMMAND = "GENERATE"

    address_index: Index

    def __init__(self):
        """
        Initializes the CommandLine instance and loads the address index.

        :param self: Instance of CommandLine
        """
        self.address_index = Index()

    def show(self) -> None:
        """
        Displays the key management menu and handles user interactions for generating new addresses or exiting the menu.

        :param self: Instance of CommandLine
        :return: None
        """
        console.print("Key Management:")
        console.rule()

        while True:
            command = self._show_key_management_menu()

            if command == self.GENERATE_COMMAND:
                self._generate_address()

            if command == self.EXIT_COMMAND or command is None:
                return

    def _show_key_management_menu(self) -> str | None:
        """
        Displays the key management menu and prompts the user to select an action.

        :param self: Instance of CommandLine
        :return: The selected command or None if the user cancels the selection
        """
        choices = [
            questionary.Choice(
                "Generate a new address",
                value=self.GENERATE_COMMAND,
            ),
            questionary.Choice(
                "Exit key management",
                value=self.EXIT_COMMAND,
            ),
        ]

        return questionary.select(
            "What do you want to do?", choices=choices, use_shortcuts=True
        ).ask()

    def _enter_key_name(self) -> str | None:
        """
        Prompts the user to enter the name of the key.

        :param self: Instance of CommandLine
        :return: The entered key name or None if the user cancels the input
        """
        return questionary.text(
            "Enter the name of the key:",
            validate=self._is_key_name_valid,
        ).ask()

    def _is_key_name_valid(self, text: str) -> bool:
        """Validates the entered key name to ensure it is not empty and does not already exist in the address index.
        :param self: Instance of CommandLine
        :param text: The entered key name to validate
        :return: True if the key name is valid, False otherwise
        """
        return (
            striped_str_is_not_empty(text) and text not in self.address_index.get_all()
        )

    def _generate_address(self) -> None:
        """Generates a new address by prompting the user for a key name, creating a CustomAddress instance,
        and saving it if the user confirms.

        :param self: Instance of CommandLine
        :return: None
        """
        key_name = self._enter_key_name()

        if key_name is None:
            return

        address = CustomAddress(key_name, CustomAddress.generate_mnemonic())

        if not self._confirm_save():
            return

        if address.try_save():
            self.address_index.add_to_index(key_name)

            print_rule_separated("Address generated and saved successfully.")

            print_info(
                f"Please note your address to identify your deployments records later and keep your mnemonic safe. It is required to recover your address.\n\n\tAddress: {address.get_address()}\n\n\tMnemonic: {address.get_mnemonic()}",
                "Important information:",
            )
        else:
            raise RuntimeError("Failed to save the address. Please try again.")

    def _confirm_save(self) -> bool:
        """Prompts the user to confirm whether they want to generate and save the address.

        :param self: Instance of CommandLine
        :return: True if the user confirms, False otherwise
        """
        return questionary.confirm(
            "Do you want to generate and save the address?", default=True
        ).ask()
