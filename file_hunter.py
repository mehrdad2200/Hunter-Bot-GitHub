import asyncio, os, re
from pyrogram import Client
from pyrogram.errors import FloodWait

# فراخوانی متغیرها دقیقاً طبق اسامی در عکس شما
API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")
# اینجا رو اصلاح کردم که STRING_SESSION رو بخونه
SESSION_STRING = os.environ.get("STRING_SESSION")

SOURCE_CHANNEL = "Videohive_templates_chat"
TARGET_CHANNEL = "favFile"
MY_ID = "@favFile"
LAST_ID_FILE = "last_post_id.txt"

async def copy_ordered():
    # بررسی وجود سشن برای جلوگیری از ارور
    if not SESSION_STRING:
        print("❌ ERROR: STRING_SESSION is empty in GitHub Secrets!")
        return

    app = Client(
        "file_hunter_session",
        api_id=int(API_ID),
        api_hash=API_HASH,
        session_string=SESSION_STRING,
        in_memory=True
    )
    
    async with app:
        print("✅ Connected to Telegram successfully!")
        
        last_id = 0
        if os.path.exists(LAST_ID_FILE):
            with open(LAST_ID_FILE, "r") as f:
                content = f.read().strip()
                if content: last_id = int(content)

        print(f"Searching for new posts after ID: {last_id}...")

        messages_to_copy = []
        # اسکن ۵۰ پست اخیر
        async for message in app.get_chat_history(SOURCE_CHANNEL, limit=50):
            if message.id <= last_id:
                break
            # فقط پست‌های دارای فایل یا متن
            if any([message.video, message.document, message.photo, message.text]):
                messages_to_copy.append(message)

        if not messages_to_copy:
            print("No new posts found.")
            return

        # مرتب‌سازی از قدیمی به جدید
        messages_to_copy.reverse()

        for message in messages_to_copy:
            try:
                new_caption = ""
                original_text = message.caption or message.text or ""
                if original_text:
                    # پاکسازی کپشن از لینک‌ها و آیدی‌های منبع
                    text = re.sub(r"@[\w_]+", "", original_text)
                    text = re.sub(r"https://t\.me/[\w_]+", "", text)
                    new_caption = text.strip() + f"\n\n🆔 {MY_ID}"

                # ارسال به کانال مقصد
                if message.video:
                    await app.send_video(TARGET_CHANNEL, message.video.file_id, caption=new_caption)
                elif message.document:
                    await app.send_document(TARGET_CHANNEL, message.document.file_id, caption=new_caption)
                elif message.photo:
                    await app.send_photo(TARGET_CHANNEL, message.photo.file_id, caption=new_caption)
                elif message.text:
                    await app.send_message(TARGET_CHANNEL, new_caption)

                print(f"✅ Post {message.id} copied.")
                
                # آپدیت آیدی آخرین پست
                with open(LAST_ID_FILE, "w") as f:
                    f.write(str(message.id))
                
                # وقفه ۱۰ ثانیه‌ای برای امنیت اکانت
                await asyncio.sleep(10)

            except FloodWait as e:
                print(f"Waiting for {e.value}s due to FloodWait...")
                await asyncio.sleep(e.value)
            except Exception as e:
                print(f"Error on post {message.id}: {e}")

if __name__ == "__main__":
    asyncio.run(copy_ordered())
