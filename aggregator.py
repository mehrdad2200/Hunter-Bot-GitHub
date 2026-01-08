import asyncio, os
from pyrogram import Client
from datetime import datetime

# تنظیمات تلگرام
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING")
CHANNEL_ID = "favproxy" # یا آیدی عددی کانالت

async def send_post():
    app = Client("sender", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)
    async with app:
        # خواندن آمار از فایلی که مرحله قبل ساختیم
        with open("stats.txt", "r", encoding="utf-8") as f:
            report_stats = f.read()
        
        now = datetime.now()
        date_str = "1404/10/18" # اینجا می‌تونی از کتابخانه jdatetime برای تاریخ شمسی استفاده کنی
        time_str = now.strftime("%H:%M")
        
        SUB_LINK = "https://mehrdad2200.github.io/Hunter-Bot-GitHub/"
        
        caption = (
            f"💠 HUNTER PREMIUM CONFIGS\n"
            f"──────────────────────\n"
            f"📅 DATE: {date_str}  |  ⏰ TIME: {time_str}\n"
            f"{report_stats}\n"
            f"🌐 NETWORK STATUS: Global Online ✅\n"
            f"──────────────────────\n"
            f"🔗 SUBSCRIPTION LINK (Tap to Copy):\n"
            f"`{SUB_LINK}`\n\n"
            f"💡 *Copy the link above and paste it into your app (v2rayNG / Shadowrocket) for auto-updates.*\n"
            f"──────────────────────\n"
            f"🆔 @favproxy"
        )
        
        await app.send_message(CHANNEL_ID, caption)

if __name__ == "__main__":
    asyncio.run(send_post())
