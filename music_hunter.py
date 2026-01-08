import asyncio, os, random, json
from pyrogram import Client

# تنظیمات اصلی از Secrets گیت‌هاب
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING")
CHANNEL_ID = "FavmeMusic"

# لیست کامل منابع اولویت‌دار (آپدیت شده)
PRIORITY_SOURCES = [
    "https://t.me/+750iUoFndkc5NDc8",
    "https://t.me/+TdHVAC-9SYAyMWI0",
    "musicbazpage",
    "InnerSpce",
    "NonVocalEcho",
    "the_playllist_group",
    "https://t.me/joinchat/P98_Guz-df0D8Pj2",
    "foreignmusiconly",
    "f_music_only",
    "https://t.me/addlist/y3ZeJkAEiGNiY2Nk"
]

async def music_hunter():
    app = Client("music_hunter_bot", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)
    async with app:
        state_file = "hunter_state.json"
        
        # مدیریت وضعیت و ریست شمارنده (شروع واقعی از صفر)
        if os.path.exists(state_file):
            try:
                with open(state_file, "r") as f:
                    state = json.load(f)
            except:
                state = {"history": [], "post_count": 0}
        else:
            state = {"history": [], "post_count": 0}
        
        # اطمینان از وجود متغیرها
        state.setdefault("history", [])
        state.setdefault("post_count", 0)

        count_in_run = 0
        print(f"--- 🚀 Hunter Activated | Starting from ID: {state['post_count'] + 1} ---")

        # چرخش در منابع برای شکار ۵۰ آهنگ
        for source in PRIORITY_SOURCES:
            if count_in_run >= 50: break
            try:
                # ورود به منبع (کانال یا گروه)
                chat = await app.get_chat(source)
                print(f"Checking source: {chat.title or source}")
                
                async for message in app.get_chat_history(chat.id, limit=80):
                    if count_in_run >= 50: break
                    
                    # فقط فایل صوتی که قبلاً شکار نشده باشد
                    if message.audio and message.audio.file_unique_id not in state["history"]:
                        audio = message.audio
                        
                        # استخراج اطلاعات از دیتای واقعی فایل
                        band = audio.performer or "Unknown Artist"
                        title = audio.title or "Unknown Track"
                        album = getattr(audio, "album", None)
                        genre = getattr(audio, "genre", None)
                        duration = f"{audio.duration // 60}:{audio.duration % 60:02d}"
                        size = f"{audio.file_size / (1024 * 1024):.1f} MB"
                        
                        # آپدیت شمارنده
                        state["post_count"] += 1
                        count_in_run += 1
                        state["history"].append(audio.file_unique_id)
                        
                        # دیزاین مدرن و تمیز
                        post_no = str(state["post_count"]).zfill(2)
                        caption = f"● {post_no}\n\n"
                        caption += f"   | Band: {band}\n"
                        caption += f"   | Title: {title}\n"
                        if album: caption += f"   | Album: {album}\n"
                        caption += f"   | Duration: {duration}\n"
                        caption += f"   | Size: {size}\n"
                        if genre: caption += f"   | Genre: #{genre.replace(' ', '').replace('/', '_')}\n"
                        
                        caption += f"\n🆔 @FavmeMusic"
                        
                        try:
                            # کپی فایل به کانال مقصد
                            await app.copy_message(CHANNEL_ID, chat.id, message.id, caption=caption)
                            print(f"✅ [{count_in_run}/50] Posted: {post_no}")
                            await asyncio.sleep(4) # وقفه برای جلوگیری از اسپم
                        except Exception as e:
                            print(f"Post error: {e}")
                            continue
            except Exception as e:
                print(f"Could not access source {source}: {e}")
                continue

        # ذخیره وضعیت نهایی برای اجرای بعدی
        state["history"] = state["history"][-3000:] # حفظ تاریخچه برای جلوگیری از تکرار
        with open(state_file, "w") as f:
            json.dump(state, f)
        
        print(f"--- Session Finished | Total Hunted: {count_in_run} ---")

if __name__ == "__main__":
    asyncio.run(music_hunter())
