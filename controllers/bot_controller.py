# controllers/bot_controller.py
"""Main bot controller implementing state machine pattern."""

from enum import Enum
from typing import Optional
from config.settings import AppConfig, Language
from services.localization_service import LocalizationService
from views.message_builder import MessageBuilder


class BotState(Enum):
    """Bot conversation state enumeration."""

    WELCOME = "welcome"
    LANGUAGE_SELECTION = "language_selection"
    MAIN_MENU = "main_menu"
    SERVICES = "services"
    RESERVATION = "reservation"
    SOCIAL_MEDIA = "social_media"
    EXIT = "exit"


class BotController:
    """
    Core bot controller managing conversation state and flow.
    Implements state machine pattern for robust navigation.
    """

    def __init__(self):
        self._config = AppConfig()
        self._localization = LocalizationService()
        self._message_builder = MessageBuilder(self._localization)
        self._current_state = BotState.WELCOME
        self._previous_state: Optional[BotState] = None

    def get_current_state(self) -> BotState:
        """Retrieve current conversation state."""
        return self._current_state

    def _transition_to(self, new_state: BotState) -> None:
        """
        Perform state transition with history tracking.

        Args:
            new_state: Target state to transition to
        """
        self._previous_state = self._current_state
        self._current_state = new_state

    def start(self) -> str:
        """
        Initialize bot conversation.

        Returns:
            Welcome message with language selection
        """
        self._transition_to(BotState.LANGUAGE_SELECTION)
        welcome = self._message_builder.build_welcome_message()
        language_menu = self._message_builder.build_language_selection()
        return welcome + language_menu

    def process_input(self, user_input: str) -> str:
        """
        Process user input based on current state.

        Args:
            user_input: User's text input

        Returns:
            Bot response message
        """
        user_input = user_input.strip()

        if self._current_state == BotState.LANGUAGE_SELECTION:
            return self._handle_language_selection(user_input)

        elif self._current_state == BotState.MAIN_MENU:
            return self._handle_main_menu(user_input)

        elif self._current_state == BotState.SERVICES:
            return self._handle_services_menu(user_input)

        elif self._current_state == BotState.RESERVATION:
            return self._handle_reservation(user_input)

        elif self._current_state == BotState.SOCIAL_MEDIA:
            return self._handle_social_media(user_input)

        return self._message_builder.build_invalid_option_message()

    def _handle_language_selection(self, user_input: str) -> str:
        """Handle language selection state."""
        if user_input == "1":
            self._localization.set_language(Language.ENGLISH)
            self._transition_to(BotState.MAIN_MENU)
            return self._message_builder.build_main_menu()

        elif user_input == "2":
            self._localization.set_language(Language.ARABIC)
            self._transition_to(BotState.MAIN_MENU)
            return self._message_builder.build_main_menu()

        return (
            self._message_builder.build_invalid_option_message()
            + "\n\n"
            + self._message_builder.build_language_selection()
        )

    def _handle_main_menu(self, user_input: str) -> str:
        """Handle main menu navigation state."""
        if user_input == "1":
            self._transition_to(BotState.SERVICES)
            services = self._config.get_services()
            return self._message_builder.build_services_menu(services)

        elif user_input == "2":
            self._transition_to(BotState.RESERVATION)
            contact = self._config.get_contact_info()
            return self._message_builder.build_reservation_message(contact.whatsapp)

        elif user_input == "3":
            self._transition_to(BotState.SOCIAL_MEDIA)
            contact = self._config.get_contact_info()
            return self._message_builder.build_social_media_message(contact)

        return (
            self._message_builder.build_invalid_option_message()
            + "\n\n"
            + self._message_builder.build_main_menu()
        )

    def _handle_services_menu(self, user_input: str) -> str:
        """Handle services menu state."""
        if user_input == "0":
            self._transition_to(BotState.MAIN_MENU)
            return self._message_builder.build_main_menu()

        services = self._config.get_services()
        if user_input.isdigit() and 1 <= int(user_input) <= len(services):
            # User selected a service, show reservation option
            self._transition_to(BotState.RESERVATION)
            contact = self._config.get_contact_info()
            return self._message_builder.build_reservation_message(contact.whatsapp)

        return (
            self._message_builder.build_invalid_option_message()
            + "\n\n"
            + self._message_builder.build_services_menu(services)
        )

    def _handle_reservation(self, user_input: str) -> str:
        """Handle reservation state."""
        if user_input == "0":
            self._transition_to(BotState.MAIN_MENU)
            return self._message_builder.build_main_menu()

        return (
            self._message_builder.build_invalid_option_message()
            + "\n\n"
            + self._message_builder.build_reservation_message(
                self._config.get_contact_info().whatsapp
            )
        )

    def _handle_social_media(self, user_input: str) -> str:
        """Handle social media display state."""
        if user_input == "0":
            self._transition_to(BotState.MAIN_MENU)
            return self._message_builder.build_main_menu()

        return (
            self._message_builder.build_invalid_option_message()
            + "\n\n"
            + self._message_builder.build_social_media_message(
                self._config.get_contact_info()
            )
        )
