"""
Blue Whisper Telegram Bot - Premium User Experience
Intuitive navigation with back buttons, clear menus, and beautiful formatting
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
    """Premium Telegram bot with 10/10 user experience."""

    def __init__(self, token: str):
        self._token = token
        self._application: Optional[Application] = None
        self._user_states: Dict[int, str] = {}
        self._user_languages: Dict[int, str] = {}
        self._human_mode: Dict[int, bool] = {}

        self._messages = {
            "en": {
                "welcome": "🌊 *Welcome to Blue Whisper Ocean Club!* 🌊\n\n✨ _Your Premium Ocean Adventure in Oman_ ✨\n\nExperience the beauty of the ocean with our world-class activities!\n\n📍 Marina Bandar Al-Rowdha, Muscat\n🌐 www.muscatjoy.com",
                "main_menu": "*🏖️ Main Menu*\n\nWhat would you like to explore?",
                "services_intro": "🌊 *Discover Our Ocean Activities*\n\nSelect any service below to see details, pricing, and availability!",
                "dolphin_info": "🐬 *Dolphin Watching Tours*\n━━━━━━━━━━━━━━━\n\n📸 Experience magical moments with dolphins in their natural habitat!\n\n*🚢 PRIVATE BOAT TOUR*\n💰 Price: 60 OMR (up to 6 people)\n⏰ Times:\n   • 8:00 - 10:00 AM\n   • 10:00 AM - 12:00 PM\n   • 12:00 - 2:00 PM\n\n*🛥️ PUBLIC BOAT TOUR*\n💰 Price: 10 OMR per person\n⏰ Times:\n   • 8:00 - 10:00 AM\n   • 10:00 AM - 12:00 PM\n\n📍 Location: Marina Bandar Al-Rowdha\n\n_Perfect for families and nature lovers!_",
                "parasailing_info": "🪂 *Parasailing Adventure*\n━━━━━━━━━━━━━━━\n\n🦅 Soar above the crystal-clear waters of Oman!\n\n💰 *Price:* 18 OMR per person\n⏱️ *Duration:* 30-40 minutes\n👥 *Group Size:* Depends on boat capacity\n⚖️ *Max Weight:* 200 KG per person\n⏰ *Operating Hours:* 8 AM - Sunset\n\n⚠️ *Important:* Advanced booking required via WhatsApp\n\n📍 Location: Marina Bandar Al-Rowdha\n\n_An unforgettable aerial experience!_",
                "sea_trip_info": "🚤 *Sea Trip Experience*\n━━━━━━━━━━━━━━━\n\n🌊 Enjoy a relaxing 60-minute ocean journey!\n\n*🛥️ OPTION 1: SMALL BOAT*\n👥 Capacity: Up to 5 people\n⏱️ Duration: 60 minutes\n🥤 Includes: Juice & Water\n\n*🚢 OPTION 2: LARGE BOAT*\n👥 Capacity: Up to 12 people\n⏱️ Duration: 60 minutes\n🥤 Includes: Juice & Water\n\n⏰ *Operating Hours:* 8 AM - Sunset\n📍 Location: Marina Bandar Al-Rowdha\n\n_Perfect for groups and families!_",
                "water_sports_info": "🏄 *Water Sports Activities*\n━━━━━━━━━━━━━━━\n\nGet your adrenaline pumping!\n\n*🏍️ CRAZY JET BOAT*\n💰 15 OMR per person\n⏱️ 15 minutes\n👥 Max 10 people\n\n*🚤 SHUTTLE BOATING*\n💰 10 OMR per person\n⏱️ 15 minutes\n👥 Max 4 people\n\n*🍌 BANANA BOAT RIDE*\n💰 10 OMR per person\n⏱️ 15 minutes\n👥 Max 8 people\n\n⏰ *Operating Hours:* 8 AM - Sunset\n📍 Location: Marina Bandar Al-Rowdha\n\n_Thrills and fun for everyone!_",
                "snorkeling_info": "🤿 *Snorkeling Adventures*\n━━━━━━━━━━━━━━━\n\n🐠 Explore the underwater paradise of Oman!\n\n*OPTION 1: SNORKELING ONLY*\n💰 12 OMR per person\n⏱️ 50-80 minutes\n👥 Max 6 people\n\n*OPTION 2: SNORKELING + DOLPHIN WATCHING*\n💰 18 OMR per person\n⏱️ 150-180 minutes (2.5-3 hours)\n👥 Max 6 people\n⏰ Times:\n   • 8:00 - 11:00 AM\n   • 11:00 AM - 1:00 PM\n\n📍 Location: Marina Bandar Al-Rowdha\n\n_Discover colorful marine life!_",
                "events_info": "🎉 *Special Events & Celebrations*\n━━━━━━━━━━━━━━━\n\n✨ Make your special moments unforgettable on the ocean!\n\n*WE ORGANIZE:*\n🎂 Birthday Parties\n💑 Anniversary Celebrations\n🎊 Private Corporate Events\n🏖️ Beach Parties\n👨‍👩‍👧‍👦 Family Gatherings\n🥂 Proposal & Engagement Events\n\n*🎨 CUSTOMIZABLE FEATURES:*\n• Your choice of color themes\n• Personalized decorations\n• Professional photography\n• Catering & refreshments\n• Music & entertainment\n• Custom cake & gifts\n\n💰 *Pricing:* Custom quotes based on your needs\n\n📞 Contact our event planning team for personalized packages!",
                "payment_info": "💳 *Payment Information*\n━━━━━━━━━━━━━━━\n\n*OPTION 1: BANK TRANSFER*\n🏦 Bank: Muscat Bank\n👤 Account Name: ALHAMS ALAZRAQ LLC\n🔢 IBAN: 0319049638080027\n\n*OPTION 2: MOBILE PAYMENT*\n📱 Muscat Bank Mobile Pay\n🔢 Account: 71902763\n👤 Name: Mohsen Amiri\n\n*OPTION 3: CASH*\n💵 Pay directly at the marina\n📍 Marina Bandar Al-Rowdha\n\n*AFTER PAYMENT:*\n✅ Send receipt via WhatsApp:\n📞 +968-77752752\n📞 +968-91220956\n\n_We'll confirm your booking immediately!_",
                "booking_info": "📞 *Ready to Book Your Adventure?*\n━━━━━━━━━━━━━━━\n\n*CONTACT US:*\n📱 WhatsApp: +968-77752752\n📱 Phone: +968-91220956\n🌐 Website: www.muscatjoy.com\n\n*VISIT US:*\n📍 Marina Bandar Al-Rowdha, Muscat\n⏰ Open Daily: 8:00 AM - Sunset\n\n*BOOKING TIPS:*\n✓ Book 24 hours in advance for best availability\n✓ Group discounts available\n✓ Flexible cancellation policy\n✓ All safety equipment provided\n\n✨ _We look forward to creating amazing memories with you!_",
                "contact_info": "📞 *Contact Blue Whisper*\n━━━━━━━━━━━━━━━\n\n*PHONE & WHATSAPP:*\n📱 +968-77752752\n📱 +968-91220956\n\n*ONLINE:*\n🌐 www.muscatjoy.com\n\n*LOCATION:*\n📍 Marina Bandar Al-Rowdha\n🗺️ Muscat, Oman\n\n*HOURS:*\n⏰ 8:00 AM - Sunset\n📅 Open 7 Days a Week\n\n_Our team is ready to help you!_",
                "human_handoff": "👨‍💼 *Connecting You to Our Team*\n━━━━━━━━━━━━━━━\n\n✅ A team member will respond to your next message shortly.\n\n*DIRECT CONTACT:*\n📱 +968-77752752\n📱 +968-91220956\n🌐 www.muscatjoy.com\n\n⏰ Response time: Usually within minutes during business hours!\n\n_Feel free to ask anything - we're here to help!_",
            },
            "ar": {
                "welcome": "🌊 *مرحباً بكم في نادي بلو ويسبر البحري!* 🌊\n\n✨ _وجهتكم المميزة للمغامرات البحرية في عمان_ ✨\n\nاستمتعوا بجمال المحيط مع أنشطتنا العالمية!\n\n📍 مارينا بندر الروضة، مسقط\n🌐 www.muscatjoy.com",
                "main_menu": "*🏖️ القائمة الرئيسية*\n\nماذا تريد أن تستكشف؟",
                "services_intro": "🌊 *اكتشف أنشطتنا البحرية*\n\nاختر أي خدمة أدناه لرؤية التفاصيل والأسعار!",
                "dolphin_info": "🐬 *جولات مشاهدة الدلافين*\n━━━━━━━━━━━━━━━\n\n📸 عش لحظات سحرية مع الدلافين في بيئتها الطبيعية!\n\n*🚢 جولة القارب الخاص*\n💰 السعر: 60 ريال (حتى 6 أشخاص)\n⏰ الأوقات:\n   • 8:00 - 10:00 صباحاً\n   • 10:00 - 12:00 ظهراً\n   • 12:00 - 2:00 مساءً\n\n*🛥️ جولة القارب العام*\n💰 السعر: 10 ريال للشخص\n⏰ الأوقات:\n   • 8:00 - 10:00 صباحاً\n   • 10:00 - 12:00 ظهراً\n\n📍 الموقع: مارينا بندر الروضة\n\n_مثالي للعائلات ومحبي الطبيعة!_",
                "parasailing_info": "🪂 *مغامرة الطيران الشراعي*\n━━━━━━━━━━━━━━━\n\n🦅 حلق فوق المياه الصافية لعمان!\n\n💰 *السعر:* 18 ريال للشخص\n⏱️ *المدة:* 30-40 دقيقة\n👥 *حجم المجموعة:* حسب سعة القارب\n⚖️ *الوزن الأقصى:* 200 كجم للشخص\n⏰ *ساعات العمل:* 8 صباحاً - الغروب\n\n⚠️ *مهم:* يتطلب حجز مسبق عبر واتساب\n\n📍 الموقع: مارينا بندر الروضة\n\n_تجربة جوية لا تُنسى!_",
                "sea_trip_info": "🚤 *تجربة الرحلة البحرية*\n━━━━━━━━━━━━━━━\n\n🌊 استمتع برحلة بحرية مريحة لمدة 60 دقيقة!\n\n*🛥️ الخيار 1: قارب صغير*\n👥 السعة: حتى 5 أشخاص\n⏱️ المدة: 60 دقيقة\n🥤 يتضمن: عصير وماء\n\n*🚢 الخيار 2: قارب كبير*\n👥 السعة: حتى 12 شخص\n⏱️ المدة: 60 دقيقة\n🥤 يتضمن: عصير وماء\n\n⏰ *ساعات العمل:* 8 صباحاً - الغروب\n📍 الموقع: مارينا بندر الروضة\n\n_مثالي للمجموعات والعائلات!_",
                "water_sports_info": "🏄 *أنشطة الرياضات المائية*\n━━━━━━━━━━━━━━━\n\nاحصل على جرعة الأدرينالين!\n\n*🏍️ قارب جت المجنون*\n💰 15 ريال للشخص\n⏱️ 15 دقيقة\n👥 حتى 10 أشخاص\n\n*🚤 القارب المكوكي*\n💰 10 ريال للشخص\n⏱️ 15 دقيقة\n👥 حتى 4 أشخاص\n\n*🍌 ركوب قارب الموز*\n💰 10 ريال للشخص\n⏱️ 15 دقيقة\n👥 حتى 8 أشخاص\n\n⏰ *ساعات العمل:* 8 صباحاً - الغروب\n📍 الموقع: مارينا بندر الروضة\n\n_إثارة ومرح للجميع!_",
                "snorkeling_info": "🤿 *مغامرات الغوص*\n━━━━━━━━━━━━━━━\n\n🐠 استكشف الجنة تحت الماء في عمان!\n\n*الخيار 1: الغوص فقط*\n💰 12 ريال للشخص\n⏱️ 50-80 دقيقة\n👥 حتى 6 أشخاص\n\n*الخيار 2: الغوص + مشاهدة الدلافين*\n💰 18 ريال للشخص\n⏱️ 150-180 دقيقة (2.5-3 ساعات)\n👥 حتى 6 أشخاص\n⏰ الأوقات:\n   • 8:00 - 11:00 صباحاً\n   • 11:00 صباحاً - 1:00 ظهراً\n\n📍 الموقع: مارينا بندر الروضة\n\n_اكتشف الحياة البحرية الملونة!_",
                "events_info": "🎉 *المناسبات والاحتفالات الخاصة*\n━━━━━━━━━━━━━━━\n\n✨ اجعل لحظاتك الخاصة لا تُنسى على المحيط!\n\n*ننظم:*\n🎂 حفلات أعياد الميلاد\n💑 احتفالات الذكرى السنوية\n🎊 الفعاليات الخاصة للشركات\n🏖️ حفلات الشاطئ\n👨‍👩‍👧‍👦 التجمعات العائلية\n🥂 فعاليات الخطوبة والزواج\n\n*🎨 ميزات قابلة للتخصيص:*\n• اختيار ثيمات الألوان\n• ديكورات شخصية\n• تصوير احترافي\n• خدمات الطعام والمشروبات\n• موسيقى وترفيه\n• كيك وهدايا مخصصة\n\n💰 *الأسعار:* عروض مخصصة حسب احتياجاتك\n\n📞 اتصل بفريق تخطيط الفعاليات للحصول على باقات شخصية!",
                "payment_info": "💳 *معلومات الدفع*\n━━━━━━━━━━━━━━━\n\n*الخيار 1: تحويل بنكي*\n🏦 البنك: بنك مسقط\n👤 اسم الحساب: ALHAMS ALAZRAQ LLC\n🔢 IBAN: 0319049638080027\n\n*الخيار 2: الدفع عبر الموبايل*\n📱 دفع موبايل بنك مسقط\n🔢 الحساب: 71902763\n👤 الاسم: محسن أميري\n\n*الخيار 3: نقدي*\n💵 ادفع مباشرة في المارينا\n📍 مارينا بندر الروضة\n\n*بعد الدفع:*\n✅ أرسل الإيصال عبر واتساب:\n📞 +968-77752752\n📞 +968-91220956\n\n_سنؤكد حجزك فوراً!_",
                "booking_info": "📞 *جاهز لحجز مغامرتك؟*\n━━━━━━━━━━━━━━━\n\n*اتصل بنا:*\n📱 واتساب: +968-77752752\n📱 هاتف: +968-91220956\n🌐 الموقع: www.muscatjoy.com\n\n*قم بزيارتنا:*\n📍 مارينا بندر الروضة، مسقط\n⏰ مفتوح يومياً: 8:00 صباحاً - الغروب\n\n*نصائح الحجز:*\n✓ احجز قبل 24 ساعة لأفضل توفر\n✓ خصومات المجموعات متاحة\n✓ سياسة إلغاء مرنة\n✓ جميع معدات السلامة متوفرة\n\n✨ _نتطلع لخلق ذكريات رائعة معك!_",
                "contact_info": "📞 *اتصل ببلو ويسبر*\n━━━━━━━━━━━━━━━\n\n*الهاتف وواتساب:*\n📱 +968-77752752\n📱 +968-91220956\n\n*عبر الإنترنت:*\n🌐 www.muscatjoy.com\n\n*الموقع:*\n📍 مارينا بندر الروضة\n🗺️ مسقط، عمان\n\n*ساعات العمل:*\n⏰ 8:00 صباحاً - الغروب\n📅 مفتوح 7 أيام في الأسبوع\n\n_فريقنا جاهز لمساعدتك!_",
                "human_handoff": "👨‍💼 *نوصلك بفريقنا*\n━━━━━━━━━━━━━━━\n\n✅ سيرد عليك أحد أعضاء الفريق على رسالتك القادمة قريباً.\n\n*اتصال مباشر:*\n📱 +968-77752752\n📱 +968-91220956\n🌐 www.muscatjoy.com\n\n⏰ وقت الاستجابة: عادة خلال دقائق خلال ساعات العمل!\n\n_لا تتردد في السؤال عن أي شيء - نحن هنا للمساعدة!_",
            },
        }

    def _get_lang_keyboard(self) -> InlineKeyboardMarkup:
        """Language selection with flags."""
        return InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"),
                    InlineKeyboardButton("🇴🇲 العربية", callback_data="lang_ar"),
                ]
            ]
        )

    def _get_main_menu_keyboard(self, lang: str) -> InlineKeyboardMarkup:
        """Beautiful main menu with emojis."""
        if lang == "en":
            return InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🌊 Ocean Activities", callback_data="menu_services"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "🎉 Special Events", callback_data="menu_events"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "💳 Payment Methods", callback_data="menu_payment"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "📞 Contact Us", callback_data="menu_contact"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "👤 Talk to Human", callback_data="menu_human"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "🌐 Change Language", callback_data="menu_language"
                        )
                    ],
                ]
            )
        else:
            return InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🌊 الأنشطة البحرية", callback_data="menu_services"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "🎉 المناسبات الخاصة", callback_data="menu_events"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "💳 طرق الدفع", callback_data="menu_payment"
                        )
                    ],
                    [InlineKeyboardButton("📞 اتصل بنا", callback_data="menu_contact")],
                    [
                        InlineKeyboardButton(
                            "👤 تحدث مع شخص", callback_data="menu_human"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "🌐 تغيير اللغة", callback_data="menu_language"
                        )
                    ],
                ]
            )

    def _get_services_keyboard(self, lang: str) -> InlineKeyboardMarkup:
        """Services grid with easy navigation."""
        if lang == "en":
            keyboard = [
                [
                    InlineKeyboardButton(
                        "🐬 Dolphin Watching", callback_data="service_dolphin"
                    ),
                    InlineKeyboardButton(
                        "🪂 Parasailing", callback_data="service_parasailing"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "🚤 Sea Trips", callback_data="service_seatrip"
                    ),
                    InlineKeyboardButton(
                        "🏄 Water Sports", callback_data="service_watersports"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "🤿 Snorkeling", callback_data="service_snorkeling"
                    )
                ],
                [
                    InlineKeyboardButton("📞 Book Now", callback_data="action_book"),
                    InlineKeyboardButton("⬅️ Main Menu", callback_data="back_main"),
                ],
            ]
        else:
            keyboard = [
                [
                    InlineKeyboardButton(
                        "🐬 مشاهدة الدلافين", callback_data="service_dolphin"
                    ),
                    InlineKeyboardButton(
                        "🪂 الطيران الشراعي", callback_data="service_parasailing"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "🚤 رحلات بحرية", callback_data="service_seatrip"
                    ),
                    InlineKeyboardButton(
                        "🏄 الرياضات المائية", callback_data="service_watersports"
                    ),
                ],
                [InlineKeyboardButton("🤿 الغوص", callback_data="service_snorkeling")],
                [
                    InlineKeyboardButton("📞 احجز الآن", callback_data="action_book"),
                    InlineKeyboardButton(
                        "⬅️ القائمة الرئيسية", callback_data="back_main"
                    ),
                ],
            ]
        return InlineKeyboardMarkup(keyboard)

    def _get_service_detail_keyboard(self, lang: str) -> InlineKeyboardMarkup:
        """Navigation for service details."""
        if lang == "en":
            return InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "📞 Book This Activity", callback_data="action_book"
                        ),
                        InlineKeyboardButton(
                            "💳 Payment Info", callback_data="menu_payment"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            "⬅️ All Services", callback_data="menu_services"
                        ),
                        InlineKeyboardButton("🏠 Main Menu", callback_data="back_main"),
                    ],
                ]
            )
        else:
            return InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "📞 احجز هذا النشاط", callback_data="action_book"
                        ),
                        InlineKeyboardButton(
                            "💳 معلومات الدفع", callback_data="menu_payment"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            "⬅️ كل الخدمات", callback_data="menu_services"
                        ),
                        InlineKeyboardButton(
                            "🏠 القائمة الرئيسية", callback_data="back_main"
                        ),
                    ],
                ]
            )

    def _get_info_keyboard(self, lang: str) -> InlineKeyboardMarkup:
        """Navigation for info pages."""
        if lang == "en":
            return InlineKeyboardMarkup(
                [[InlineKeyboardButton("⬅️ Main Menu", callback_data="back_main")]]
            )
        else:
            return InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "⬅️ القائمة الرئيسية", callback_data="back_main"
                        )
                    ]
                ]
            )

    async def _start_command(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Welcoming start command."""
        user_id = update.effective_user.id
        self._user_states[user_id] = "language"

        welcome = self._messages["en"]["welcome"]

        await update.message.reply_text(
            welcome + "\n\n*Select Your Language / اختر لغتك:*",
            reply_markup=self._get_lang_keyboard(),
            parse_mode=ParseMode.MARKDOWN,
        )

    async def _button_callback(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Smart button handler with perfect navigation."""
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
            self._user_states[user_id] = "main_menu"

            await query.edit_message_text(
                self._messages[lang_code]["main_menu"],
                reply_markup=self._get_main_menu_keyboard(lang_code),
                parse_mode=ParseMode.MARKDOWN,
            )

        # Main menu items
        elif data == "menu_services":
            await query.edit_message_text(
                msgs["services_intro"],
                reply_markup=self._get_services_keyboard(lang),
                parse_mode=ParseMode.MARKDOWN,
            )

        elif data == "menu_events":
            await query.edit_message_text(
                msgs["events_info"],
                reply_markup=self._get_service_detail_keyboard(lang),
                parse_mode=ParseMode.MARKDOWN,
            )

        elif data == "menu_payment":
            await query.edit_message_text(
                msgs["payment_info"],
                reply_markup=self._get_info_keyboard(lang),
                parse_mode=ParseMode.MARKDOWN,
            )

        elif data == "menu_contact":
            await query.edit_message_text(
                msgs["contact_info"],
                reply_markup=self._get_info_keyboard(lang),
                parse_mode=ParseMode.MARKDOWN,
            )

        elif data == "menu_human":
            self._human_mode[user_id] = True
            await query.edit_message_text(
                msgs["human_handoff"], parse_mode=ParseMode.MARKDOWN
            )

        elif data == "menu_language":
            await query.edit_message_text(
                "*Select Your Language / اختر لغتك:*",
                reply_markup=self._get_lang_keyboard(),
                parse_mode=ParseMode.MARKDOWN,
            )

        # Services
        elif data.startswith("service_"):
            service = data.split("_")[1]
            text = msgs.get(f"{service}_info", "Service info")

            await query.edit_message_text(
                text,
                reply_markup=self._get_service_detail_keyboard(lang),
                parse_mode=ParseMode.MARKDOWN,
            )

        elif data == "action_book":
            await query.edit_message_text(
                msgs["booking_info"],
                reply_markup=self._get_info_keyboard(lang),
                parse_mode=ParseMode.MARKDOWN,
            )

        # Navigation
        elif data == "back_main":
            self._user_states[user_id] = "main_menu"
            await query.edit_message_text(
                msgs["main_menu"],
                reply_markup=self._get_main_menu_keyboard(lang),
                parse_mode=ParseMode.MARKDOWN,
            )

    async def _message_handler(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Handle text messages - guide users to menu."""
        user_id = update.effective_user.id

        # If in human mode, don't respond
        if self._human_mode.get(user_id):
            return

        lang = self._user_languages.get(user_id, "en")
        msgs = self._messages[lang]

        await update.message.reply_text(
            msgs["main_menu"],
            reply_markup=self._get_main_menu_keyboard(lang),
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
        print("✅ 10/10 User Experience Active!")
        print("🌐 www.muscatjoy.com")
        print("📞 +968-77752752")

        await self._application.initialize()
        await self._application.start()
        await self._application.updater.start_polling(drop_pending_updates=True)

    async def stop(self) -> None:
        """Stop the bot."""
        if self._application:
            await self._application.updater.stop()
            await self._application.stop()
            await self._application.shutdown()
