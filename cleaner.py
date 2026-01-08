import asyncio, os
from pyrogram import Client
from datetime import datetime, timedelta, timezone

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING")
CHANNEL_ID = "favproxy"

async def clean_old_posts():
    app = Client("cleaner_bot", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)
    async with app:
        now = datetime.now(timezone.utc)
        
        # تنظیم دقیق بر اساس دستور شما:
        config_threshold = now - timedelta(days=30)  # فایل‌های کانفیگ -> ۳۰ روز ماندگاری
        report_threshold = now - timedelta(hours=72) # گزارش‌های متنی/آماری -> ۷۲ ساعت ماندگاری

        async for message in app.get_chat_history(CHANNEL_ID, limit=300):
            if message.pinned:
                continue

            # ۱. پاکسازی گزارش‌های شبانه و پیام‌های متنی (بدون فایل) بعد از ۷۲ ساعت
            if not message.document and message.date < report_threshold:
                try:
                    await message.delete()
                    print(f"Deleted old report/text: {message.id}")
                except Exception as e:
                    print(f"Error: {e}")

            # ۲. پاکسازی فایل‌های کانفیگ (Document) بعد از ۳۰ روز
            elif message.document and message.date < config_threshold:
                try:
                    await message.delete()
                    print(f"Deleted old config file: {message.id}")
                except Exception as e:
                    print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(clean_old_posts())
