import asyncio, os
from pyrogram import Client
from pyrogram.errors import FloodWait

# فراخوانی سکرت‌ها از گیت‌هاب
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING")

# آیدی کانال مقصد (موزیک)
TARGET_CHANNEL = "FavmeMusic"
# کانال‌هایی که ازشون موزیک جمع می‌کنی
MUSIC_SOURCES = ["Melobit", "Ahangify", "MifaMusic_ir"] 

async def music_hunter():
    # اضافه کردن session_string برای جلوگیری از ارور شماره تلفن
    app = Client("music_session", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)
    
    async with app:
        print("Music Hunter Started...")
        for source in MUSIC_SOURCES:
            try:
                # گرفتن ۵ موزیک آخر از هر منبع
                async for message in app.get_chat_history(source, limit=5):
                    if message.audio or message.voice:
                        # کپی کردن موزیک به کانال خودت بدون نام منبع
                        await message.copy(TARGET_CHANNEL)
                        print(f"✅ Music copied from {source}")
                        await asyncio.sleep(3) # برای جلوگیری از بلاک شدن
            except FloodWait as e:
                await asyncio.sleep(e.value)
            except Exception as e:
                print(f"❌ Error in {source}: {e}")

if __name__ == "__main__":
    asyncio.run(music_hunter())
