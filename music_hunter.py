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

PRIORITY_SOURCES = [
    "https://t.me/+750iUoFndkc5NDc8",
    "https://t.me/+TdHVAC-9SYAyMWI0",
    "musicbazpage",
    "InnerSpce"
]

async def generate_caption(file_name):
    # لیست پرومپت‌های رندوم برای اینکه کپشن‌ها شبیه هم نشن
    style = random.choice([
        "یک جمله کوتاه و عمیق درباره تنهایی و موسیقی بنویس.",
        "یک مصرع شعر نو یا یک جمله دارک کوتاه بنویس.",
        "یک جمله مینیمال و مفهومی بنویس.",
        "یک جمله کوتاه درباره خاطرات و نت‌های موسیقی بنویس."
    ])
    
    prompt = f"نام آهنگ: {file_name}. {style} فقط جمله رو بفرست و هیچی اضافه نکن."

    # لایه ۱: Gemini
    if KEYS["GEMINI"]:
        try:
            client = OpenAI(base_url="https://generativelanguage.googleapis.com/v1beta/openai/", api_key=KEYS["GEMINI"])
            resp = client.chat.completions.create(model="gemini-1.5-flash", messages=[{"role": "user", "content": prompt}], timeout=10)
            return resp.choices[0].message.content.strip()
        except: pass

    # لایه ۲: Groq (Llama 3.3)
    if KEYS["GROQ"]:
        try:
            client = OpenAI(base_url="https://api.groq.com/openai/v1", api_key=KEYS["GROQ"])
            resp = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}], timeout=10)
            return resp.choices[0].message.content.strip()
        except: pass

    # لایه ۳: OpenRouter (بهترین جایگزین)
    if KEYS["OPENROUTER"]:
        try:
            client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=KEYS["OPENROUTER"])
            resp = client.chat.completions.create(model="google/gemini-2.0-flash-exp:free", messages=[{"role": "user", "content": prompt}], timeout=10)
            return resp.choices[0].message.content.strip()
        except: pass

    return None # اگر هیچکدام کار نکرد متن تکراری نده

async def music_hunter():
    app = Client("music_hunter_bot", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)
    async with app:
        state_file = "hunter_state.json"
        if os.path.exists(state_file):
            try:
                with open(state_file, "r") as f: state = json.load(f)
            except: state = {"history": [], "post_count": 2580} # از اینجا به بعد شماره بزنه
        else: state = {"history": [], "post_count": 2580}
        
        state.setdefault("history", [])
        state.setdefault("post_count", 2580)

        count = 0
        for source in PRIORITY_SOURCES:
            if count >= 50: break
            try:
                chat = await app.get_chat(source)
                async for message in app.get_chat_history(chat.id, limit=60):
                    if count >= 50: break
                    if message.audio and message.audio.file_unique_id not in state["history"]:
                        
                        # تولید کپشن
                        ai_text = await generate_caption(message.audio.file_name or "Music")
                        
                        if ai_text: # فقط اگر هوش مصنوعی جواب داد پست کن
                            state["history"].append(message.audio.file_unique_id)
                            state["post_count"] += 1
                            count += 1
                            
                            num = str(state["post_count"]).zfill(2)
                            final_text = f"{num}. {ai_text}\n\n🆔 @FavmeMusic"
                            
                            await app.copy_message(CHANNEL_ID, chat.id, message.id, caption=final_text)
                            await asyncio.sleep(4)
            except: continue

        state["history"] = state["history"][-2000:]
        with open(state_file, "w") as f: json.dump(state, f)

if __name__ == "__main__":
    asyncio.run(music_hunter())
