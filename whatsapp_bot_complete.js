const { default: makeWASocket, DisconnectReason, useMultiFileAuthState } = require('@whiskeysockets/baileys');
const qrcode = require('qrcode-terminal');
const fs = require('fs');
const path = require('path');

// User states
const userStates = {};
const userLanguages = {};
const humanMode = {};

// Service images paths
const serviceImages = {
    dolphin: path.join(__dirname, 'images', 'dolphin.jpg'),
    parasailing: path.join(__dirname, 'images', 'parasailing.jpg'),
    seaTrip: path.join(__dirname, 'images', 'sea_trip.jpg'),
    waterSports: path.join(__dirname, 'images', 'water_sports.jpg'),
    snorkeling: path.join(__dirname, 'images', 'snorkeling.jpg'),
    events: path.join(__dirname, 'images', 'events.jpg')
};

const messages = {
    en: {
        welcome: "🌊 *Welcome to Blue Whisper Ocean Club!* 🌊\n\n✨ _Your Premium Ocean Adventure in Oman_ ✨\n\nExperience the beauty of the ocean with our world-class activities!\n\n📍 Marina Bandar Al-Rowdha, Muscat\n🌐 www.muscatjoy.com\n\n",
        
        mainChoice: "*How would you like to proceed?*\n\n🤖 *1* - Browse Services (Automated)\n👤 *2* - Speak with Our Team\n🎉 *3* - Special Events & Celebrations\n\n_Reply with a number_",
        
        servicesMenu: "🏖️ *Our Ocean Activities*\n\n*1* 🐬 Dolphin Watching\n*2* 🪂 Parasailing\n*3* 🚤 Sea Trip\n*4* 🏄 Water Sports\n*5* 🤿 Snorkeling\n*6* 💰 Payment Information\n\n*0* ⬅️ Back\n*9* 👤 Talk to Human\n\n_Choose an option:_",
        
        dolphinInfo: "🐬 *Dolphin Watching Tours*\n\n📸 _Experience magical moments with dolphins!_\n\n🚢 *Private Boat Tour*\n💰 60 OMR (up to 6 people)\n⏰ 8:00-10:00 AM | 10:00 AM-12:00 PM | 12:00-2:00 PM\n\n🛥️ *Public Boat Tour*\n💰 10 OMR per person\n⏰ 8:00-10:00 AM | 10:00 AM-12:00 PM\n\n📍 Marina Bandar Al-Rowdha\n\n*0* ⬅️ Back | *9* 📞 Book Now",
        
        parasailingInfo: "🪂 *Parasailing Adventure*\n\n🦅 _Fly above the beautiful Omani coast!_\n\n💰 18 OMR per person\n⏱️ 30-40 minutes\n👥 Depends on boat passengers\n⚖️ Max Weight: 200 KG\n⏰ 8 AM - Sunset\n\n⚠️ *Must book in advance on WhatsApp*\n\n📍 Marina Bandar Al-Rowdha\n\n*0* ⬅️ Back | *9* 📞 Book Now",
        
        seaTripInfo: "🚤 *Sea Trip Experience*\n\n🌊 _60-minute ocean journey with refreshments!_\n\n🛥️ *Capacity 5 people* - 60 min + 🥤 Juice & Water\n🚢 *Capacity 12 people* - 60 min + 🥤 Juice & Water\n\n⏰ 8 AM - Sunset\n📍 Marina Bandar Al-Rowdha\n\n*0* ⬅️ Back | *9* 📞 Book Now",
        
        waterSportsInfo: "🏄 *Water Sports Activities*\n\n🏍️ *Crazy Jet Boat*\n💰 15 OMR/person | ⏱️ 15 min | 👥 Max 10\n\n🚤 *Shuttle Boating*\n💰 10 OMR/person | ⏱️ 15 min | 👥 Max 4\n\n🍌 *Banana Boat*\n💰 10 OMR/person | ⏱️ 15 min | 👥 Max 8\n\n⏰ 8 AM - Sunset\n📍 Marina Bandar Al-Rowdha\n\n*0* ⬅️ Back | *9* 📞 Book Now",
        
        snorkelingInfo: "🤿 *Snorkeling Adventures*\n\n🐠 *Snorkeling Only*\n💰 12 OMR/person | ⏱️ 50-80 min | 👥 Max 6\n\n🐬 *Snorkeling + Dolphin*\n💰 18 OMR/person | ⏱️ 150-180 min | 👥 Max 6\n⏰ 8-11 AM | 11 AM-1 PM\n\n🌊 _Explore underwater beauty!_\n\n*0* ⬅️ Back | *9* 📞 Book Now",
        
        eventsInfo: "🎉 *Special Events & Celebrations*\n\n✨ _Make your special moments unforgettable!_\n\nWe organize:\n🎂 Birthday Parties\n💑 Anniversary Celebrations\n🎊 Private Events\n🏖️ Beach Parties\n👨‍👩‍👧‍👦 Family Gatherings\n\n🎨 *Customizable Themes*\n• Color schemes\n• Personalized decorations\n• Catering options\n• Photography services\n\n📞 Contact us for custom quotes!\n\n*0* ⬅️ Back | *9* 📞 Speak with Event Planner",
        
        paymentInfo: "💳 *Payment Information*\n\n🏦 *Bank Transfer:*\nBank: Muscat Bank\nAccount: ALHAMS ALAZRAQ LLC\nIBAN: 0319049638080027\n\n📱 *Mobile Payment:*\nAccount: 71902763\nName: Mohsen Amiri\n\n💵 *Cash:* Pay at marina\n\n✅ Send receipt to:\n📞 +968-77752752\n📞 +968-91220956\n\n*0* ⬅️ Back",
        
        bookingInfo: "📞 *Ready to Book?*\n\n*Contact us:*\n📱 +968-77752752\n📱+968-91220956\n🌐 www.muscatjoy.com\n\n📍 Marina Bandar Al-Rowdha\n⏰ 8 AM - Sunset (Daily)\n\n✨ We look forward to serving you!\n\n*0* ⬅️ Back",
        
        humanHandoff: "✅ *Connecting to our team...*\n\n👨‍💼 A staff member will respond shortly.\n\n📞 *Direct contact:*\n+968-77752752\n+968-91220956\n🌐 www.muscatjoy.com\n\n⏰ Quick response during hours!\n\n_Type *MENU* to return to automated service._",
        
        invalid: "❌ Invalid option. Please try again."
    },
    
    ar: {
        welcome: "🌊 *مرحباً بكم في نادي بلو ويسبر البحري!* 🌊\n\n✨ _وجهتكم المميزة للمغامرات البحرية_ ✨\n\nاستمتعوا بجمال المحيط مع أنشطتنا!\n\n📍 مارينا بندر الروضة، مسقط\n🌐 www.muscatjoy.com\n\n",
        
        mainChoice: "*كيف تريد المتابعة؟*\n\n🤖 *1* - تصفح الخدمات (آلي)\n👤 *2* - التحدث مع فريقنا\n🎉 *3* - المناسبات الخاصة\n\n_أرسل رقماً_",
        
        servicesMenu: "🏖️ *أنشطتنا البحرية*\n\n*1* 🐬 مشاهدة الدلافين\n*2* 🪂 الطيران الشراعي\n*3* 🚤 رحلة بحرية\n*4* 🏄 الرياضات المائية\n*5* 🤿 الغوص\n*6* 💰 معلومات الدفع\n\n*0* ⬅️ رجوع\n*9* 👤 تحدث مع شخص\n\n_اختر خياراً:_",
        
        dolphinInfo: "🐬 *جولات مشاهدة الدلافين*\n\n📸 _عيش لحظات سحرية!_\n\n🚢 *قارب خاص*\n💰 60 ريال (حتى 6 أشخاص)\n⏰ 8-10 ص | 10-12 ظ | 12-2 م\n\n🛥️ *قارب عام*\n💰 10 ريال للشخص\n⏰ 8-10 ص | 10-12 ظ\n\n📍 مارينا بندر الروضة\n\n*0* ⬅️ رجوع | *9* 📞 احجز الآن",
        
        parasailingInfo: "🪂 *مغامرة الطيران الشراعي*\n\n🦅 _حلق فوق ساحل عمان!_\n\n💰 18 ريال للشخص\n⏱️ 30-40 دقيقة\n👥 حسب ركاب القارب\n⚖️ الوزن الأقصى: 200 كجم\n⏰ 8 صباحاً - الغروب\n\n⚠️ *يجب الحجز مسبقاً*\n\n📍 مارينا بندر الروضة\n\n*0* ⬅️ رجوع | *9* 📞 احجز الآن",
        
        seaTripInfo: "🚤 *تجربة الرحلة البحرية*\n\n🌊 _رحلة 60 دقيقة مع مرطبات!_\n\n🛥️ *سعة 5 أشخاص* - 60 دقيقة + 🥤 عصير وماء\n🚢 *سعة 12 شخص* - 60 دقيقة + 🥤 عصير وماء\n\n⏰ 8 صباحاً - الغروب\n📍 مارينا بندر الروضة\n\n*0* ⬅️ رجوع | *9* 📞 احجز الآن",
        
        waterSportsInfo: "🏄 *الرياضات المائية*\n\n🏍️ *قارب جت المجنون*\n💰 15 ريال/شخص | ⏱️ 15 دقيقة | 👥 حتى 10\n\n🚤 *القارب المكوكي*\n💰 10 ريال/شخص | ⏱️ 15 دقيقة | 👥 حتى 4\n\n🍌 *قارب الموز*\n💰 10 ريال/شخص | ⏱️ 15 دقيقة | 👥 حتى 8\n\n⏰ 8 صباحاً - الغروب\n📍 مارينا بندر الروضة\n\n*0* ⬅️ رجوع | *9* 📞 احجز الآن",
        
        snorkelingInfo: "🤿 *مغامرات الغوص*\n\n🐠 *الغوص فقط*\n💰 12 ريال/شخص | ⏱️ 50-80 دقيقة | 👥 حتى 6\n\n🐬 *الغوص + الدلافين*\n💰 18 ريال/شخص | ⏱️ 150-180 دقيقة | 👥 حتى 6\n⏰ 8-11 ص | 11 ص-1 ظ\n\n🌊 _استكشف الجمال تحت الماء!_\n\n*0* ⬅️ رجوع | *9* 📞 احجز الآن",
        
        eventsInfo: "🎉 *المناسبات الخاصة*\n\n✨ _اجعل لحظاتك لا تُنسى!_\n\nننظم:\n🎂 حفلات أعياد الميلاد\n💑 احتفالات الذكرى\n🎊 المناسبات الخاصة\n🏖️ حفلات الشاطئ\n👨‍👩‍👧‍👦 التجمعات العائلية\n\n🎨 *ثيمات مخصصة*\n• نظام الألوان\n• ديكورات شخصية\n• خيارات الطعام\n• خدمات التصوير\n\n📞 اتصل بنا للعروض!\n\n*0* ⬅️ رجوع | *9* 📞 تحدث مع منظم المناسبات",
        
        paymentInfo: "💳 *معلومات الدفع*\n\n🏦 *تحويل بنكي:*\nالبنك: بنك مسقط\nالحساب: ALHAMS ALAZRAQ LLC\nIBAN: 0319049638080027\n\n📱 *دفع موبايل:*\nالحساب: 71902763\nالاسم: محسن أميري\n\n💵 *نقدي:* ادفع في المارينا\n\n✅ أرسل الإيصال:\n📞 +968-77752752\n📞 +968-91220956\n\n*0* ⬅️ رجوع",
        
        bookingInfo: "📞 *جاهز للحجز؟*\n\n*اتصل بنا:*\n📱 +968-77752752\n📱+968-91220956\n🌐 www.muscatjoy.com\n\n📍 مارينا بندر الروضة\n⏰ 8 صباحاً - الغروب (يومياً)\n\n✨ نتطلع لخدمتكم!\n\n*0* ⬅️ رجوع",
        
        humanHandoff: "✅ *جاري التوصيل بفريقنا...*\n\n👨‍💼 سيرد عليك موظف قريباً.\n\n📞 *اتصال مباشر:*\n+968-77752752\n+968-91220956\n🌐 www.muscatjoy.com\n\n⏰ رد سريع أثناء ساعات العمل!\n\n_اكتب *MENU* للعودة للخدمة الآلية._",
        
        invalid: "❌ خيار غير صحيح. حاول مرة أخرى."
    }
};

async function sendImageWithCaption(sock, userId, imagePath, caption) {
    try {
        if (fs.existsSync(imagePath)) {
            const imageBuffer = fs.readFileSync(imagePath);
            await sock.sendMessage(userId, {
                image: imageBuffer,
                caption: caption
            });
            return true;
        } else {
            console.log(`⚠️ Image not found: ${imagePath}`);
            await sock.sendMessage(userId, { text: caption });
            return false;
        }
    } catch (error) {
        console.error(`❌ Error sending image: ${error.message}`);
        await sock.sendMessage(userId, { text: caption });
        return false;
    }
}

function handleMessage(userId, message) {
    const input = message.trim().toLowerCase();
    
    if (input === 'menu' && humanMode[userId]) {
        delete humanMode[userId];
        userStates[userId] = 'services';
        const lang = userLanguages[userId] || 'en';
        return { type: 'text', content: messages[lang].servicesMenu };
    }
    
    if (humanMode[userId]) {
        return null;
    }
    
    if (!userStates[userId]) {
        userStates[userId] = 'language';
        userLanguages[userId] = 'en';
        return { 
            type: 'text', 
            content: messages.en.welcome + "*Select Language / اختر اللغة:*\n\n*1* - English 🇬🇧\n*2* - العربية 🇴🇲" 
        };
    }
    
    const lang = userLanguages[userId];
    const state = userStates[userId];
    
    if (state === 'language') {
        if (input === '1') {
            userLanguages[userId] = 'en';
            userStates[userId] = 'main_choice';
            return { type: 'text', content: messages.en.mainChoice };
        } else if (input === '2') {
            userLanguages[userId] = 'ar';
            userStates[userId] = 'main_choice';
            return { type: 'text', content: messages.ar.mainChoice };
        }
        return { type: 'text', content: messages[lang].invalid };
    }
    
    if (state === 'main_choice') {
        if (input === '1') {
            userStates[userId] = 'services';
            return { type: 'text', content: messages[lang].servicesMenu };
        } else if (input === '2') {
            humanMode[userId] = true;
            return { type: 'text', content: messages[lang].humanHandoff };
        } else if (input === '3') {
            userStates[userId] = 'events';
            return { 
                type: 'image', 
                imagePath: serviceImages.events,
                content: messages[lang].eventsInfo 
            };
        }
        return { type: 'text', content: messages[lang].invalid + '\n\n' + messages[lang].mainChoice };
    }
    
    if (state === 'services') {
        if (input === '1') {
            return { 
                type: 'image', 
                imagePath: serviceImages.dolphin,
                content: messages[lang].dolphinInfo 
            };
        } else if (input === '2') {
            return { 
                type: 'image', 
                imagePath: serviceImages.parasailing,
                content: messages[lang].parasailingInfo 
            };
        } else if (input === '3') {
            return { 
                type: 'image', 
                imagePath: serviceImages.seaTrip,
                content: messages[lang].seaTripInfo 
            };
        } else if (input === '4') {
            return { 
                type: 'image', 
                imagePath: serviceImages.waterSports,
                content: messages[lang].waterSportsInfo 
            };
        } else if (input === '5') {
            return { 
                type: 'image', 
                imagePath: serviceImages.snorkeling,
                content: messages[lang].snorkelingInfo 
            };
        } else if (input === '6') {
            return { type: 'text', content: messages[lang].paymentInfo };
        } else if (input === '0') {
            userStates[userId] = 'main_choice';
            return { type: 'text', content: messages[lang].mainChoice };
        } else if (input === '9') {
            humanMode[userId] = true;
            return { type: 'text', content: messages[lang].humanHandoff };
        }
        return { type: 'text', content: messages[lang].invalid + '\n\n' + messages[lang].servicesMenu };
    }
    
    if (['events'].includes(state)) {
        if (input === '0') {
            userStates[userId] = 'main_choice';
            return { type: 'text', content: messages[lang].mainChoice };
        } else if (input === '9') {
            return { type: 'text', content: messages[lang].bookingInfo };
        }
        return { type: 'text', content: messages[lang].invalid };
    }
    
    return { type: 'text', content: messages[lang].invalid };
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
            console.log('🌐 www.muscatjoy.com');
            console.log('🎯 All services active');
            console.log('📸 Image sending enabled\n');
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
                if (response.type === 'image') {
                    const sent = await sendImageWithCaption(sock, userId, response.imagePath, response.content);
                    if (sent) {
                        console.log(`📸 [IMAGE] Sent to ${userName}\n`);
                    } else {
                        console.log(`✅ [TEXT] Replied to ${userName} (image not found)\n`);
                    }
                } else {
                    await sock.sendMessage(userId, { text: response.content });
                    console.log(`✅ [TEXT] Replied to ${userName}\n`);
                }
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
console.log('   🎉 Special Events');
console.log('\n📸 Image support: ENABLED');
console.log('🌐 Website: www.muscatjoy.com');
console.log('📞 Contact: +968-77752752\n');

startWhatsAppBot().catch(err => console.error('Error:', err));