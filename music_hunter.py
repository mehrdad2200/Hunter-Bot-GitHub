import asyncio, os, random, json, re
from pyrogram import Client
from google import genai 
from openai import OpenAI

# تنظیمات اصلی
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING")
CHANNEL_ID = "FavmeMusic"

# کلیدهای هوش مصنوعی (Sercets)
KEYS = {
    "GEMINI": os.environ.get("GEMINI_KEY"),
    "GROQ": os.environ.get("GROQ_KEY"),
    "CEREBRAS": os.environ.get("CEREBRAS_KEY"),
    "OPENROUTER": os.environ.get("OPENROUTER_KEY")
}

async def generate_human_text(prompt):
    """مدیریت هوشمند خروجی هوش مصنوعی با اولویت‌بندی"""
    # ۱. اولویت اول: Gemini 2.0
    if KEYS["GEMINI"]:
        try:
            client = genai.Client(api_key=KEYS["GEMINI"])
            response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
            return response.text
        except: pass

    # ۲. اولویت دوم: Groq
    if KEYS["GROQ"]:
        try:
            client = OpenAI(base_url="https://api.groq.com/openai/v1", api_key=KEYS["GROQ"])
            resp = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile",
            )
            return resp.choices[0].message.content
        except: pass

    # ۳. لایه پشتیبان نهایی (Cerebras یا OpenRouter)
    for provider in ["CEREBRAS", "OPENROUTER"]:
        if KEYS[provider]:
            url = "https://api.cerebras.ai/v1" if provider == "CEREBRAS" else "https://openrouter.ai/api/v1"
            model_name = "llama3.1-70b" if provider == "CEREBRAS" else "google/gemini-2.0-flash-exp:free"
            try:
                client = OpenAI(base_url=url, api_key=KEYS[provider])
                resp = client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model=model_name,
                )
                return resp.choices[0].message.content
            except: continue

    return "یک قطعه موسیقی شنیدنی؛ بشنویم و لذت ببریم.\n\n#موسیقی"

async def music_hunter():
    app = Client("music_hunter_bot", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)
    async with app:
        state_file = "hunter_state.json"
        
        # لود کردن دیتابیس وضعیت
        if os.path.exists(state_file):
            try:
                with open(state_file, "r") as f: 
                    state = json.load(f)
                state.setdefault("counter", 0)
                state.setdefault("history", [])
            except: state = {"counter": 0, "history": []}
        else: state = {"counter": 0, "history": []}

        state["counter"] += 1
        is_farsi = (state["counter"] % 4 == 1) # ۱ بار فارسی، ۳ بار خارجی
        
        queries = ["آهنگ جدید", "موزیک ایرانی"] if is_farsi else ["new music", "remix 2026", "techno", "deep house"]
        query = random.choice(queries)
        
        print(f"--- 🚀 Hunting Mode: {'Farsi' if is_farsi else 'Global'} | Query: {query} ---")

        count = 0
        async for message in app.search_global(query, limit=400):
            if count >= 50: break # شکار ۵۰ عدد در هر اجرا
            
            if message.audio:
                f_id = message.audio.file_unique_id
                if f_id not in state["history"]:
                    count += 1
                    state["history"].append(f_id)
                    
                    source = f"@{message.chat.username}" if message.chat.username else (message.chat.title or "منبع")
                    f_name = message.audio.file_name or "Unknown"
                    
                    prompt = f"فایل موسیقی '{f_name}' پیدا شده. یک معرفی انسانی و صمیمی ۳ خطی به فارسی بنویس که اصلا شبیه ربات نباشه. آخرش هشتگ خواننده و سبک بزن."
                    
                    ai_text = await generate_human_text(prompt)
                    final_caption = f"{ai_text}\n\n🎵 منبع شکار: {source}\n🆔 @FavmeMusic"
                    
                    try:
                        await app.copy_message(CHANNEL_ID, message.chat.id, message.id, caption=final_caption)
                        print(f"✅ [{count}] Posted: {f_name}")
                        await asyncio.sleep(2.5) # فاصله ایمن
                    except: continue

        # ذخیره و تمیزکاری تاریخچه
        state["history"] = state["history"][-2000:]
        with open(state_file, "w") as f:
            json.dump(state, f)

if __name__ == "__main__":
    asyncio.run(music_hunter())
