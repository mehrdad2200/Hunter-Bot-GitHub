import asyncio, os, random, json
from pyrogram import Client

# تنظیمات اصلی
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING")
CHANNEL_ID = "FavmeMusic"

PRIORITY_SOURCES = [
    "https://t.me/+750iUoFndkc5NDc8",
    "https://t.me/+TdHVAC-9SYAyMWI0",
    "musicbazpage",
    "InnerSpce"
]

async def music_hunter():
    app = Client("music_hunter_bot", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)
    async with app:
        state_file = "hunter_state.json"
        
        # لود کردن وضعیت (شروع شمارنده از 0 اگر فایل نباشد)
        if os.path.exists(state_file):
            try:
                with open(state_file, "r") as f: state = json.load(f)
            except: state = {"history": [], "post_count": 0}
        else: state = {"history": [], "post_count": 0}
        
        state.setdefault("history", [])
        state.setdefault("post_count", 0)

        count_in_run = 0
        print(f"--- 🚀 Hunter Started | Current Count: {state['post_count']} ---")

        for source in PRIORITY_SOURCES:
            if count_in_run >= 50: break
            try:
                chat = await app.get_chat(source)
                async for message in app.get_chat_history(chat.id, limit=80):
                    if count_in_run >= 50: break
                    
                    if message.audio and message.audio.file_unique_id not in state["history"]:
                        audio = message.audio
                        
                        # استخراج اطلاعات
                        band = audio.performer or "Unknown Artist"
                        title = audio.title or "Unknown Track"
                        album = getattr(audio, "album", "Single") or "Single"
                        duration = f"{audio.duration // 60}:{audio.duration % 60:02d}"
                        size = f"{audio.file_size / (1024 * 1024):.1f} MB"
                        
                        # افزایش شمارنده
                        state["post_count"] += 1
                        count_in_run += 1
                        state["history"].append(audio.file_unique_id)
                        
                        # شماره‌گذاری شیک (01, 02, ... 100, 101, ...)
                        post_id = str(state["post_count"]).zfill(2)
                        
                        # دیزاین مدرن و تمیز بدون جملات اضافه هوش مصنوعی
                        caption = (
                            f"𝟶𝟷. {post_id}\n\n" # شماره پست با فونت مونو
                            f"   | Band: {band}\n"
                            f"   | Title: {title}\n"
                            f"   | Album: {album}\n"
                            f"   | Duration: {duration}\n"
                            f"   | Size: {size}\n"
                            f"   | Genres: #PostRock #Ambient #Electronic #Minimal\n\n"
                            f"🆔 @FavmeMusic"
                        )
                        
                        try:
                            await app.copy_message(CHANNEL_ID, chat.id, message.id, caption=caption)
                            print(f"✅ Posted: {post_id}")
                            await asyncio.sleep(3.5) # وقفه ایمن
                        except Exception as e:
                            print(f"Post error: {e}")
                            continue
            except Exception as e:
                print(f"Source error {source}: {e}")
                continue

        # ذخیره وضعیت برای دفعه بعد
        state["history"] = state["history"][-3000:] # نگه داشتن ۳۰۰۰ آی‌دی آخر برای جلوگیری از تکرار
        with open(state_file, "w") as f:
            json.dump(state, f)
        
        print(f"--- Session Finished | Total Sent: {count_in_run} | Final ID: {state['post_count']} ---")

if __name__ == "__main__":
    asyncio.run(music_hunter())
