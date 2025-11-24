# interfaces/console_interface.py
"""
Console-based user interface for bot interaction.
Provides terminal I/O handling with formatted output.
"""

import os
from typing import Optional
from controllers.bot_controller import BotController, BotState


class ConsoleInterface:
    """
    Terminal interface for bot interaction.
    Handles user input/output with proper formatting.
    """

    def __init__(self):
        self._controller = BotController()
        self._running = False

    @staticmethod
    def clear_screen() -> None:
        """Clear terminal screen for clean presentation."""
        os.system("cls" if os.name == "nt" else "clear")

    @staticmethod
    def print_separator() -> None:
        """Print visual separator line."""
        print("\n" + "=" * 50 + "\n")

    def display_message(self, message: str) -> None:
        """
        Display bot message with formatting.

        Args:
            message: Message text to display
        """
        self.clear_screen()
        print(message)

    def get_user_input(self) -> str:
        """
        Prompt and retrieve user input.

        Returns:
            User input string
        """
        return input("\n👉 Your choice: ").strip()

    def run(self) -> None:
        """
        Main interface loop.
        Manages conversation flow until exit.
        """
        self._running = True

        # Display welcome and language selection
        welcome_message = self._controller.start()
        self.display_message(welcome_message)

        while self._running:
            try:
                user_input = self.get_user_input()

                # Check for exit commands
                if user_input.lower() in ["exit", "quit", "q"]:
                    self._running = False
                    self.display_message(
                        "\n👋 Thank you for visiting Blue Whisper Ocean Club!\n"
                    )
                    break

                # Process input through controller
                response = self._controller.process_input(user_input)
                self.display_message(response)

            except KeyboardInterrupt:
                self._running = False
                self.display_message("\n\n👋 Goodbye! Come back soon!\n")
                break

            except Exception as e:
                print(f"\n❌ An error occurred: {str(e)}")
                print("Please try again.\n")
