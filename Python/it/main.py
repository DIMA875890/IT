import telebot
from telebot import types
from deep_translator import GoogleTranslator
from gtts import gTTS
import os
from database import init_db, add_translation

TOKEN = '8663400990:AAEvDb26CRZZbTM4hnz3q3AJNNCLA2Vuvmw'
bot = telebot.TeleBot(TOKEN)

user_prefs = {}

LANG_NAMES = {
    'en': 'English', 'ru': 'Russian', 'de': 'German',
    'fr': 'French', 'es': 'Spanish', 'it': 'Italian',
    'zh-CN': 'Chinese', 'ja': 'Japanese', 'tr': 'Turkish',
    'ar': 'Arabic', 'ko': 'Korean', 'pl': 'Polish'
}

LANGS = {
    '🇬🇧 English': 'en', '🇷🇺 Russian': 'ru', '🇩🇪 German': 'de',
    '🇫🇷 French': 'fr', '🇪🇸 Spanish': 'es', '🇮🇹 Italian': 'it',
    '🇨🇳 Chinese': 'zh-CN', '🇯🇵 Japanese': 'ja', '🇹🇷 Turkish': 'tr',
    '🇦🇪 Arabic': 'ar', '🇰🇷 Korean': 'ko', '🇵🇱 Polish': 'pl'
}

init_db()

def get_langs_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    buttons = [types.InlineKeyboardButton(text=name, callback_data=code) for name, code in LANGS.items()]
    markup.add(*buttons)
    return markup

def get_restart_keyboard():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text="🔄 Menu", callback_data="go_start"))
    return markup

@bot.message_handler(commands=['start', 'settings'])
def start(message):
    bot.send_message(
        message.chat.id, 
        "<b>🌍 Select Language:</b>", 
        reply_markup=get_langs_keyboard(),
        parse_mode="HTML"
    )

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == "go_start":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "<b>🌍 Select Language:</b>", reply_markup=get_langs_keyboard(), parse_mode="HTML")
        return

    lang_code = call.data
    user_prefs[call.from_user.id] = lang_code
    bot.answer_callback_query(call.id)
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="<b>Ready! Send text to translate.</b>",
        parse_mode="HTML"
    )

@bot.message_handler(func=lambda message: True)
def handle_translate(message):
    user_id = message.from_user.id
    target_lang = user_prefs.get(user_id, 'en')
    
    try:
        translated_text = GoogleTranslator(source='auto', target=target_lang).translate(message.text)
        add_translation(user_id, message.text, translated_text, target_lang)
        
        tts = gTTS(text=translated_text, lang=target_lang)
        audio_file = f"voice_{user_id}.mp3"
        tts.save(audio_file)
        
        display_name = LANG_NAMES.get(target_lang, target_lang)
        styled_response = f"<b>{display_name}:</b>\n{translated_text}"
        
        bot.send_message(message.chat.id, styled_response, parse_mode="HTML")
        
        with open(audio_file, 'rb') as audio:
            bot.send_voice(message.chat.id, audio, reply_markup=get_restart_keyboard())
            
        os.remove(audio_file)
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    bot.infinity_polling()