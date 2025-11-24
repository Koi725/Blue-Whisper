# main.py
"""
Application entry point for Blue Whisper Ocean Club Chatbot.
Initializes and launches the bot interface.
"""

import sys
from interfaces.console_interface import ConsoleInterface


def main() -> int:
    """
    Main application entry point.

    Returns:
        Exit status code (0 for success, 1 for error)
    """
    try:
        print("\n🚀 Starting Blue Whisper Ocean Club Bot...\n")

        # Initialize and run console interface
        interface = ConsoleInterface()
        interface.run()

        return 0

    except Exception as e:
        print(f"\n❌ Fatal error: {str(e)}")
        print("Please contact support if the problem persists.\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
