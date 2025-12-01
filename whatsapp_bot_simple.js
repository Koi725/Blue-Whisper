const { default: makeWASocket, DisconnectReason, useMultiFileAuthState } = require('@whiskeysockets/baileys');
const qrcode = require('qrcode-terminal');
const fs = require('fs');
const path = require('path');

// User states
const userStates = {};
const userLanguages = {};
const humanMode = {};

// Service images (base64 encoded - you can replace with actual image paths)
const serviceImages = {
    dolphin: './images/dolphin.jpg',
    parasailing: './images/parasailing.jpg',
    seaTrip: './images/sea_trip.jpg',
    // crazyJet: './images/crazy_jet.jpg',
    // shuttleBoat: './images/shuttle.jpg',
    // bananaBoat: './images/banana.jpg',
    // snorkeling: './images/snorkeling.jpg',
    events: './images/events.jpg'
};

const messages = {
    en: {
        welcome: "🌊 *Welcome to Blue Whisper Ocean Club!* 🌊\n\n✨ _Your Premium Ocean Adventure in Oman_ ✨\n\nExperience the beauty of the ocean with our world-class activities!\n\n📍 Marina Bandar Al-Rowdha, Muscat\n\n",
        
        mainChoice: "*How would you like to proceed?*\n\n🤖 *1* - Browse Services (Automated)\n👤 *2* - Speak with Our Team\n🎉 *3* - Special Events & Celebrations\n\n_Reply with a number_",
        
        servicesMenu: "🏖️ *Our Ocean Activities*\n\n*1* 🐬 Dolphin Watching\n*2* 🪂 Parasailing\n*3* 🚤 Sea Trip\n*4* 🏄 Water Sports (Jet/Banana/Shuttle)\n*5* 🤿 Snorkeling Adventures\n*6* 💰 Payment Information\n\n*0* ⬅️ Back\n*9* 👤 Talk to Human\n\n_Choose an option:_",
        
        dolphinMenu: "🐬 *Dolphin Watching Tours*\n\n📸 _Experience magical moments with dolphins!_\n\n*Choose your tour:*\n\n*1* 🚢 *Private Boat Tour*\n   💰 60 OMR (up to 6 people)\n   ⏰ 8:00-10:00 AM\n   ⏰ 10:00 AM-12:00 PM\n   ⏰ 12:00-2:00 PM\n\n*2* 🛥️ *Public Boat Tour*\n   💰 10 OMR per person\n   ⏰ 8:00-10:00 AM\n   ⏰ 10:00 AM-12:00 PM\n\n📍 Marina Bandar Al-Rowdha\n\n*0* ⬅️ Back\n*9* 📞 Book Now",
        
        parasailingInfo: "🪂 *Parasailing Adventure*\n\n🦅 _Fly above the beautiful Omani coast!_\n\n💰 *Price:* 18 OMR per person\n⏱️ *Duration:* 30-40 minutes\n👥 *Capacity:* Depends on boat passengers (min 20 min)\n⚖️ *Max Weight:* 200 KG\n⏰ *Timing:* 8 AM until sunset\n\n⚠️ *Important:* Must book in advance on WhatsApp\n\n📍 Marina Bandar Al-Rowdha\n\n*0* ⬅️ Back\n*9* 📞 Book Now",
        
        seaTripInfo: "🚤 *Sea Trip Experience*\n\n🌊 _60-minute ocean journey with refreshments!_\n\n*Boat Options:*\n\n🛥️ *Capacity 5 people*\n   💰 Price varies by group\n   ⏱️ 60 minutes\n   🥤 Juice & Water included\n\n🚢 *Capacity 12 people*\n   💰 Price varies by group\n   ⏱️ 60 minutes\n   🥤 Juice & Water included\n\n⏰ *Timing:* 8 AM until sunset\n📍 Marina Bandar Al-Rowdha\n\n*0* ⬅️ Back\n*9* 📞 Book Now",
        
        waterSportsMenu: "🏄 *Water Sports Activities*\n\n*1* 🏍️ *Crazy Jet Boat*\n   💰 15 OMR/person\n   ⏱️ 15 minutes\n   👥 Max 10 people\n\n*2* 🚤 *Shuttle Boating*\n   💰 10 OMR/person\n   ⏱️ 15 minutes\n   👥 Max 4 people\n\n*3* 🍌 *Banana Boat*\n   💰 10 OMR/person\n   ⏱️ 15 minutes\n   👥 Max 8 people\n\n⏰ *Timing:* 8 AM until sunset\n\n*0* ⬅️ Back\n*9* 📞 Book Now",
        
        snorkelingMenu: "🤿 *Snorkeling Adventures*\n\n*1* 🐠 *Snorkeling Only*\n   💰 12 OMR/person\n   ⏱️ 50-80 minutes\n   👥 Max 6 people\n\n*2* 🐬 *Snorkeling + Dolphin Watching*\n   💰 18 OMR/person\n   ⏱️ 150-180 minutes (2.5-3 hours)\n   👥 Max 6 people\n   ⏰ 8-11 AM | 11 AM-1 PM\n\n🌊 _Explore the underwater beauty of Oman!_\n\n*0* ⬅️ Back\n*9* 📞 Book Now",
        
        specialEventsInfo: "🎉 *Special Events & Celebrations*\n\n✨ _Make your special moments unforgettable!_\n\nWe organize:\n\n🎂 *Birthday Parties*\n💑 *Anniversary Celebrations*\n🎊 *Private Events*\n🏖️ *Beach Parties*\n👨‍👩‍👧‍👦 *Family Gatherings*\n\n🎨 *Customizable Themes:*\n   • Choose your color scheme\n   • Personalized decorations\n   • Special arrangements\n   • Catering options\n   • Photography services\n\n💰 *Pricing:* Custom quotes based on your needs\n\n📞 *Contact us to plan your dream event!*\n\n*0* ⬅️ Back\n*9* 📞 Speak with Event Planner",
        
        paymentInfo: "💳 *Payment Information*\n\n🏦 *Bank Transfer:*\n   Bank: Muscat Bank\n   Account Name: ALHAMS ALAZRAQ LLC\n   IBAN: 0319049638080027\n\n📱 *Muscat Bank Mobile Payment:*\n   Account: 71902763\n   Name: Mohsen Amiri\n\n💵 *Cash Payment:*\n   Pay at Marina Bandar Al-Rowdha\n\n✅ *After payment, send receipt to:*\n   📞 +968-91220955\n   📞 +968-91142192\n\n*0* ⬅️ Back to Menu",
        
        bookingInfo: "📞 *Ready to Book?*\n\n*Contact us on WhatsApp:*\n📱 +968-91220955\n📱 +968-91142192\n\n*Direct WhatsApp Links:*\n🔗 https://wa.me/96891220955\n🔗 https://wa.me/96891142192\n\n📍 *Location:*\nMarina Bandar Al-Rowdha, Muscat\n\n⏰ *Operating Hours:*\n8:00 AM - Sunset (Daily)\n\n✨ _We look forward to serving you!_\n\n*0* ⬅️ Back to Menu",
        
        humanHandoff: "✅ *Connecting you to our team...*\n\n👨‍💼 One of our staff members will respond shortly.\n\n📞 *Or call us directly:*\n   +968-91220955\n   +968-91142192\n\n⏰ We respond within minutes during operating hours!\n\n_Type *MENU* anytime to return to automated service._",
        
        thankYou: "🙏 *Thank you for choosing Blue Whisper!*\n\n🌊 _We can't wait to welcome you!_\n\nType *MENU* to start over.",
        
        invalid: "❌ Invalid option. Please try again."
    },
    
    ar: {
        welcome: "🌊 *مرحباً بكم في نادي بلو ويسبر البحري!* 🌊\n\n✨ _وجهتكم المميزة للمغامرات البحرية في عمان_ ✨\n\nاستمتعوا بجمال المحيط مع أنشطتنا ذات المستوى العالمي!\n\n📍 مارينا بندر الروضة، مسقط\n\n",
        
        mainChoice: "*كيف تريد المتابعة؟*\n\n🤖 *1* - تصفح الخدمات (آلي)\n👤 *2* - التحدث مع فريقنا\n🎉 *3* - المناسبات والاحتفالات الخاصة\n\n_أرسل رقماً_",
        
        servicesMenu: "🏖️ *أنشطتنا البحرية*\n\n*1* 🐬 مشاهدة الدلافين\n*2* 🪂 الطيران الشراعي\n*3* 🚤 رحلة بحرية\n*4* 🏄 الرياضات المائية\n*5* 🤿 مغامرات الغوص\n*6* 💰 معلومات الدفع\n\n*0* ⬅️ رجوع\n*9* 👤 التحدث مع شخص\n\n_اختر خياراً:_",
        
        dolphinMenu: "🐬 *جولات مشاهدة الدلافين*\n\n📸 _عيش لحظات سحرية مع الدلافين!_\n\n*اختر جولتك:*\n\n*1* 🚢 *قارب خاص*\n   💰 60 ريال (حتى 6 أشخاص)\n   ⏰ 8:00-10:00 صباحاً\n   ⏰ 10:00-12:00 ظهراً\n   ⏰ 12:00-2:00 مساءً\n\n*2* 🛥️ *قارب عام*\n   💰 10 ريال للشخص\n   ⏰ 8:00-10:00 صباحاً\n   ⏰ 10:00-12:00 ظهراً\n\n📍 مارينا بندر الروضة\n\n*0* ⬅️ رجوع\n*9* 📞 احجز الآن",
        
        parasailingInfo: "🪂 *مغامرة الطيران الشراعي*\n\n🦅 _حلق فوق ساحل عمان الجميل!_\n\n💰 *السعر:* 18 ريال للشخص\n⏱️ *المدة:* 30-40 دقيقة\n👥 *السعة:* حسب ركاب القارب (20 دقيقة كحد أدنى)\n⚖️ *الوزن الأقصى:* 200 كجم\n⏰ *التوقيت:* من 8 صباحاً حتى الغروب\n\n⚠️ *مهم:* يجب الحجز مسبقاً عبر واتساب\n\n📍 مارينا بندر الروضة\n\n*0* ⬅️ رجوع\n*9* 📞 احجز الآن",
        
        seaTripInfo: "🚤 *تجربة الرحلة البحرية*\n\n🌊 _رحلة بحرية لمدة 60 دقيقة مع المرطبات!_\n\n*خيارات القوارب:*\n\n🛥️ *سعة 5 أشخاص*\n   💰 السعر يختلف حسب المجموعة\n   ⏱️ 60 دقيقة\n   🥤 عصير وماء متضمن\n\n🚢 *سعة 12 شخص*\n   💰 السعر يختلف حسب المجموعة\n   ⏱️ 60 دقيقة\n   🥤 عصير وماء متضمن\n\n⏰ *التوقيت:* من 8 صباحاً حتى الغروب\n📍 مارينا بندر الروضة\n\n*0* ⬅️ رجوع\n*9* 📞 احجز الآن",
        
        waterSportsMenu: "🏄 *أنشطة الرياضات المائية*\n\n*1* 🏍️ *قارب جت المجنون*\n   💰 15 ريال/شخص\n   ⏱️ 15 دقيقة\n   👥 حتى 10 أشخاص\n\n*2* 🚤 *القارب المكوكي*\n   💰 10 ريال/شخص\n   ⏱️ 15 دقيقة\n   👥 حتى 4 أشخاص\n\n*3* 🍌 *قارب الموز*\n   💰 10 ريال/شخص\n   ⏱️ 15 دقيقة\n   👥 حتى 8 أشخاص\n\n⏰ *التوقيت:* من 8 صباحاً حتى الغروب\n\n*0* ⬅️ رجوع\n*9* 📞 احجز الآن",
        
        snorkelingMenu: "🤿 *مغامرات الغوص*\n\n*1* 🐠 *الغوص فقط*\n   💰 12 ريال/شخص\n   ⏱️ 50-80 دقيقة\n   👥 حتى 6 أشخاص\n\n*2* 🐬 *الغوص + مشاهدة الدلافين*\n   💰 18 ريال/شخص\n   ⏱️ 150-180 دقيقة (2.5-3 ساعات)\n   👥 حتى 6 أشخاص\n   ⏰ 8-11 صباحاً | 11 صباحاً-1 ظهراً\n\n🌊 _استكشف الجمال تحت الماء في عمان!_\n\n*0* ⬅️ رجوع\n*9* 📞 احجز الآن",
        
        specialEventsInfo: "🎉 *المناسبات والاحتفالات الخاصة*\n\n✨ _اجعل لحظاتك الخاصة لا تُنسى!_\n\nننظم:\n\n🎂 *حفلات أعياد الميلاد*\n💑 *احتفالات الذكرى السنوية*\n🎊 *المناسبات الخاصة*\n🏖️ *حفلات الشاطئ*\n👨‍👩‍👧‍👦 *التجمعات العائلية*\n\n🎨 *ثيمات قابلة للتخصيص:*\n   • اختر نظام الألوان الخاص بك\n   • ديكورات شخصية\n   • ترتيبات خاصة\n   • خيارات الطعام\n   • خدمات التصوير\n\n💰 *التسعير:* عروض مخصصة حسب احتياجاتك\n\n📞 *اتصل بنا لتخطيط حدثك المثالي!*\n\n*0* ⬅️ رجوع\n*9* 📞 التحدث مع منظم المناسبات",
        
        paymentInfo: "💳 *معلومات الدفع*\n\n🏦 *التحويل البنكي:*\n   البنك: بنك مسقط\n   اسم الحساب: ALHAMS ALAZRAQ LLC\n   IBAN: 0319049638080027\n\n📱 *الدفع عبر موبايل بنك مسقط:*\n   الحساب: 71902763\n   الاسم: محسن أميري\n\n💵 *الدفع النقدي:*\n   ادفع في مارينا بندر الروضة\n\n✅ *بعد الدفع، أرسل الإيصال إلى:*\n   📞 +968-91220955\n   📞 +968-91142192\n\n*0* ⬅️ رجوع للقائمة",
        
        bookingInfo: "📞 *جاهز للحجز؟*\n\n*اتصل بنا على واتساب:*\n📱 +968-91220955\n📱 +968-91142192\n\n*روابط واتساب المباشرة:*\n🔗 https://wa.me/96891220955\n🔗 https://wa.me/96891142192\n\n📍 *الموقع:*\nمارينا بندر الروضة، مسقط\n\n⏰ *ساعات العمل:*\n8:00 صباحاً - الغروب (يومياً)\n\n✨ _نتطلع لخدمتكم!_\n\n*0* ⬅️ رجوع للقائمة",
        
        humanHandoff: "✅ *جاري توصيلك بفريقنا...*\n\n👨‍💼 سيرد عليك أحد موظفينا قريباً.\n\n📞 *أو اتصل بنا مباشرة:*\n   +968-91220955\n   +968-91142192\n\n⏰ نرد خلال دقائق أثناء ساعات العمل!\n\n_اكتب *MENU* في أي وقت للعودة للخدمة الآلية._",
        
        thankYou: "🙏 *شكراً لاختياركم بلو ويسبر!*\n\n🌊 _في انتظار استقبالكم!_\n\nاكتب *MENU* للبدء من جديد.",
        
        invalid: "❌ خيار غير صحيح. حاول مرة أخرى."
    }
};

function handleMessage(userId, message) {
    const input = message.trim().toLowerCase();
    
    // Return to menu from human mode
    if (input === 'menu' && humanMode[userId]) {
        delete humanMode[userId];
        userStates[userId] = 'services';
        const lang = userLanguages[userId] || 'en';
        return messages[lang].servicesMenu;
    }
    
    // In human mode - don't respond
    if (humanMode[userId]) {
        return null;
    }
    
    // New user
    if (!userStates[userId]) {
        userStates[userId] = 'language';
        userLanguages[userId] = 'en';
        return messages.en.welcome + "*Select Language / اختر اللغة:*\n\n*1* - English 🇬🇧\n*2* - العربية 🇴🇲";
    }
    
    const lang = userLanguages[userId];
    const state = userStates[userId];
    
    // Language selection
    if (state === 'language') {
        if (input === '1') {
            userLanguages[userId] = 'en';
            userStates[userId] = 'main_choice';
            return messages.en.mainChoice;
        } else if (input === '2') {
            userLanguages[userId] = 'ar';
            userStates[userId] = 'main_choice';
            return messages.ar.mainChoice;
        }
        return messages[lang].invalid;
    }
    
    // Main choice
    if (state === 'main_choice') {
        if (input === '1') {
            userStates[userId] = 'services';
            return messages[lang].servicesMenu;
        } else if (input === '2') {
            humanMode[userId] = true;
            return messages[lang].humanHandoff;
        } else if (input === '3') {
            userStates[userId] = 'special_events';
            return messages[lang].specialEventsInfo;
        }
        return messages[lang].invalid + '\n\n' + messages[lang].mainChoice;
    }
    
    // Services menu
    if (state === 'services') {
        if (input === '1') {
            userStates[userId] = 'dolphin';
            return messages[lang].dolphinMenu;
        } else if (input === '2') {
            userStates[userId] = 'parasailing';
            return messages[lang].parasailingInfo;
        } else if (input === '3') {
            userStates[userId] = 'sea_trip';
            return messages[lang].seaTripInfo;
        } else if (input === '4') {
            userStates[userId] = 'water_sports';
            return messages[lang].waterSportsMenu;
        } else if (input === '5') {
            userStates[userId] = 'snorkeling';
            return messages[lang].snorkelingMenu;
        } else if (input === '6') {
            return messages[lang].paymentInfo;
        } else if (input === '0') {
            userStates[userId] = 'main_choice';
            return messages[lang].mainChoice;
        } else if (input === '9') {
            humanMode[userId] = true;
            return messages[lang].humanHandoff;
        }
        return messages[lang].invalid + '\n\n' + messages[lang].servicesMenu;
    }
    
    // Dolphin menu
    if (state === 'dolphin' || state === 'parasailing' || state === 'sea_trip' || state === 'water_sports' || state === 'snorkeling' || state === 'special_events') {
        if (input === '0') {
            userStates[userId] = 'services';
            return messages[lang].servicesMenu;
        } else if (input === '9') {
            return messages[lang].bookingInfo;
        }
        return messages[lang].invalid;
    }
    
    return messages[lang].invalid;
}

async function startWhatsAppBot() {
    const { state, saveCreds } = await useMultiFileAuthState('auth_info_baileys');

    const sock = makeWASocket({
        auth: state,
        printQRInTerminal: false
    });

    sock.ev.on('creds.update', saveCreds);

    sock.ev.on('connection.update', (update) => {
        const { connection, lastDisconnect, qr } = update;

        if (qr) {
            console.log('\n🌊 Blue Whisper WhatsApp Bot - Scan QR Code:\n');
            qrcode.generate(qr, { small: true });
            console.log('\n📱 Open WhatsApp → Settings → Linked Devices → Link Device\n');
        }

        if (connection === 'close') {
            const shouldReconnect = lastDisconnect?.error?.output?.statusCode !== DisconnectReason.loggedOut;
            if (shouldReconnect) {
                setTimeout(startWhatsAppBot, 5000);
            }
        } else if (connection === 'open') {
            console.log('\n✅ WhatsApp Bot Connected!');
            console.log('🌊 Blue Whisper Ocean Club - LIVE');
            console.log('📍 Marina Bandar Al-Rowdha');
            console.log('🎯 All services active\n');
        }
    });

    sock.ev.on('messages.upsert', async ({ messages: msgs }) => {
        const msg = msgs[0];
        if (!msg.message || msg.key.fromMe) return;

        const userId = msg.key.remoteJid;
        const messageText = msg.message.conversation || msg.message.extendedTextMessage?.text || '';
        if (!messageText) return;

        const userName = msg.pushName || userId.split('@')[0];
        console.log(`📩 ${userName}: ${messageText}`);

        try {
            const response = handleMessage(userId, messageText);
            
            if (response === null) {
                console.log(`👤 [HUMAN MODE] ${userName} - Manual response needed\n`);
                return;
            }
            
            if (response) {
                await sock.sendMessage(userId, { text: response });
                console.log(`✅ Replied to ${userName}\n`);
            }
        } catch (error) {
            console.error('❌ Error:', error.message);
        }
    });
}

console.log('🚀 Starting Blue Whisper WhatsApp Bot...\n');
console.log('📊 Services loaded:');
console.log('   🐬 Dolphin Watching');
console.log('   🪂 Parasailing');
console.log('   🚤 Sea Trips');
console.log('   🏄 Water Sports');
console.log('   🤿 Snorkeling');
console.log('   🎉 Special Events\n');

startWhatsAppBot().catch(err => console.error('Error:', err));