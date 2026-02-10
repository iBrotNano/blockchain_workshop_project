import sys

from config import config
from config.console import console
from address.custom_address import CustomAddress as CustomAddress
from address.solana_address import SolanaAddress as SolanaAddress
from main_menu import CommandLine as menu
from address.command_line import CommandLine as address_cli


def show_main_menu():
    """
    Displays the main menu and handles user input.
    """
    try:
        command = main_menu.show()

        if command == main_menu.KEY_MANAGEMENT_COMMAND:
            address_cli().show()

        if command == main_menu.EXIT_COMMAND or command is None:
            console.print("Goodbye! 👋")
            exit(0)

    except Exception as e:
        print(e)
        # log.exception(f"An error of type {type(e)} occurred. Message: {e}")


try:
    config.configure()
    console.print("Welcome to the Plockchain CLI!")
    console.rule()
    main_menu = menu()

    while True:
        show_main_menu()
# Catch any unexpected errors at the top level during app initialization.
except Exception as e:
    # log.critical(f"An error of type {type(e)} occurred. Message: {e}", exc_info=True)
    exit(1)
