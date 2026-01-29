import asyncio, os
from pyrogram import Client
from pyrogram.errors import FloodWait

# تنظیمات از Secrets گیت‌هاب
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING")

SOURCE_CHANNEL = "Videohive_templates_chat" # کانال منبع
TARGET_CHANNEL = "favFile" # کانال تو

async def copy_files():
    app = Client("file_copier", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)
    
    async with app:
        print("Starting to copy files...")
        # بررسی ۵۰ پست آخر (می‌تونی عدد رو بیشتر کنی)
        async for message in app.get_chat_history(SOURCE_CHANNEL, limit=50):
            try:
                # کپی کردن پست با تمام جزئیات (کپشن، فایل، دکمه و...)
                await message.copy(TARGET_CHANNEL)
                print(f"✅ Post {message.id} copied.")
                # وقفه کوتاه برای جلوگیری از ریپورت تلگرام
                await asyncio.sleep(2) 
            except FloodWait as e:
                print(f"Waiting for {e.value} seconds...")
                await asyncio.sleep(e.value)
            except Exception as e:
                print(f"Error copying message {message.id}: {e}")

if __name__ == "__main__":
    asyncio.run(copy_files())
