# adapters/telegram_adapter.py
"""
Telegram bot adapter implementing platform-specific integration.
Bridges Telegram API with core bot controller logic.
"""

from typing import Optional
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from controllers.bot_controller import BotController, BotState
from config.settings import Language


class TelegramBotAdapter:
    """
    Telegram platform adapter for bot controller.
    Handles Telegram-specific message formatting and user interaction.
    """

    def __init__(self, token: str):
        """
        Initialize Telegram adapter.

        Args:
            token: Telegram Bot API token
        """
        self._token = token
        self._application: Optional[Application] = None
        self._user_controllers = {}  # Store controller per user

    def _get_or_create_controller(self, user_id: int) -> BotController:
        """
        Retrieve or create bot controller for specific user.
        Maintains separate conversation state per user.

        Args:
            user_id: Telegram user identifier

        Returns:
            BotController instance for user
        """
        if user_id not in self._user_controllers:
            self._user_controllers[user_id] = BotController()
        return self._user_controllers[user_id]

    def _create_language_keyboard(self) -> InlineKeyboardMarkup:
        """
        Create inline keyboard for language selection.

        Returns:
            Telegram inline keyboard markup
        """
        keyboard = [
            [
                InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"),
                InlineKeyboardButton("🇴🇲 العربية", callback_data="lang_ar"),
            ]
        ]
        return InlineKeyboardMarkup(keyboard)

    def _create_main_menu_keyboard(
        self, controller: BotController
    ) -> InlineKeyboardMarkup:
        """
        Create inline keyboard for main menu navigation.

        Args:
            controller: Bot controller instance

        Returns:
            Telegram inline keyboard markup
        """
        loc = controller._localization

        keyboard = [
            [
                InlineKeyboardButton(
                    f"🎯 {loc.get_text('services_menu')}", callback_data="menu_services"
                )
            ],
            [
                InlineKeyboardButton(
                    f"📞 {loc.get_text('reservation')}",
                    callback_data="menu_reservation",
                )
            ],
            [
                InlineKeyboardButton(
                    f"📱 {loc.get_text('social_media')}", callback_data="menu_social"
                )
            ],
        ]
        return InlineKeyboardMarkup(keyboard)

    def _create_services_keyboard(
        self, controller: BotController
    ) -> InlineKeyboardMarkup:
        """
        Create inline keyboard for services menu.

        Args:
            controller: Bot controller instance

        Returns:
            Telegram inline keyboard markup
        """
        loc = controller._localization
        config = controller._config
        services = config.get_services()

        keyboard = []

        for idx, service in enumerate(services, 1):
            lang = loc.get_current_language()
            name = service.name_ar if lang == Language.ARABIC else service.name_en
            price = loc.format_price(service.price, service.currency)

            keyboard.append(
                [
                    InlineKeyboardButton(
                        f"{name} - {price}", callback_data=f"service_{idx}"
                    )
                ]
            )

        keyboard.append(
            [
                InlineKeyboardButton(
                    f"⬅️ {loc.get_text('back')}", callback_data="back_main"
                )
            ]
        )

        return InlineKeyboardMarkup(keyboard)

    def _create_back_keyboard(self, controller: BotController) -> InlineKeyboardMarkup:
        """
        Create inline keyboard with back button.

        Args:
            controller: Bot controller instance

        Returns:
            Telegram inline keyboard markup
        """
        loc = controller._localization

        keyboard = [
            [
                InlineKeyboardButton(
                    f"⬅️ {loc.get_text('back')}", callback_data="back_main"
                )
            ]
        ]
        return InlineKeyboardMarkup(keyboard)

    async def _start_command(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """
        Handle /start command - initialize conversation.

        Args:
            update: Telegram update object
            context: Callback context
        """
        user_id = update.effective_user.id
        controller = self._get_or_create_controller(user_id)

        # Start conversation and get welcome message
        welcome_message = controller.start()

        # Extract just the welcome part without language selection
        welcome_lines = welcome_message.split("=" * 50)
        welcome_text = welcome_lines[0].strip()

        await update.message.reply_text(
            welcome_text, reply_markup=self._create_language_keyboard()
        )

    async def _help_command(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """
        Handle /help command - show help information.

        Args:
            update: Telegram update object
            context: callback context
        """
        help_text = """
🤖 **Blue Whisper Ocean Club Bot**

**Available Commands:**
/start - Start conversation
/help - Show this help message
/menu - Show main menu
/services - View our services
/contact - Contact information

**How to Use:**
1. Select your language
2. Browse our services
3. Make a reservation via WhatsApp
4. Follow us on social media

**Need Help?**
Contact us on WhatsApp: +968-9123-4567
"""
        await update.message.reply_text(help_text, parse_mode="Markdown")

    async def _menu_command(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """
        Handle /menu command - show main menu.

        Args:
            update: Telegram update object
            context: Callback context
        """
        user_id = update.effective_user.id
        controller = self._get_or_create_controller(user_id)

        # Transition to main menu if not already there
        if controller.get_current_state() != BotState.MAIN_MENU:
            controller._transition_to(BotState.MAIN_MENU)

        menu_text = controller._localization.get_text("main_menu")

        await update.message.reply_text(
            menu_text, reply_markup=self._create_main_menu_keyboard(controller)
        )

    async def _services_command(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """
        Handle /services command - show services directly.

        Args:
            update: Telegram update object
            context: Callback context
        """
        user_id = update.effective_user.id
        controller = self._get_or_create_controller(user_id)

        controller._transition_to(BotState.SERVICES)
        services = controller._config.get_services()
        message = controller._message_builder.build_services_menu(services)

        # Remove the "0️⃣ Back" text as we have keyboard button
        message = message.replace(
            f"0️⃣ {controller._localization.get_text('back')}\n", ""
        )

        await update.message.reply_text(
            message, reply_markup=self._create_services_keyboard(controller)
        )

    async def _contact_command(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """
        Handle /contact command - show contact information.

        Args:
            update: Telegram update object
            context: Callback context
        """
        user_id = update.effective_user.id
        controller = self._get_or_create_controller(user_id)

        contact = controller._config.get_contact_info()
        controller._transition_to(BotState.SOCIAL_MEDIA)

        message = controller._message_builder.build_social_media_message(contact)
        message = message.replace(
            f"0️⃣ {controller._localization.get_text('back')}\n", ""
        )

        await update.message.reply_text(
            message, reply_markup=self._create_back_keyboard(controller)
        )

    async def _button_callback(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """
        Handle inline keyboard button callbacks.

        Args:
            update: Telegram update object
            context: Callback context
        """
        query = update.callback_query
        await query.answer()

        user_id = update.effective_user.id
        controller = self._get_or_create_controller(user_id)
        callback_data = query.data

        # Language selection
        if callback_data.startswith("lang_"):
            lang_code = callback_data.split("_")[1]

            if lang_code == "en":
                controller._localization.set_language(Language.ENGLISH)
            elif lang_code == "ar":
                controller._localization.set_language(Language.ARABIC)

            controller._transition_to(BotState.MAIN_MENU)
            menu_text = controller._localization.get_text("main_menu")

            await query.edit_message_text(
                menu_text, reply_markup=self._create_main_menu_keyboard(controller)
            )

        # Main menu navigation
        elif callback_data == "menu_services":
            controller._transition_to(BotState.SERVICES)
            services = controller._config.get_services()
            message = controller._message_builder.build_services_menu(services)
            message = message.replace(
                f"0️⃣ {controller._localization.get_text('back')}\n", ""
            )

            await query.edit_message_text(
                message, reply_markup=self._create_services_keyboard(controller)
            )

        elif callback_data == "menu_reservation":
            controller._transition_to(BotState.RESERVATION)
            contact = controller._config.get_contact_info()
            message = controller._message_builder.build_reservation_message(
                contact.whatsapp
            )
            message = message.replace(
                f"0️⃣ {controller._localization.get_text('back')}\n", ""
            )

            await query.edit_message_text(
                message,
                reply_markup=self._create_back_keyboard(controller),
                disable_web_page_preview=True,
            )

        elif callback_data == "menu_social":
            controller._transition_to(BotState.SOCIAL_MEDIA)
            contact = controller._config.get_contact_info()
            message = controller._message_builder.build_social_media_message(contact)
            message = message.replace(
                f"0️⃣ {controller._localization.get_text('back')}\n", ""
            )

            await query.edit_message_text(
                message,
                reply_markup=self._create_back_keyboard(controller),
                disable_web_page_preview=True,
            )

        # Service selection
        elif callback_data.startswith("service_"):
            controller._transition_to(BotState.RESERVATION)
            contact = controller._config.get_contact_info()
            message = controller._message_builder.build_reservation_message(
                contact.whatsapp
            )
            message = message.replace(
                f"0️⃣ {controller._localization.get_text('back')}\n", ""
            )

            await query.edit_message_text(
                message,
                reply_markup=self._create_back_keyboard(controller),
                disable_web_page_preview=True,
            )

        # Back to main menu
        elif callback_data == "back_main":
            controller._transition_to(BotState.MAIN_MENU)
            menu_text = controller._localization.get_text("main_menu")

            await query.edit_message_text(
                menu_text, reply_markup=self._create_main_menu_keyboard(controller)
            )

    async def _message_handler(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """
        Handle regular text messages.

        Args:
            update: Telegram update object
            context: Callback context
        """
        user_id = update.effective_user.id
        controller = self._get_or_create_controller(user_id)

        # If user hasn't started, prompt them to use /start
        if controller.get_current_state() == BotState.WELCOME:
            await update.message.reply_text("👋 Please use /start to begin!")
            return

        # Show main menu for any text input
        await update.message.reply_text(
            controller._localization.get_text("main_menu"),
            reply_markup=self._create_main_menu_keyboard(controller),
        )

    def setup_handlers(self) -> None:
        """Configure all bot command and callback handlers."""
        if not self._application:
            raise RuntimeError("Application not initialized")

        # Command handlers
        self._application.add_handler(CommandHandler("start", self._start_command))
        self._application.add_handler(CommandHandler("help", self._help_command))
        self._application.add_handler(CommandHandler("menu", self._menu_command))
        self._application.add_handler(
            CommandHandler("services", self._services_command)
        )
        self._application.add_handler(CommandHandler("contact", self._contact_command))

        # Callback query handler for inline buttons
        self._application.add_handler(CallbackQueryHandler(self._button_callback))

        # Message handler for text messages
        self._application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self._message_handler)
        )

    async def start(self) -> None:
        """Initialize and start the Telegram bot."""
        self._application = Application.builder().token(self._token).build()
        self.setup_handlers()

        print("🤖 Blue Whisper Bot is starting...")
        print("✅ Bot is ready and listening for messages!")

        await self._application.initialize()
        await self._application.start()
        await self._application.updater.start_polling(drop_pending_updates=True)

    async def stop(self) -> None:
        """Stop the Telegram bot gracefully."""
        if self._application:
            await self._application.updater.stop()
            await self._application.stop()
            await self._application.shutdown()
            print("👋 Bot stopped successfully!")
