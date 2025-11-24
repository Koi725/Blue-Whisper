# config/settings.py
"""
Application configuration management with environment-specific settings.
Implements singleton pattern for centralized configuration access.
"""

from dataclasses import dataclass
from typing import Dict, List
from enum import Enum


class Language(Enum):
    """Supported language enumeration."""

    ENGLISH = "en"
    ARABIC = "ar"


@dataclass
class ContactInfo:
    """Contact information data structure."""

    whatsapp: str
    facebook: str
    instagram: str
    twitter: str
    email: str


@dataclass
class ServicePrice:
    """Service pricing information structure."""

    name_en: str
    name_ar: str
    price: float
    currency: str
    duration: str


class AppConfig:
    """
    Application configuration singleton.
    Centralizes all application settings and constants.
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self) -> None:
        """Initialize configuration parameters."""
        self.default_language = Language.ENGLISH
        self.currency = "OMR"
        self.contact = ContactInfo(
            whatsapp="+968-9123-4567",
            facebook="https://facebook.com/bluewhisperoman",
            instagram="https://instagram.com/bluewhisperoman",
            twitter="https://twitter.com/bluewhisperoman",
            email="info@bluewhisper.om",
        )

        self.services = [
            ServicePrice("Jet Ski", "جت سكي", 25.0, self.currency, "30 minutes"),
            ServicePrice(
                "Parasailing", "الطيران الشراعي", 35.0, self.currency, "15 minutes"
            ),
            ServicePrice(
                "Banana Boat", "قارب الموز", 15.0, self.currency, "20 minutes"
            ),
            ServicePrice("Snorkeling", "الغوص بالأنبوب", 20.0, self.currency, "1 hour"),
            ServicePrice("Kayaking", "التجديف", 18.0, self.currency, "1 hour"),
            ServicePrice(
                "Diving Experience", "تجربة الغوص", 50.0, self.currency, "2 hours"
            ),
        ]

    def get_services(self) -> List[ServicePrice]:
        """Retrieve all available services."""
        return self.services

    def get_contact_info(self) -> ContactInfo:
        """Retrieve contact information."""
        return self.contact
