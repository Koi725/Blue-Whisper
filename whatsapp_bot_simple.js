const { default: makeWASocket, DisconnectReason, useMultiFileAuthState } = require('@whiskeysockets/baileys');
const qrcode = require('qrcode-terminal');

// Store user states
const userStates = {};
const userLanguages = {};
const humanMode = {}; // Track who wants human support

// Translations
const messages = {
    en: {
        welcome: "🌊 *Welcome to Blue Whisper Ocean Club!* 🌊\n\nYour Premium Ocean Adventure Destination in Oman\n\n",
        firstMenu: "How can I help you today?\n\n🤖 *1* - General Information (Automated)\n👤 *2* - Speak with Our Team\n\nReply with *1* or *2*",
        humanHandoff: "✅ *Connecting you to our team...*\n\nOne of our staff members will respond to you shortly.\n\nThank you for your patience! 🙏",
        backToBot: "Type *MENU* anytime to return to automated service.",
        selectLanguage: "Please select your language:\n*1* - English 🇬🇧\n*2* - العربية 🇴🇲",
        mainMenu: "🏖️ *Main Menu*\n\n*1* - 🎯 Our Services & Pricing\n*2* - 📞 Make a Reservation\n*3* - 📱 Social Media\n*0* - 👤 Talk to Human\n\nReply with number:",
        services: "🎯 *Our Services & Pricing*\n\n*1* - Jet Ski\n   💰 OMR 25.00 | ⏱️ 30 min\n\n*2* - Parasailing\n   💰 OMR 35.00 | ⏱️ 15 min\n\n*3* - Banana Boat\n   💰 OMR 15.00 | ⏱️ 20 min\n\n*4* - Snorkeling\n   💰 OMR 20.00 | ⏱️ 1 hour\n\n*5* - Kayaking\n   💰 OMR 18.00 | ⏱️ 1 hour\n\n*6* - Diving Experience\n   💰 OMR 50.00 | ⏱️ 2 hours\n\n*0* - ⬅️ Back to Menu",
        reservation: "📞 *Make a Reservation*\n\nContact us on WhatsApp:\n📱 +968-9123-4567\n\n🔗 https://wa.me/96891234567\n\n*0* - ⬅️ Back to Menu",
        social: "📱 *Connect With Us*\n\nFollow us for updates and special offers!\n\n📘 Facebook: facebook.com/bluewhisperoman\n📸 Instagram: instagram.com/bluewhisperoman\n🐦 Twitter: twitter.com/bluewhisperoman\n✉️ Email: info@bluewhisper.om\n\n*0* - ⬅️ Back to Menu",
        invalid: "❌ Invalid option. Please try again."
    },
    ar: {
        welcome: "🌊 *مرحباً بكم في نادي بلو ويسبر البحري!* 🌊\n\nوجهتكم المميزة للمغامرات البحرية في عمان\n\n",
        firstMenu: "كيف يمكنني مساعدتك اليوم؟\n\n🤖 *1* - معلومات عامة (آلي)\n👤 *2* - التحدث مع فريقنا\n\nأرسل *1* أو *2*",
        humanHandoff: "✅ *جاري توصيلك بفريقنا...*\n\nسيرد عليك أحد موظفينا قريباً.\n\nشكراً لصبرك! 🙏",
        backToBot: "اكتب *MENU* في أي وقت للعودة إلى الخدمة الآلية.",
        selectLanguage: "الرجاء اختيار لغتك:\n*1* - English 🇬🇧\n*2* - العربية 🇴🇲",
        mainMenu: "🏖️ *القائمة الرئيسية*\n\n*1* - 🎯 خدماتنا وأسعارنا\n*2* - 📞 حجز موعد\n*3* - 📱 وسائل التواصل\n*0* - 👤 التحدث مع شخص\n\nأرسل الرقم:",
        services: "🎯 *خدماتنا وأسعارنا*\n\n*1* - جت سكي\n   💰 25.00 OMR | ⏱️ 30 دقيقة\n\n*2* - الطيران الشراعي\n   💰 35.00 OMR | ⏱️ 15 دقيقة\n\n*3* - قارب الموز\n   💰 15.00 OMR | ⏱️ 20 دقيقة\n\n*4* - الغوص بالأنبوب\n   💰 20.00 OMR | ⏱️ ساعة واحدة\n\n*5* - التجديف\n   💰 18.00 OMR | ⏱️ ساعة واحدة\n\n*6* - تجربة الغوص\n   💰 50.00 OMR | ⏱️ ساعتان\n\n*0* - ⬅️ العودة للقائمة",
        reservation: "📞 *حجز موعد*\n\nاتصل بنا على واتساب:\n📱 +968-9123-4567\n\n🔗 https://wa.me/96891234567\n\n*0* - ⬅️ العودة للقائمة",
        social: "📱 *تواصل معنا*\n\nتابعنا للحصول على التحديثات والعروض الخاصة!\n\n📘 فيسبوك: facebook.com/bluewhisperoman\n📸 إنستغرام: instagram.com/bluewhisperoman\n🐦 تويتر: twitter.com/bluewhisperoman\n✉️ البريد: info@bluewhisper.om\n\n*0* - ⬅️ العودة للقائمة",
        invalid: "❌ خيار غير صحيح. حاول مرة أخرى."
    }
};

function handleMessage(userId, message) {
    const input = message.trim().toLowerCase();
    
    // Check if user wants to return to bot from human mode
    if (input === 'menu' && humanMode[userId]) {
        delete humanMode[userId];
        userStates[userId] = 'main';
        const lang = userLanguages[userId] || 'en';
        return messages[lang].mainMenu;
    }
    
    // If in human mode, ignore (let human respond)
    if (humanMode[userId]) {
        return null; // Don't respond, leave for human
    }
    
    // Initialize new user
    if (!userStates[userId]) {
        userStates[userId] = 'first_choice';
        userLanguages[userId] = 'en';
        return messages.en.welcome + messages.en.firstMenu;
    }
    
    const lang = userLanguages[userId];
    const state = userStates[userId];
    
    // First choice: Bot or Human
    if (state === 'first_choice') {
        if (input === '1') {
            userStates[userId] = 'language';
            return messages[lang].selectLanguage;
        } else if (input === '2') {
            humanMode[userId] = true;
            userStates[userId] = 'human';
            return messages[lang].humanHandoff + '\n\n' + messages[lang].backToBot;
        }
        return messages[lang].invalid + '\n\n' + messages[lang].firstMenu;
    }
    
    // Language selection
    if (state === 'language') {
        if (input === '1') {
            userLanguages[userId] = 'en';
            userStates[userId] = 'main';
            return messages.en.mainMenu;
        } else if (input === '2') {
            userLanguages[userId] = 'ar';
            userStates[userId] = 'main';
            return messages.ar.mainMenu;
        }
        return messages[lang].invalid + '\n\n' + messages[lang].selectLanguage;
    }
    
    // Main menu
    if (state === 'main') {
        if (input === '1') {
            userStates[userId] = 'services';
            return messages[lang].services;
        } else if (input === '2') {
            userStates[userId] = 'reservation';
            return messages[lang].reservation;
        } else if (input === '3') {
            userStates[userId] = 'social';
            return messages[lang].social;
        } else if (input === '0') {
            humanMode[userId] = true;
            userStates[userId] = 'human';
            return messages[lang].humanHandoff + '\n\n' + messages[lang].backToBot;
        }
        return messages[lang].invalid + '\n\n' + messages[lang].mainMenu;
    }
    
    // Services menu
    if (state === 'services') {
        if (input === '0') {
            userStates[userId] = 'main';
            return messages[lang].mainMenu;
        } else if (['1','2','3','4','5','6'].includes(input)) {
            userStates[userId] = 'reservation';
            return messages[lang].reservation;
        }
        return messages[lang].invalid + '\n\n' + messages[lang].services;
    }
    
    // Reservation/Social - back to main
    if (state === 'reservation' || state === 'social') {
        if (input === '0') {
            userStates[userId] = 'main';
            return messages[lang].mainMenu;
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
            console.log('\n🌊 Blue Whisper WhatsApp Bot - Scan this QR Code:\n');
            qrcode.generate(qr, { small: true });
            console.log('\n📱 Open WhatsApp → Settings → Linked Devices → Link a Device\n');
        }

        if (connection === 'close') {
            const shouldReconnect = lastDisconnect?.error?.output?.statusCode !== DisconnectReason.loggedOut;
            console.log('⚠️ Connection closed. Reconnecting...', shouldReconnect);
            if (shouldReconnect) {
                setTimeout(startWhatsAppBot, 5000);
            }
        } else if (connection === 'open') {
            console.log('\n✅ WhatsApp Bot Connected!');
            console.log('🌊 Blue Whisper Ocean Club WhatsApp Bot is LIVE!');
            console.log('🤖 Automatic replies enabled');
            console.log('👤 Human handoff available\n');
        }
    });

    sock.ev.on('messages.upsert', async ({ messages }) => {
        const msg = messages[0];

        if (!msg.message || msg.key.fromMe) return;

        const userId = msg.key.remoteJid;
        const messageText = msg.message.conversation || 
                           msg.message.extendedTextMessage?.text || '';

        if (!messageText) return;

        const userName = msg.pushName || userId.split('@')[0];

        console.log(`📩 ${userName}: ${messageText}`);

        try {
            const response = handleMessage(userId, messageText);
            
            if (response === null) {
                // User is in human mode - don't respond
                console.log(`👤 [HUMAN MODE] Message from ${userName} - waiting for manual reply\n`);
                return;
            }
            
            if (response) {
                await sock.sendMessage(userId, { text: response });
                
                if (humanMode[userId]) {
                    console.log(`👤 [HANDED OFF] ${userName} is now in human support mode\n`);
                } else {
                    console.log(`🤖 [BOT] Auto-replied to ${userName}\n`);
                }
            }
        } catch (error) {
            console.error('❌ Error:', error.message);
        }
    });
}

console.log('🚀 Starting Blue Whisper WhatsApp Bot with Human Handoff...\n');
startWhatsAppBot().catch(err => console.error('Error:', err));