import telebot
import sqlite3
from telebot import types
from datetime import datetime, timedelta
from flask import Flask
from threading import Thread
import time

# Bot Token (သေချာပြန်စစ်ပေးပါ)
TOKEN = '8242602571:AAFfOR9SmP6T5cc_YWoKt0tmJXpOa7VbmP4'
bot = telebot.TeleBot(TOKEN)

# --- Flask Server for Render Port Binding ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is Running!"

def run():
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- Database Functions ---
def init_db():
    try:
        conn = sqlite3.connect('bot_users.db', check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, join_date TEXT)')
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"DB Init Error: {e}")

def add_user(user_id):
    try:
        conn = sqlite3.connect('bot_users.db', check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute('SELECT user_id FROM users WHERE user_id = ?', (user_id,))
        if cursor.fetchone() is None:
            join_date = datetime.now().strftime('%Y-%m-%d')
            cursor.execute('INSERT INTO users (user_id, join_date) VALUES (?, ?)', (user_id, join_date))
            conn.commit()
        conn.close()
    except Exception as e:
        print(f"DB Add Error: {e}")

# --- Menu Design ---
def main_menu():
    welcome_text = """
<tg-emoji emoji-id="6238006042534353720">✨</tg-emoji> 👑 <b>Decentralized Store</b> 👑 <tg-emoji emoji-id="6238006042534353720">✨</tg-emoji>

📦 <b>Products</b> 👇
━━━━━━━━━━━━━━━━━━
🔹 Tiktok : Like | View | Follower
🔹 Facebook Profile & Page : Like | Follower
🔹 Facebook : Reaction | Reel View
🔹 Youtube : Subscriber | View | Like
🔹 Instagram : Reaction | Follower
🔹 Telegram : Subscriber | Member | View | Reaction

🎓 <b>Classes Available</b> 👇
━━━━━━━━━━━━━━━━━━
💰 5000ks Classes
▪ Premium Package တွေ ရောင်းနည်း
▪ Dia, UC, etc... ရောင်းနည်း
▪ Design & Logo ဆွဲနည်း

💰 15000ks Classes
▪ AI Movie Recap Class
▪ Like | View | Follower ထည့်နည်း
▪ TikTok အကောင့် Hack နည်း
▪ Telegram အကောင့် Hack နည်း

📩 စျေးနှုန်းညှိရန် & Class များတက်ရန်
Telegram DM 👉 @Decentralized34
    """
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton("🇯🇵 Japan Tiktok အကောင့် ဝယ်ရန်", callback_data="buy_tiktok")
    btn2 = types.InlineKeyboardButton("🎬 AI Movie Recap တက်ရန်", callback_data="ai_class")
    btn3 = types.InlineKeyboardButton("✈️ Telegram ဝန်ဆောင်မှုများ", callback_data="tg_service")
    btn4 = types.InlineKeyboardButton("💰 Payment အကောင့်များ", callback_data="payment")
    markup.add(btn1, btn2, btn3, btn4)
    return welcome_text, markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    add_user(message.from_user.id)
    text, markup = main_menu()
    bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode="HTML")

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    # Button နှိပ်လိုက်ရင် တုံ့ပြန်မှုမြန်အောင် အရင်ဆုံး Answer လုပ်ပေးရတယ်
    bot.answer_callback_query(call.id)
    
    back_markup = types.InlineKeyboardMarkup()
    back_btn = types.InlineKeyboardButton("🔙 မူလစာမျက်နှာသို့", callback_data="go_start")
    back_markup.add(back_btn)

    if call.data == "buy_tiktok":
        text = "🇯🇵 <b>Japan TikTok အကောင့် ဝယ်ယူရန်</b>\n\n💰 စျေးနှုန်း - တစ်ကောင့်လျှင် <b>5000ks</b>\n\n📩 လိုချင်ပါက Telegram DM 👉 @Decentralized34\n💸 ငွေလွဲပြီးနောက် Screenshot ပို့ပေးပါ။"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=back_markup, parse_mode="HTML")
        
    elif call.data == "ai_class":
        text = "🎬 <b>AI Movie Recap Class တက်ရောက်ရန်</b>\n\n✅ Acc ရှိ - <b>15000ks</b>\n❌ Acc မရှိ - <b>20000ks</b>\n\n📩 လိုချင်ပါက Telegram DM 👉 @Decentralized34\n💸 ငွေလွဲပြီးနောက် Screenshot ပို့ပေးပါ။"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=back_markup, parse_mode="HTML")

    elif call.data == "tg_service":
        text = "✈️ <b>Telegram ဝန်ဆောင်မှုများ</b>\n\n🔹 Telegram Account အသစ် - <b>5000ks</b>\n🔹 Telegram SMS Fee - <b>10000ks</b>\n\n📩 လိုချင်ပါက Telegram DM 👉 @Decentralized34"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=back_markup, parse_mode="HTML")

    elif call.data == "payment":
        payment_info = """
<tg-emoji emoji-id="6237668552594167846">💰</tg-emoji> <b>Payment Methods</b> <tg-emoji emoji-id="6237668552594167846">💰</tg-emoji>
━━━━━━━━━━━━━━━━━━
<tg-emoji emoji-id="6237668552594167846">💸</tg-emoji> <b>Kpay</b>
09883363434
Daw moe moe lwin

<tg-emoji emoji-id="6237668552594167846">💸</tg-emoji> <b>Wave Pay</b>
09883363434
Daw moe moe lwin

<tg-emoji emoji-id="6237668552594167846">💸</tg-emoji> <b>Uab Pay</b>
09883363434
Maung Maung

⚠️ <b>မှတ်ချက်</b> - ငွေလွဲပြီးပါက Screenshot ပြရန် မမေ့ပါနှင့်။
        """
        bot.edit_message_text(payment_info, call.message.chat.id, call.message.message_id, reply_markup=back_markup, parse_mode="HTML")

    elif call.data == "go_start":
        text, markup = main_menu()
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="HTML")

if __name__ == "__main__":
    init_db()
    keep_alive()
    print("Bot is starting with Port 10000...")
    # Polling ကို ပိုစိတ်ချရအောင် infinity_polling သုံးထားတယ်
    bot.infinity_polling(timeout=20, long_polling_timeout=10)

