
import os

if __name__ == '__main__':
    import threading
    t = threading.Thread(target=run_flask)
    t.start()
    
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    
    bot.infinity_polling(timeout=60, long_polling_timeout=60)

import os
from flask import Flask, render_template_string
import telebot

# আপনার টেলিগ্রাম বটের টোকেন এখানে দিন
TOKEN = '8886625553:AAE1WOI_-EpBlNFm08jEE1zDqtvEKw1myc8'
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)

# ইন-মেমোরি ডাটাবেস (ভিডিও স্টোর করার জন্য)
videos = {}

# বটের স্টার্ট কমান্ড
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "স্বাগতম! ভিডিও যুক্ত করতে /add কমান্ড ব্যবহার করুন।")

# ভিডিও যুক্ত করার কমান্ড (ব্যবহার: /add শিরোনাম | থাম্বনেইল_লিংক | ভিডিও_লিংক)
@bot.message_handler(commands=['add'])
def add_video(message):
    try:
        parts = message.text.replace('/add', '').strip().split('|')
        if len(parts) < 3:
            bot.reply_to(message, "সঠিক ফরম্যাট: /add শিরোনাম | থাম্বনেইল_লিংক | ভিডিও_লিংক")
            return
        
        title = parts[0].strip()
        thumb = parts[1].strip()
        vlink = parts[2].strip()
        
        # ইউনিক আইডি তৈরি
        video_id = str(len(videos) + 1)
        videos[video_id] = {'title': title, 'thumb': thumb, 'link': vlink}
        
        # জেনারেট হওয়া লিংক বকিতে পাঠানো
        watch_url = f"https://your-tunnel-url.trycloudflare.com/watch/{video_id}"
        bot.reply_to(message, f"ভিডিও সফলভাবে যুক্ত হয়েছে!\nওয়েব লিংক: {watch_url}")
    except Exception as e:
        bot.reply_to(message, f"ত্রুটি হয়েছে: {str(e)}")

# ফ্লাস্ক ওয়েব পেজ (যেখানে ভিডিও এবং বিজ্ঞাপন শো করবে)
@app.route('/watch/<video_id>')
def watch_video(video_id):
    video = videos.get(video_id)
    if not video:
        return "ভিডিওটি পাওয়া যায়নি!", 404

    html_template = """
    <!DOCTYPE html>
    <html lang="bn">
    <head>
        <meta charset="UTF-8">
        <title>{{ video.title }}</title>
        <style>
            body { font-family: Arial, sans-serif; background: #121212; color: #fff; text-align: center; padding: 20px; }
            .video-container { max-width: 600px; margin: auto; }
            img { width: 100%; border-radius: 10px; }
            .ad-box { background: #333; padding: 15px; margin: 20px 0; border-radius: 5px; color: #ffeb3b; }
            .btn { display: inline-block; background: #0088cc; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; margin-top: 15px; }
        </style>
    </head>
    <body>
        <div class="video-container">
            <h2>{{ video.title }}</h2>
            
            <!-- অ্যাড স্পেস -->
            <div class="ad-box">
                <p>--- এখানে আপনার অ্যাড কোড (Ad Code) বসাবেন ---</p>
            </div>

            <img src="{{ video.thumb }}" alt="Thumbnail">
            <br>
            <a class="btn" href="{{ video.link }}" target="_blank">ভিডিও দেখতে এখানে ক্লিক করুন</a>

            <!-- আরেকটি অ্যাড স্পেস -->
            <div class="ad-box">
                <p>--- নিচের অ্যাড স্পেস ---</p>
            </div>
        </div>
    </body>
    </html>
    """
    return render_template_string(html_template, video=video)

def run_flask():
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

if __name__ == '__main__':
    import threading
    t = threading.Thread(target=run_flask)
    t.start()
    bot.infinity_polling(timeout=60, long_polling_timeout=60)


