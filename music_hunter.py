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
    # سیستم اولویت‌بندی AI
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
    return "یک قطعه موسیقی پیشنهادی؛ بشنویم و لذت ببریم.\n\n#موسیقی"

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
        
        # لیست کوئری‌های رندوم برای اینکه هر بار موزیک‌های متفاوتی پیدا شود
        search_terms = ["#music", "remix 2026", "techno", "deep house", "top hits", "جدید", "آهنگ", ".mp3", "full track"]
        random.shuffle(search_terms)
        
        count = 0
        sources_this_run = [] # برای جلوگیری از تکرار منبع در یک اجرا

        print("--- 🌍 Global Random Hunting Started ---")

        for query in search_terms:
            if count >= 50: break
            print(f"Searching globally for: {query}")
            
            try:
                # جستجوی سراسری در کل تلگرام (Global Search)
                async for message in app.search_global(query, limit=150):
                    if count >= 50: break
                    
                    # فقط فایل‌های صوتی
                    if message.audio:
                        f_id = message.audio.file_unique_id
                        chat_id = message.chat.id
                        
                        # فیلتر: تکراری نباشد و در این اجرا از این کانال موزیک نگرفته باشد
                        if f_id not in state["history"] and chat_id not in sources_this_run:
                            
                            # دریافت اطلاعات منبع (رندوم از کل تلگرام)
                            source_username = f"@{message.chat.username}" if message.chat.username else None
                            source_name = message.chat.title or "Unknown"
                            source_display = source_username if source_username else source_name
                            
                            count += 1
                            state["history"].append(f_id)
                            sources_this_run.append(chat_id)
                            
                            f_name = message.audio.file_name or "Track"
                            prompt = f"فایل '{f_name}'. یک معرفی صمیمی و انسانی ۳ خطی به فارسی بنویس. آخرش هشتگ خواننده و سبک بزن."
                            
                            ai_text = await generate_human_text(prompt)
                            
                            final_caption = (
                                f"{ai_text}\n\n"
                                f"🔹 منبع: {source_display}\n"
                                f"🆔 @FavmeMusic"
                            )
                            
                            # کپی فایل به کانال تو
                            await app.copy_message(CHANNEL_ID, message.chat.id, message.id, caption=final_caption)
                            print(f"✅ Hunted from Global: {f_name} (Source: {source_display})")
                            
                            # وقفه برای جلوگیری از محدودیت تلگرام (Flood Wait)
                            await asyncio.sleep(4)
            except Exception as e:
                print(f"Error during global search: {e}")
                continue

        # ذخیره وضعیت و تمیزکاری تاریخچه
        state["history"] = state["history"][-2000:]
        with open(state_file, "w") as f: json.dump(state, f)

if __name__ == "__main__":
    asyncio.run(music_hunter())
