# services/localization_service.py
"""
Localization service for multi-language support.
Implements strategy pattern for language-specific content delivery.
"""

from typing import Dict
from config.settings import Language


class LocalizationService:
    """
    Manages application translations and localized content.
    Provides interface for retrieving language-specific strings.
    """

    def __init__(self):
        self._translations = self._load_translations()
        self._current_language = Language.ENGLISH

    def _load_translations(self) -> Dict[Language, Dict[str, str]]:
        """Load translation dictionaries for supported languages."""
        return {
            Language.ENGLISH: {
                "welcome": "🌊 Welcome to Blue Whisper Ocean Club! 🌊",
                "welcome_subtitle": "Your Premium Ocean Adventure Destination in Oman Muscat",
                "welcome_message": "Experience the thrill of the ocean with our world-class water sports and activities.",
                "language_prompt": "Please select your preferred language:",
                "main_menu": "🏖️ Main Menu",
                "services_menu": "🎯 Our Services & Pricing",
                "reservation": "📞 Make a Reservation",
                "social_media": "📱 Follow Us on Social Media",
                "back": "⬅️ Back to Main Menu",
                "contact_whatsapp": "📞 Contact us on WhatsApp to book:",
                "service_duration": "Duration",
                "thank_you": "Thank you for choosing Blue Whisper Ocean Club!",
                "see_you": "We look forward to seeing you soon! 🌊",
                "select_option": "Please select an option:",
                "invalid_option": "❌ Invalid option. Please try again.",
                "social_media_title": "📱 Connect With Us",
                "social_media_subtitle": "Follow us for updates, special offers, and amazing ocean moments!",
            },
            Language.ARABIC: {
                "welcome": "🌊 مرحباً بكم في نادي بلو ويسبر البحري! 🌊",
                "welcome_subtitle": "وجهتكم المميزة للمغامرات البحرية في عمان",
                "welcome_message": "استمتع بإثارة المحيط مع أنشطتنا ورياضاتنا المائية ذات المستوى العالمي.",
                "language_prompt": "الرجاء اختيار لغتك المفضلة:",
                "main_menu": "🏖️ القائمة الرئيسية",
                "services_menu": "🎯 خدماتنا وأسعارنا",
                "reservation": "📞 حجز موعد",
                "social_media": "📱 تابعنا على وسائل التواصل",
                "back": "⬅️ العودة للقائمة الرئيسية",
                "contact_whatsapp": "📞 اتصل بنا على واتساب للحجز:",
                "service_duration": "المدة",
                "thank_you": "شكراً لاختياركم نادي بلو ويسبر البحري!",
                "see_you": "نتطلع لرؤيتكم قريباً! 🌊",
                "select_option": "الرجاء اختيار خيار:",
                "invalid_option": "❌ خيار غير صحيح. حاول مرة أخرى.",
                "social_media_title": "📱 تواصل معنا",
                "social_media_subtitle": "تابعنا للحصول على التحديثات والعروض الخاصة ولحظات بحرية مذهلة!",
            },
        }

    def set_language(self, language: Language) -> None:
        """Set current application language."""
        self._current_language = language

    def get_current_language(self) -> Language:
        """Retrieve current language setting."""
        return self._current_language

    def get_text(self, key: str) -> str:
        """
        Retrieve localized text for given key.

        Args:
            key: Translation key identifier

        Returns:
            Localized string in current language
        """
        return self._translations.get(
            self._current_language, self._translations[Language.ENGLISH]
        ).get(key, key)

    def format_price(self, amount: float, currency: str) -> str:
        """Format price according to current locale."""
        if self._current_language == Language.ARABIC:
            return f"{amount:.2f} {currency}"
        return f"{currency} {amount:.2f}"
