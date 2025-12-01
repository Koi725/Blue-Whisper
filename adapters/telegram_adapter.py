"""
Telegram bot adapter with complete Blue Whisper services and human handoff.
"""

from typing import Optional, Dict
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from telegram.constants import ParseMode


class TelegramBotAdapter:
    """Complete Telegram bot with all Blue Whisper services."""

    def __init__(self, token: str):
        self._token = token
        self._application: Optional[Application] = None
        self._user_states: Dict[int, str] = {}
        self._user_languages: Dict[int, str] = {}
        self._human_mode: Dict[int, bool] = {}

        self._messages = {
            "en": {
                "welcome": "🌊 *Welcome to Blue Whisper Ocean Club!* 🌊\n\n✨ _Your Premium Ocean Adventure in Oman_ ✨\n\nExperience the beauty of the ocean with our world-class activities!\n\n📍 Marina Bandar Al-Rowdha, Muscat",
                "main_choice": "*How would you like to proceed?*\n\n🤖 Browse Services (Automated)\n👤 Speak with Our Team\n🎉 Special Events & Celebrations",
                "services_menu": "🏖️ *Our Ocean Activities*\n\nChoose a service to learn more:",
                "dolphin_info": "🐬 *Dolphin Watching Tours*\n\n📸 _Experience magical moments with dolphins!_\n\n🚢 *Private Boat:* 60 OMR (up to 6 people)\n⏰ 8-10 AM, 10 AM-12 PM, 12-2 PM\n\n🛥️ *Public Boat:* 10 OMR per person\n⏰ 8-10 AM, 10 AM-12 PM\n\n📍 Marina Bandar Al-Rowdha",
                "parasailing_info": "🪂 *Parasailing Adventure*\n\n🦅 _Fly above the beautiful Omani coast!_\n\n💰 18 OMR per person\n⏱️ 30-40 minutes\n👥 Depends on boat passengers\n⚖️ Max Weight: 200 KG\n⏰ 8 AM - Sunset\n\n⚠️ Must book in advance on WhatsApp",
                "sea_trip_info": "🚤 *Sea Trip Experience*\n\n🌊 _60-minute ocean journey with refreshments!_\n\n🛥️ Capacity 5 people - 60 min\n🚢 Capacity 12 people - 60 min\n🥤 Juice & Water included\n⏰ 8 AM - Sunset\n\n📍 Marina Bandar Al-Rowdha",
                "water_sports_info": "🏄 *Water Sports Activities*\n\n🏍️ *Crazy Jet Boat*\n💰 15 OMR/person | ⏱️ 15 min | 👥 Max 10\n\n🚤 *Shuttle Boating*\n💰 10 OMR/person | ⏱️ 15 min | 👥 Max 4\n\n🍌 *Banana Boat*\n💰 10 OMR/person | ⏱️ 15 min | 👥 Max 8\n\n⏰ 8 AM - Sunset",
                "snorkeling_info": "🤿 *Snorkeling Adventures*\n\n🐠 *Snorkeling Only*\n💰 12 OMR/person | ⏱️ 50-80 min | 👥 Max 6\n\n🐬 *Snorkeling + Dolphin*\n💰 18 OMR/person | ⏱️ 150-180 min | 👥 Max 6\n⏰ 8-11 AM | 11 AM-1 PM\n\n🌊 _Explore underwater beauty!_",
                "events_info": "🎉 *Special Events & Celebrations*\n\n✨ _Make your moments unforgettable!_\n\nWe organize:\n🎂 Birthday Parties\n💑 Anniversary Celebrations\n🎊 Private Events\n🏖️ Beach Parties\n👨‍👩‍👧‍👦 Family Gatherings\n\n🎨 *Customizable Themes*\n• Color schemes\n• Personalized decorations\n• Catering options\n• Photography services\n\n📞 Contact us for custom quotes!",
                "payment_info": "💳 *Payment Information*\n\n🏦 *Bank Transfer:*\nBank: Muscat Bank\nAccount: ALHAMS ALAZRAQ LLC\nIBAN: 0319049638080027\n\n📱 *Mobile Payment:*\nAccount: 71902763\nName: Mohsen Amiri\n\n💵 *Cash:* Pay at marina\n\n✅ Send receipt to:\n📞 +968-91220955\n📞 +968-91142192",
                "booking_info": "📞 *Ready to Book?*\n\n*WhatsApp:*\n📱 +968-91220955\n📱 +968-91142192\n\n📍 Marina Bandar Al-Rowdha\n⏰ 8 AM - Sunset (Daily)\n\n✨ We look forward to serving you!",
                "human_handoff": "✅ *Connecting to our team...*\n\n👨‍💼 A staff member will respond shortly.\n\n📞 *Direct contact:*\n+968-91220955\n+968-91142192\n\n⏰ Quick response during hours!",
                "back": "⬅️ Back",
                "book": "📞 Book Now",
                "menu": "🏖️ Main Menu",
            },
            "ar": {
                "welcome": "🌊 *مرحباً بكم في نادي بلو ويسبر البحري!* 🌊\n\n✨ _وجهتكم المميزة للمغامرات البحرية_ ✨\n\nاستمتعوا بجمال المحيط مع أنشطتنا!\n\n📍 مارينا بندر الروضة، مسقط",
                "main_choice": "*كيف تريد المتابعة؟*\n\n🤖 تصفح الخدمات (آلي)\n👤 التحدث مع فريقنا\n🎉 المناسبات الخاصة",
                "services_menu": "🏖️ *أنشطتنا البحرية*\n\nاختر خدمة لمعرفة المزيد:",
                "dolphin_info": "🐬 *جولات مشاهدة الدلافين*\n\n📸 _عيش لحظات سحرية!_\n\n🚢 *قارب خاص:* 60 ريال (حتى 6 أشخاص)\n⏰ 8-10 ص، 10-12 ظ، 12-2 م\n\n🛥️ *قارب عام:* 10 ريال للشخص\n⏰ 8-10 ص، 10-12 ظ\n\n📍 مارينا بندر الروضة",
                "parasailing_info": "🪂 *مغامرة الطيران الشراعي*\n\n🦅 _حلق فوق ساحل عمان!_\n\n💰 18 ريال للشخص\n⏱️ 30-40 دقيقة\n👥 حسب ركاب القارب\n⚖️ الوزن الأقصى: 200 كجم\n⏰ 8 صباحاً - الغروب\n\n⚠️ يجب الحجز مسبقاً",
                "sea_trip_info": "🚤 *تجربة الرحلة البحرية*\n\n🌊 _رحلة 60 دقيقة مع مرطبات!_\n\n🛥️ سعة 5 أشخاص - 60 دقيقة\n🚢 سعة 12 شخص - 60 دقيقة\n🥤 عصير وماء متضمن\n⏰ 8 صباحاً - الغروب\n\n📍 مارينا بندر الروضة",
                "water_sports_info": "🏄 *الرياضات المائية*\n\n🏍️ *قارب جت المجنون*\n💰 15 ريال/شخص | ⏱️ 15 دقيقة | 👥 حتى 10\n\n🚤 *القارب المكوكي*\n💰 10 ريال/شخص | ⏱️ 15 دقيقة | 👥 حتى 4\n\n🍌 *قارب الموز*\n💰 10 ريال/شخص | ⏱️ 15 دقيقة | 👥 حتى 8\n\n⏰ 8 صباحاً - الغروب",
                "snorkeling_info": "🤿 *مغامرات الغوص*\n\n🐠 *الغوص فقط*\n💰 12 ريال/شخص | ⏱️ 50-80 دقيقة | 👥 حتى 6\n\n🐬 *الغوص + الدلافين*\n💰 18 ريال/شخص | ⏱️ 150-180 دقيقة | 👥 حتى 6\n⏰ 8-11 ص | 11 ص-1 ظ\n\n🌊 _استكشف الجمال تحت الماء!_",
                "events_info": "🎉 *المناسبات الخاصة*\n\n✨ _اجعل لحظاتك لا تُنسى!_\n\nننظم:\n🎂 حفلات أعياد الميلاد\n💑 احتفالات الذكرى\n🎊 المناسبات الخاصة\n🏖️ حفلات الشاطئ\n👨‍👩‍👧‍👦 التجمعات العائلية\n\n🎨 *ثيمات مخصصة*\n• نظام الألوان\n• ديكورات شخصية\n• خيارات الطعام\n• خدمات التصوير\n\n📞 اتصل بنا للعروض!",
                "payment_info": "💳 *معلومات الدفع*\n\n🏦 *تحويل بنكي:*\nالبنك: بنك مسقط\nالحساب: ALHAMS ALAZRAQ LLC\nIBAN: 0319049638080027\n\n📱 *دفع موبايل:*\nالحساب: 71902763\nالاسم: محسن أميري\n\n💵 *نقدي:* ادفع في المارينا\n\n✅ أرسل الإيصال:\n📞 +968-91220955\n📞 +968-91142192",
                "booking_info": "📞 *جاهز للحجز؟*\n\n*واتساب:*\n📱 +968-91220955\n📱 +968-91142192\n\n📍 مارينا بندر الروضة\n⏰ 8 صباحاً - الغروب (يومياً)\n\n✨ نتطلع لخدمتكم!",
                "human_handoff": "✅ *جاري التوصيل بفريقنا...*\n\n👨‍💼 سيرد عليك موظف قريباً.\n\n📞 *اتصال مباشر:*\n+968-91220955\n+968-91142192\n\n⏰ رد سريع أثناء ساعات العمل!",
                "back": "⬅️ رجوع",
                "book": "📞 احجز الآن",
                "menu": "🏖️ القائمة الرئيسية",
            },
        }

    def _get_lang_keyboard(self) -> InlineKeyboardMarkup:
        """Language selection keyboard."""
        return InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"),
                    InlineKeyboardButton("🇴🇲 العربية", callback_data="lang_ar"),
                ]
            ]
        )

    def _get_main_choice_keyboard(self, lang: str) -> InlineKeyboardMarkup:
        """Main choice keyboard."""
        if lang == "en":
            return InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🤖 Browse Services", callback_data="choice_services"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "👤 Speak with Team", callback_data="choice_human"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "🎉 Special Events", callback_data="choice_events"
                        )
                    ],
                ]
            )
        else:
            return InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🤖 تصفح الخدمات", callback_data="choice_services"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "👤 التحدث مع الفريق", callback_data="choice_human"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "🎉 المناسبات الخاصة", callback_data="choice_events"
                        )
                    ],
                ]
            )

    def _get_services_keyboard(self, lang: str) -> InlineKeyboardMarkup:
        """Services menu keyboard."""
        if lang == "en":
            keyboard = [
                [
                    InlineKeyboardButton(
                        "🐬 Dolphin Watching", callback_data="service_dolphin"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🪂 Parasailing", callback_data="service_parasailing"
                    )
                ],
                [InlineKeyboardButton("🚤 Sea Trip", callback_data="service_seatrip")],
                [
                    InlineKeyboardButton(
                        "� Water Sports", callback_data="service_watersports"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🤿 Snorkeling", callback_data="service_snorkeling"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "💳 Payment Info", callback_data="service_payment"
                    )
                ],
                [
                    InlineKeyboardButton("⬅️ Back", callback_data="back_main"),
                    InlineKeyboardButton(
                        "👤 Talk to Human", callback_data="choice_human"
                    ),
                ],
            ]
        else:
            keyboard = [
                [
                    InlineKeyboardButton(
                        "🐬 مشاهدة الدلافين", callback_data="service_dolphin"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🪂 الطيران الشراعي", callback_data="service_parasailing"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🚤 رحلة بحرية", callback_data="service_seatrip"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🏄 الرياضات المائية", callback_data="service_watersports"
                    )
                ],
                [InlineKeyboardButton("🤿 الغوص", callback_data="service_snorkeling")],
                [
                    InlineKeyboardButton(
                        "💳 معلومات الدفع", callback_data="service_payment"
                    )
                ],
                [
                    InlineKeyboardButton("⬅️ رجوع", callback_data="back_main"),
                    InlineKeyboardButton(
                        "👤 تحدث مع شخص", callback_data="choice_human"
                    ),
                ],
            ]
        return InlineKeyboardMarkup(keyboard)

    def _get_back_book_keyboard(self, lang: str) -> InlineKeyboardMarkup:
        """Back and book keyboard."""
        msgs = self._messages[lang]
        return InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(msgs["back"], callback_data="back_services"),
                    InlineKeyboardButton(msgs["book"], callback_data="service_booking"),
                ]
            ]
        )

    async def _start_command(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Handle /start command."""
        user_id = update.effective_user.id
        self._user_states[user_id] = "language"

        welcome = self._messages["en"]["welcome"]

        await update.message.reply_text(
            welcome,
            reply_markup=self._get_lang_keyboard(),
            parse_mode=ParseMode.MARKDOWN,
        )

    async def _button_callback(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Handle button callbacks."""
        query = update.callback_query
        await query.answer()

        user_id = update.effective_user.id
        data = query.data
        lang = self._user_languages.get(user_id, "en")
        msgs = self._messages[lang]

        # Language selection
        if data.startswith("lang_"):
            lang_code = data.split("_")[1]
            self._user_languages[user_id] = lang_code
            self._user_states[user_id] = "main_choice"

            await query.edit_message_text(
                self._messages[lang_code]["main_choice"],
                reply_markup=self._get_main_choice_keyboard(lang_code),
                parse_mode=ParseMode.MARKDOWN,
            )

        # Main choices
        elif data == "choice_services":
            self._user_states[user_id] = "services"
            await query.edit_message_text(
                msgs["services_menu"],
                reply_markup=self._get_services_keyboard(lang),
                parse_mode=ParseMode.MARKDOWN,
            )

        elif data == "choice_human":
            self._human_mode[user_id] = True
            await query.edit_message_text(
                msgs["human_handoff"], parse_mode=ParseMode.MARKDOWN
            )

        elif data == "choice_events":
            await query.edit_message_text(
                msgs["events_info"],
                reply_markup=self._get_back_book_keyboard(lang),
                parse_mode=ParseMode.MARKDOWN,
            )

        # Services
        elif data.startswith("service_"):
            service = data.split("_")[1]
            text = msgs.get(f"{service}_info", "Service info not available")

            await query.edit_message_text(
                text,
                reply_markup=self._get_back_book_keyboard(lang),
                parse_mode=ParseMode.MARKDOWN,
            )

        elif data == "service_booking":
            await query.edit_message_text(
                msgs["booking_info"],
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                msgs["back"], callback_data="back_services"
                            )
                        ]
                    ]
                ),
                parse_mode=ParseMode.MARKDOWN,
            )

        # Navigation
        elif data == "back_services":
            await query.edit_message_text(
                msgs["services_menu"],
                reply_markup=self._get_services_keyboard(lang),
                parse_mode=ParseMode.MARKDOWN,
            )

        elif data == "back_main":
            self._user_states[user_id] = "main_choice"
            await query.edit_message_text(
                msgs["main_choice"],
                reply_markup=self._get_main_choice_keyboard(lang),
                parse_mode=ParseMode.MARKDOWN,
            )

    async def _message_handler(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Handle text messages."""
        user_id = update.effective_user.id

        # If in human mode, don't respond
        if self._human_mode.get(user_id):
            return

        lang = self._user_languages.get(user_id, "en")
        msgs = self._messages[lang]

        await update.message.reply_text(
            msgs.get("menu", "Use /start to begin"),
            reply_markup=self._get_main_choice_keyboard(lang),
            parse_mode=ParseMode.MARKDOWN,
        )

    def setup_handlers(self) -> None:
        """Setup all handlers."""
        if not self._application:
            raise RuntimeError("Application not initialized")

        self._application.add_handler(CommandHandler("start", self._start_command))
        self._application.add_handler(CallbackQueryHandler(self._button_callback))
        self._application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self._message_handler)
        )

    async def start(self) -> None:
        """Start the bot."""
        self._application = Application.builder().token(self._token).build()
        self.setup_handlers()

        print("🤖 Blue Whisper Telegram Bot starting...")
        print("✅ Bot is ready!")

        await self._application.initialize()
        await self._application.start()
        await self._application.updater.start_polling(drop_pending_updates=True)

    async def stop(self) -> None:
        """Stop the bot."""
        if self._application:
            await self._application.updater.stop()
            await self._application.stop()
            await self._application.shutdown()
