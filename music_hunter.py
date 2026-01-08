import asyncio, os, random, json, re
from pyrogram import Client
import google.generativeai as genai
from openai import OpenAI

# تنظیمات اصلی
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING")
CHANNEL_ID = "FavmeMusic"

# کلیدهای هوش مصنوعی از Secrets
KEYS = {
    "GEMINI": os.environ.get("GEMINI_KEY"),
    "GROQ": os.environ.get("GROQ_KEY"),
    "CEREBRAS": os.environ.get("CEREBRAS_KEY"),
    "OPENROUTER": os.environ.get("OPENROUTER_KEY")
}

async def generate_human_text(prompt):
    # اولویت ۱: Gemini
    if KEYS["GEMINI"]:
        try:
            genai.configure(api_key=KEYS["GEMINI"])
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt)
            return response.text
        except: pass

    # اولویت ۲: Groq
    if KEYS["GROQ"]:
        try:
            client = OpenAI(base_url="https://api.groq.com/openai/v1", api_key=KEYS["GROQ"])
            response = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile",
            )
            return response.choices[0].message.content
        except: pass

    # اولویت ۳: Cerebras
    if KEYS["CEREBRAS"]:
        try:
            client = OpenAI(base_url="https://api.cerebras.ai/v1", api_key=KEYS["CEREBRAS"])
            response = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama3.1-70b",
            )
            return response.choices[0].message.content
        except: pass

    # اولویت ۴: OpenRouter
    if KEYS["OPENROUTER"]:
        try:
            client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=KEYS["OPENROUTER"])
            response = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="google/gemini-2.0-flash-exp:free",
            )
            return response.choices[0].message.content
        except: pass

    return "یک موسیقی ناب برای لحظات شما. بشنویم و لذت ببریم.\n\n#موسیقی #پیشنهاد"

async def music_hunter():
    app = Client("music_hunter_bot", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)
    async with app:
        # مدیریت وضعیت (نوبت و تاریخچه)
        state_file = "hunter_state.json"
        if os.path.exists(state_file):
            try:
                with open(state_file, "r") as f: state = json.load(f)
            except: state = {"counter": 0, "history": []}
        else: state = {"counter": 0, "history": []}

        state["counter"] += 1
        is_farsi = (state["counter"] % 4 == 1) # چرخه ۱ فارسی، ۳ خارجی
        
        # استراتژی جستجو
        search_queries = ["آهنگ جدید", "موزیک فارسی"] if is_farsi else ["new music", "remix 2026", "deep house", "techno"]
        query = random.choice(search_queries)
        
        print(f"--- Hunting Phase: {'Farsi' if is_farsi else 'Global'} | Query: {query} ---")

        count = 0
        async for message in app.search_global(query, limit=200):
            if count >= 45: break # هدف ۳۰ تا ۵۰ آهنگ
            
            if message.audio:
                file_id = message.audio.file_unique_id
                if file_id not in state["history"]:
                    count += 1
                    state["history"].append(file_id)
                    
                    # استخراج نام منبع
                    source = f"@{message.chat.username}" if message.chat.username else (message.chat.title or "منبع ناشناس")
                    
                    # پرومپت برای هوش مصنوعی
                    f_name = message.audio.file_name or "Unknown"
                    orig_cap = message.caption or ""
                    prompt = f"فایل: {f_name}. کپشن: {orig_cap}. این موزیک رو تحلیل کن و یک معرفی ۳ خطی صمیمی و انسانی به زبان فارسی بنویس. اصلاً رباتیک نباشه. آخرش هشتگ خواننده و سبک بزن."
                    
                    human_text = await generate_human_text(prompt)
                    
                    final_caption = (
                        f"{human_text}\n\n"
                        f"🎵 شکار شده از: {source}\n"
                        f"🆔 @FavmeMusic"
                    )
                    
                    try:
                        await app.copy_message(CHANNEL_ID, message.chat.id, message.id, caption=final_caption)
                        print(f"Successfully posted: {f_name}")
                        await asyncio.sleep(4) # فاصله برای جلوگیری از بلاک
                    except: continue

        # ذخیره وضعیت (۱۰۰۰ آهنگ آخر برای جلوگیری از تکرار)
        state["history"] = state["history"][-1000:]
        with open(state_file, "w") as f: json.dump(state, f)

if __name__ == "__main__":
    asyncio.run(music_hunter())
