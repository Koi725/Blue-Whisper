# README.md

"""

# Blue Whisper Ocean Club - Intelligent Chatbot

## Overview

Enterprise-grade bilingual chatbot system for Blue Whisper Ocean Club in Oman.
Provides interactive service discovery, pricing information, and reservation management.

## Features

- 🌐 Bilingual Support (English & Arabic)
- 💰 Real-time Pricing Information
- 🏖️ Complete Service Catalog
- 📞 WhatsApp Integration
- 📱 Social Media Links
- 🎯 State Machine Architecture

## Architecture

```
project/
├── config/
│   └── settings.py          # Application configuration & constants
├── services/
│   └── localization_service.py  # Multi-language support
├── views/
│   └── message_builder.py   # Message formatting layer
├── controllers/
│   └── bot_controller.py    # Core business logic & state management
├── interfaces/
│   └── console_interface.py # User interface layer
└── main.py                  # Application entry point
```

## Design Patterns

- **Singleton Pattern**: Configuration management
- **Builder Pattern**: Complex message construction
- **State Machine Pattern**: Conversation flow management
- **Strategy Pattern**: Language-specific content delivery
- **MVC Pattern**: Separation of concerns

## Installation

```bash
# Clone repository
git clone https://github.com/yourusername/blue-whisper-bot.git

# Navigate to project directory
cd blue-whisper-bot

# No external dependencies required (uses Python stdlib only)
```

## Usage

```bash
# Run the chatbot
python main.py
```

## Configuration

Edit `config/settings.py` to customize:

- Contact information
- Service offerings and prices
- Default language settings
- Currency and pricing format

## Services Offered

1. Jet Ski - OMR 25.00 (30 minutes)
2. Parasailing - OMR 35.00 (15 minutes)
3. Banana Boat - OMR 15.00 (20 minutes)
4. Snorkeling - OMR 20.00 (1 hour)
5. Kayaking - OMR 18.00 (1 hour)
6. Diving Experience - OMR 50.00 (2 hours)

## Requirements

- Python 3.8+
- No external dependencies

## Code Quality Standards

- ✅ OOP Principles
- ✅ SOLID Principles
- ✅ Type Hints
- ✅ Comprehensive Documentation
- ✅ Clean Architecture
- ✅ Design Patterns

## License

Proprietary - Blue Whisper Ocean Club © 2024

## Contact

- WhatsApp: +968-9123-4567
- Email: info@bluewhisper.om
- Website: www.bluewhisper.om
  """
