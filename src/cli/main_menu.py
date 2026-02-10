import questionary


class CommandLine:
    EXIT_COMMAND = "EXIT"
    KEY_MANAGEMENT_COMMAND = "KEY_MANAGEMENT"
    CREATE_DEPLOYMENT_RECORD_COMMAND = "CREATE_DEPLOYMENT_RECORD"

    def show(self) -> str | None:
        """
        Displays the main menu and handles user input.

        Returns:
            str: The command selected by the user, or None if the user cancels.
        """
        choices = [
            questionary.Choice(
                "Key management",
                value=self.KEY_MANAGEMENT_COMMAND,
            ),
            questionary.Choice(
                "Create a deployment record",
                value=self.CREATE_DEPLOYMENT_RECORD_COMMAND,
            ),
            questionary.Choice(
                "Exit the application",
                value=self.EXIT_COMMAND,
            ),
        ]

        return questionary.select(
            "What do you want to do?", choices=choices, use_shortcuts=True
        ).ask()
