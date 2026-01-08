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
    "GROQ": os.environ.get("GROQ_KEY"),
    "CEREBRAS": os.environ.get("CEREBRAS_KEY"),
    "OPENROUTER": os.environ.get("OPENROUTER_KEY")
}

async def generate_human_text(prompt):
    # سیستم اولویت‌بندی AI (Gemini -> Groq -> Others)
    if KEYS["GEMINI"]:
        try:
            client = OpenAI(base_url="https://generativelanguage.googleapis.com/v1beta/openai/", api_key=KEYS["GEMINI"])
            resp = client.chat.completions.create(model="gemini-1.5-flash", messages=[{"role": "user", "content": prompt}])
            return resp.choices[0].message.content
        except: pass
    
    if KEYS["GROQ"]:
        try:
            client = OpenAI(base_url="https://api.groq.com/openai/v1", api_key=KEYS["GROQ"])
            resp = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model="llama-3.3-70b-versatile")
            return resp.choices[0].message.content
        except: pass
    return "یک قطعه موسیقی شنیدنی؛ بشنویم و لذت ببریم.\n\n#موسیقی"

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
        
        # کوئری‌های متنوع برای تحریک موتور جستجوی تلگرام
        search_terms = ["#music", ".mp3", "track", "remix", "آهنگ جدید", "song 2026", "electro", "deep house"]
        random.shuffle(search_terms)
        
        count = 0
        sources_this_run = []

        print("--- 🚀 High-Intensity Hunting Started ---")

        for query in search_terms:
            if count >= 50: break
            print(f"Searching for: {query}")
            
            try:
                # جستجو با محدودیت بیشتر برای جلوگیری از بلاک شدن توسط تلگرام
                async for message in app.search_global(query, limit=100):
                    if count >= 50: break
                    
                    if message.audio:
                        f_id = message.audio.file_unique_id
                        chat_id = message.chat.id
                        
                        # فیلتر تکرار فایل و تکرار منبع در یک اجرا
                        if f_id not in state["history"] and chat_id not in sources_this_run:
                            count += 1
                            state["history"].append(f_id)
                            sources_this_run.append(chat_id)
                            
                            source = f"@{message.chat.username}" if message.chat.username else (message.chat.title or "منبع")
                            f_name = message.audio.file_name or "Unknown"
                            
                            prompt = f"فایل '{f_name}'. یک معرفی ۳ خطی صمیمی و انسانی به فارسی بنویس. آخرش هشتگ خواننده و سبک بزن."
                            ai_text = await generate_human_text(prompt)
                            
                            final_caption = f"{ai_text}\n\n🔹 منبع: {source}\n🆔 @FavmeMusic"
                            
                            await app.copy_message(CHANNEL_ID, message.chat.id, message.id, caption=final_caption)
                            print(f"✅ Hunted: {f_name}")
                            await asyncio.sleep(4) # وقفه برای ایمنی اکانت
            except Exception as e:
                print(f"Search error for {query}: {e}")
                continue

        # ذخیره وضعیت
        state["history"] = state["history"][-2000:]
        with open(state_file, "w") as f: json.dump(state, f)

if __name__ == "__main__":
    asyncio.run(music_hunter())
