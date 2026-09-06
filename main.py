import os
from flask import Flask
from threading import Thread
import telebot
from telebot import types

TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    web_app = types.WebAppInfo("https://Sobujvai770.github.io/telegram-video-bot/") 
    button = types.InlineKeyboardButton("Watch Now 🎬", web_app=web_app)
    markup.add(button)
    
    welcome_text = "🎬 এখানে পাবেন নিত্য নতুন কালেকশন 🎬 দেরি না করে নিচের Watch Now বাটনে ক্লিক করুন!"
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()

