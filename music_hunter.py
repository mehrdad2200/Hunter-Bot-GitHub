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
    """تولید متن با سیستم Failover (اولویت با Gemini)"""
    if KEYS["GEMINI"]:
        try:
            client = OpenAI(base_url="https://generativelanguage.googleapis.com/v1beta/openai/", api_key=KEYS["GEMINI"])
            resp = client.chat.completions.create(model="gemini-1.5-flash", messages=[{"role": "user", "content": prompt}])
            return resp.choices[0].message.content
        except: pass
    
    # لایه‌های بعدی (Groq, Cerebras, OpenRouter) در صورت شکست Gemini
    for provider in ["GROQ", "CEREBRAS", "OPENROUTER"]:
        if KEYS[provider]:
            url = "https://api.groq.com/openai/v1" if provider == "GROQ" else ("https://api.cerebras.ai/v1" if provider == "CEREBRAS" else "https://openrouter.ai/api/v1")
            model = "llama-3.3-70b-versatile" if provider == "GROQ" else ("llama3.1-70b" if provider == "CEREBRAS" else "google/gemini-2.0-flash-exp:free")
            try:
                client = OpenAI(base_url=url, api_key=KEYS[provider])
                resp = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model=model)
                return resp.choices[0].message.content
            except: continue
    return "یک موسیقی ناب رندوم تقدیم به شما.\n\n#موسیقی"

async def music_hunter():
    app = Client("music_hunter_bot", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)
    async with app:
        state_file = "hunter_state.json"
        if os.path.exists(state_file):
            try:
                with open(state_file, "r") as f: state = json.load(f)
            except: state = {"history": [], "sources_today": []}
        else: state = {"history": [], "sources_today": []}

        state.setdefault("history", [])
        state.setdefault("sources_today", [])
        
        # ۱. انتخاب کوئری کاملاً رندوم برای پیدا کردن آهنگ‌های مختلف
        search_terms = [".mp3", "music", "track", "remix", "آهنگ", "موزیک", "جدید", "song", "2026"]
        query = random.choice(search_terms)
        
        print(f"--- 🎯 Random Global Hunting: {query} ---")
        count = 0
        
        # ۲. جستجو در کل دنیای تلگرام (Global)
        async for message in app.search_global(query, limit=500):
            if count >= 50: break # سقف ۵۰ آهنگ
            
            if message.audio:
                f_id = message.audio.file_unique_id
                chat_id = message.chat.id
                
                # ۳. فیلتر: تکراری نباشد و از یک کانال در این دور دو تا نگیرد (تنوع حداکثری)
                if f_id not in state["history"] and chat_id not in state["sources_today"]:
                    count += 1
                    state["history"].append(f_id)
                    state["sources_today"].append(chat_id)
                    
                    # استخراج اطلاعات منبع برای کپشن
                    source_link = f"@{message.chat.username}" if message.chat.username else (message.chat.title or "Unknown")
                    
                    prompt = f"آهنگ '{message.audio.file_name}'. یک معرفی ۳ خطی صمیمی و انسانی به فارسی بنویس. اصلاً رباتیک نباشه. در آخر هشتگ خواننده و سبک بزن."
                    ai_text = await generate_human_text(prompt)
                    
                    final_caption = (
                        f"{ai_text}\n\n"
                        f"🔹 منبع: {source_link}\n"
                        f"🆔 @FavmeMusic"
                    )
                    
                    try:
                        await app.copy_message(CHANNEL_ID, message.chat.id, message.id, caption=final_caption)
                        print(f"✅ [{count}] Randomly Hunted from {source_link}")
                        await asyncio.sleep(2.5) # وقفه ایمن
                    except: continue

        # ریست کردن لیست منابع برای اجرای بعدی (تا در هر نوبت تنوع داشته باشیم)
        state["sources_today"] = []
        state["history"] = state["history"][-2000:]
        with open(state_file, "w") as f: json.dump(state, f)

if __name__ == "__main__":
    asyncio.run(music_hunter())
