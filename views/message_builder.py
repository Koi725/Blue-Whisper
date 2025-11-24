# views/message_builder.py
"""
View layer responsible for constructing formatted bot messages.
Implements builder pattern for complex message composition.
"""

from typing import List
from config.settings import AppConfig, ServicePrice, ContactInfo
from services.localization_service import LocalizationService, Language


class MessageBuilder:
    """
    Constructs formatted messages for bot responses.
    Separates presentation logic from business logic.
    """

    def __init__(self, localization_service: LocalizationService):
        self._localization = localization_service
        self._config = AppConfig()

    def build_welcome_message(self) -> str:
        """
        Construct welcome message with branding.

        Returns:
            Formatted welcome message string
        """
        welcome = self._localization.get_text("welcome")
        subtitle = self._localization.get_text("welcome_subtitle")
        message = self._localization.get_text("welcome_message")

        return f"""
{welcome}

{subtitle}

{message}

{'=' * 50}
"""

    def build_language_selection(self) -> str:
        """
        Construct language selection menu.

        Returns:
            Formatted language selection message
        """
        prompt = self._localization.get_text("language_prompt")

        return f"""
{prompt}

1️⃣ English
2️⃣ العربية (Arabic)

{'=' * 50}
"""

    def build_main_menu(self) -> str:
        """
        Construct main menu with navigation options.

        Returns:
            Formatted main menu message
        """
        title = self._localization.get_text("main_menu")
        services = self._localization.get_text("services_menu")
        reservation = self._localization.get_text("reservation")
        social = self._localization.get_text("social_media")
        select = self._localization.get_text("select_option")

        return f"""
{title}

1️⃣ {services}
2️⃣ {reservation}
3️⃣ {social}

{select}
{'=' * 50}
"""

    def build_services_menu(self, services: List[ServicePrice]) -> str:
        """
        Construct services listing with prices.

        Args:
            services: List of available services

        Returns:
            Formatted services menu message
        """
        title = self._localization.get_text("services_menu")
        duration_label = self._localization.get_text("service_duration")
        back = self._localization.get_text("back")

        lang = self._localization.get_current_language()

        message = f"\n{title}\n\n"

        for idx, service in enumerate(services, 1):
            name = service.name_ar if lang == Language.ARABIC else service.name_en
            price = self._localization.format_price(service.price, service.currency)

            message += f"{idx}️⃣ {name}\n"
            message += f"   💰 {price}\n"
            message += f"   ⏱️ {duration_label}: {service.duration}\n\n"

        message += f"\n0️⃣ {back}\n"
        message += "=" * 50

        return message

    def build_reservation_message(self, whatsapp: str) -> str:
        """
        Construct reservation instructions with contact info.

        Args:
            whatsapp: WhatsApp contact number

        Returns:
            Formatted reservation message
        """
        contact_text = self._localization.get_text("contact_whatsapp")
        back = self._localization.get_text("back")

        whatsapp_link = f"https://wa.me/{whatsapp.replace('+', '').replace('-', '')}"

        return f"""
{contact_text}

📱 {whatsapp}

🔗 Click here: {whatsapp_link}

0️⃣ {back}
{'=' * 50}
"""

    def build_social_media_message(self, contact: ContactInfo) -> str:
        """
        Construct social media links message.

        Args:
            contact: Contact information object

        Returns:
            Formatted social media message
        """
        title = self._localization.get_text("social_media_title")
        subtitle = self._localization.get_text("social_media_subtitle")
        back = self._localization.get_text("back")

        return f"""
{title}

{subtitle}

📘 Facebook: {contact.facebook}

📸 Instagram: {contact.instagram}

🐦 Twitter: {contact.twitter}

✉️ Email: {contact.email}

0️⃣ {back}
{'=' * 50}
"""

    def build_thank_you_message(self) -> str:
        """
        Construct closing thank you message.

        Returns:
            Formatted thank you message
        """
        thank_you = self._localization.get_text("thank_you")
        see_you = self._localization.get_text("see_you")

        return f"""
{thank_you}
{see_you}

{'=' * 50}
"""

    def build_invalid_option_message(self) -> str:
        """
        Construct error message for invalid input.

        Returns:
            Formatted error message
        """
        return self._localization.get_text("invalid_option")
