import asyncio, os, random, json
from pyrogram import Client
from openai import OpenAI

# تنظیمات اصلی
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING")
CHANNEL_ID = "FavmeMusic" 

KEYS = {
    "GEMINI": os.environ.get("GEMINI_KEY"),
    "GROQ": os.environ.get("GROQ_KEY")
}

async def generate_human_text(prompt):
    try:
        # استفاده از Gemini به عنوان موتور اصلی
        client = OpenAI(base_url="https://generativelanguage.googleapis.com/v1beta/openai/", api_key=KEYS["GEMINI"])
        resp = client.chat.completions.create(model="gemini-1.5-flash", messages=[{"role": "user", "content": prompt}])
        return resp.choices[0].message.content
    except:
        return "یک موسیقی ناب برای لحظات شما. بشنویم و لذت ببریم.\n\n#موسیقی"

async def music_hunter():
    app = Client("music_hunter_bot", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)
    async with app:
        state_file = "hunter_state.json"
        if os.path.exists(state_file):
            try:
                with open(state_file, "r") as f: state = json.load(f)
            except: state = {"history": []}
        else: state = {"history": []}
        state.setdefault("history", [])

        count = 0
        sources_this_run = []
        
        # ۱. استراتژی اول: جستجوی جهانی (رندوم)
        search_terms = ["remix 2026", "آهنگ جدید", "music mp3", "top track"]
        random.shuffle(search_terms)
        
        # ۲. استراتژی دوم (پشتیبان): لیست کانال‌های هدف برای اینکه لیست حتما پر بشه
        # این‌ها فقط مثال هستن، می‌تونی یوزرنیم کانال‌های غول موزیک رو اینجا اضافه کنی
        backup_channels = [
            "melobit", "radiojavan", "MifaMusic_ir", "Ahang_Nab", "Nex1Music_com", 
            "worldmusic7", "deephousenation", "The_Top_Music", "G_Music", "top_music_ir"
        ]
        random.shuffle(backup_channels)

        print("--- 🚀 High Intensity Hunting Started ---")

        # اول سعی میکنیم از کل تلگرام بگیریم
        for query in search_terms:
            if count >= 50: break
            try:
                async for message in app.search_global(query, limit=50):
                    if count >= 50: break
                    if message.audio and message.chat.id not in sources_this_run:
                        if message.audio.file_unique_id not in state["history"]:
                            await process_and_post(app, message, state, sources_this_run, CHANNEL_ID)
                            count += 1
                            await asyncio.sleep(3.5)
            except: continue

        # اگر هنوز به ۵۰ تا نرسیدیم، میریم سراغ مخازن اصلی (لیست پرکن)
        if count < 50:
            print(f"Global search limited. Filling the list from backup channels... Current: {count}")
            for target in backup_channels:
                if count >= 50: break
                try:
                    async for message in app.get_chat_history(target, limit=20):
                        if count >= 50: break
                        if message.audio and message.audio.file_unique_id not in state["history"]:
                            await process_and_post(app, message, state, sources_this_run, CHANNEL_ID)
                            count += 1
                            await asyncio.sleep(3.5)
                except: continue

        # ذخیره وضعیت
        state["history"] = state["history"][-2000:]
        with open(state_file, "w") as f: json.dump(state, f)
        print(f"--- Finished! Total Hunted: {count} ---")

async def process_and_post(app, message, state, sources_this_run, target_channel):
    f_id = message.audio.file_unique_id
    state["history"].append(f_id)
    sources_this_run.append(message.chat.id)
    
    source = f"@{message.chat.username}" if message.chat.username else message.chat.title
    prompt = f"فایل '{message.audio.file_name}'. معرفی انسانی و صمیمی ۳ خطی به فارسی. آخرش هشتگ خواننده و سبک."
    
    ai_text = await generate_human_text(prompt)
    caption = f"{ai_text}\n\n🔹 منبع شکار: {source}\n🆔 @FavmeMusic"
    
    try:
        await app.copy_message(target_channel, message.chat.id, message.id, caption=caption)
    except Exception as e:
        print(f"Post Error: {e}")

if __name__ == "__main__":
    asyncio.run(music_hunter())
