

import os
import threading
import telebot
from flask import Flask

# ফ্লাস্ক ওয়েব সার্ভার সেটআপ (Render-এর পোর্ট রিকোয়ারমেন্ট পূরণের জন্য)
app = Flask('')


@app.route('/')
def home():
  return "Bot is running 24/7!"


def run():
  app.run(host='0.0.0.0', port=8080)


def keep_alive():
  t = threading.Thread(target=run)
  t.start()


# ফ্লাস্ক ব্যাকগ্রাউন্ডে রান করা শুরু করবে
keep_alive()

# টেলিগ্রাম বট টোকেন এনভায়রনমেন্ট ভ্যারিয়েবল থেকে নেওয়া হচ্ছে
TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# ইন-মেমোরি ডাটাবেস (ভিডিও স্টোর করার জন্য)
videos = {}


# বটের /start কমান্ড
@bot.message_handler(commands=['start'])
def send_welcome(message):
  bot.reply_to(message, 'স্বাগতম! ভিডিও যুক্ত করতে /add কমান্ড ব্যবহার করুন।')


# ভিডিও যুক্ত করার কমান্ড (ব্যবহার: /add শিরোনাম | থাম্বনেইল_লিংক | ভিডিও_লিংক)
@bot.message_handler(commands=['add'])
def add_video(message):
  try:
    parts = message.text.replace('/add', '').strip().split('|')
    if len(parts) < 3:
      bot.reply_to(
          message,
          'সঠিক ফরম্যাট: /add শিরোনাম | থাম্বনেইল_লিংক | ভিডিও_লিংক',
      )
      return

    title = parts[0].strip()
    thumb = parts[1].strip()
    vlink = parts[2].strip()

    video_id = str(len(videos) + 1)
    videos[video_id] = {'title': title, 'thumb': thumb, 'link': vlink}

    bot.reply_to(message, f'ভিডিও সফলভাবে যুক্ত হয়েছে! আইডি: {video_id}')
  except Exception as e:
    bot.reply_to(message, f'ত্রুটি ঘটেছে: {e}')


# বট চালু রাখা
if __name__ == '__main__':
  bot.infinity_polling(timeout=60, long_polling_timeout=60)

