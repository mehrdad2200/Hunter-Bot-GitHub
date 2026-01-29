import asyncio, os, re
from pyrogram import Client
from pyrogram.errors import FloodWait

# تنظیمات از Secrets
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING")

SOURCE_CHANNEL = "Videohive_templates_chat"
TARGET_CHANNEL = "favFile"
MY_ID = "@favFile" # آیدی کانال خودت برای جایگزینی

async def copy_and_clean():
    app = Client("file_hunter", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)
    
    async with app:
        print("Start copying and cleaning posts...")
        # بررسی ۲۰ پست آخر در هر بار اجرا (برای جلوگیری از حساسیت تلگرام)
        async for message in app.get_chat_history(SOURCE_CHANNEL, limit=20):
            try:
                new_caption = ""
                if message.caption:
                    # حذف آیدی‌های تلگرامی منبع (هر چیزی که با @ شروع میشه)
                    text = re.sub(r"@[\w_]+", "", message.caption)
                    # حذف لینک‌های t.me منبع
                    text = re.sub(r"https://t\.me/[\w_]+", "", text)
                    new_caption = text.strip() + f"\n\n🆔 {MY_ID}"
                elif message.text:
                    text = re.sub(r"@[\w_]+", "", message.text)
                    text = re.sub(r"https://t\.me/[\w_]+", "", text)
                    new_caption = text.strip() + f"\n\n🆔 {MY_ID}"

                # ارسال بر اساس نوع فایل
                if message.video:
                    await app.send_video(TARGET_CHANNEL, message.video.file_id, caption=new_caption)
                elif message.document:
                    await app.send_document(TARGET_CHANNEL, message.document.file_id, caption=new_caption)
                elif message.photo:
                    await app.send_photo(TARGET_CHANNEL, message.photo.file_id, caption=new_caption)
                elif message.text:
                    await app.send_message(TARGET_CHANNEL, new_caption)
                
                print(f"✅ Post {message.id} sent to {TARGET_CHANNEL}")
                await asyncio.sleep(5) # وقفه برای امنیت اکانت
                
            except FloodWait as e:
                await asyncio.sleep(e.value)
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(copy_and_clean())
