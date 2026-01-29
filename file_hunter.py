import asyncio, os, re
from pyrogram import Client
from pyrogram.errors import FloodWait

# تنظیمات از Secrets
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING")

SOURCE_CHANNEL = "Videohive_templates_chat"
TARGET_CHANNEL = "favFile"
MY_ID = "@favFile"
LAST_ID_FILE = "last_post_id.txt"

async def copy_ordered():
    app = Client("file_hunter", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)
    
    async with app:
        # ۱. خوندن آیدی آخرین پستی که قبلاً کپی شده
        last_id = 0
        if os.path.exists(LAST_ID_FILE):
            with open(LAST_ID_FILE, "r") as f:
                last_id = int(f.read().strip())

        print(f"Searching for posts after ID: {last_id}...")

        # ۲. گرفتن پست‌ها (به ترتیب قدیمی به جدید)
        # ما پست‌ها رو برعکس می‌گیریم تا از قدیمی شروع کنیم
        messages_to_copy = []
        async for message in app.get_chat_history(SOURCE_CHANNEL, limit=50):
            if message.id <= last_id:
                break
            messages_to_copy.append(message)

        if not messages_to_copy:
            print("No new posts found.")
            return

        # مرتب کردن از قدیمی به جدید
        messages_to_copy.reverse()

        for message in messages_to_copy:
            try:
                new_caption = ""
                # تمیز کردن کپشن و جایگزینی آیدی تو
                original_text = message.caption or message.text or ""
                if original_text:
                    text = re.sub(r"@[\w_]+", "", original_text)
                    text = re.sub(r"https://t\.me/[\w_]+", "", text)
                    new_caption = text.strip() + f"\n\n🆔 {MY_ID}"

                # کپی کردن پست
                if message.video:
                    await app.send_video(TARGET_CHANNEL, message.video.file_id, caption=new_caption)
                elif message.document:
                    await app.send_document(TARGET_CHANNEL, message.document.file_id, caption=new_caption)
                elif message.photo:
                    await app.send_photo(TARGET_CHANNEL, message.photo.file_id, caption=new_caption)
                elif message.text:
                    await app.send_message(TARGET_CHANNEL, new_caption)

                print(f"✅ Post {message.id} copied.")
                
                # ۳. ذخیره آیدی پست کپی شده به عنوان آخرین آیدی
                with open(LAST_ID_FILE, "w") as f:
                    f.write(str(message.id))
                
                await asyncio.sleep(10) # وقفه برای امنیت اکانت

            except FloodWait as e:
                await asyncio.sleep(e.value)
            except Exception as e:
                print(f"Error on post {message.id}: {e}")

if __name__ == "__main__":
    asyncio.run(copy_ordered())
