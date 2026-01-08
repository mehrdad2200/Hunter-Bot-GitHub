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

async def get_creative_note(band, title):
    """تولید نوت کوتاه و خاص توسط AI"""
    prompt = f"Band: {band}, Title: {title}. یک جمله بسیار کوتاه (۵ کلمه) عمیق و انتزاعی به فارسی بنویس. فقط جمله را بفرست."
    for provider in ["GEMINI", "GROQ", "OPENROUTER"]:
        if KEYS[provider]:
            try:
                base_url = "https://generativelanguage.googleapis.com/v1beta/openai/" if provider == "GEMINI" else \
                           ("https://api.groq.com/openai/v1" if provider == "GROQ" else "https://openrouter.ai/api/v1")
                client = OpenAI(base_url=base_url, api_key=KEYS[provider])
                resp = client.chat.completions.create(
                    model="gemini-1.5-flash" if provider == "GEMINI" else "llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}], timeout=7
                )
                return resp.choices[0].message.content.strip()
            except: continue
    return "انعکاسِ یک سکوت."

async def music_hunter():
    app = Client("music_hunter_bot", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)
    async with app:
        state_file = "hunter_state.json"
        if os.path.exists(state_file):
            try:
                with open(state_file, "r") as f: state = json.load(f)
            except: state = {"history": [], "post_count": 2580}
        else: state = {"history": [], "post_count": 2580}

        count = 0
        for source in PRIORITY_SOURCES:
            if count >= 50: break
            try:
                chat = await app.get_chat(source)
                async for message in app.get_chat_history(chat.id, limit=80):
                    if count >= 50: break
                    if message.audio and message.audio.file_unique_id not in state["history"]:
                        
                        audio = message.audio
                        band = audio.performer or "Various Artists"
                        title = audio.title or "Unknown Track"
                        album = audio.file_name.split('-')[0] if not getattr(audio, 'album', None) else audio.album
                        
                        # استخراج اطلاعات فنی
                        duration = f"{audio.duration // 60}:{audio.duration % 60:02d}"
                        size = f"{audio.file_size / (1024 * 1024):.1f} MB"
                        
                        ai_note = await get_creative_note(band, title)
                        
                        state["history"].append(audio.file_unique_id)
                        state["post_count"] += 1
                        count += 1
                        
                        # دیزاینِ مدرن و شیک (Layout)
                        post_id = str(state["post_count"]).zfill(2)
                        
                        caption = (
                            f"● {post_id}. {ai_note}\n\n"
                            f"   | Band: {band}\n"
                            f"   | Title: {title}\n"
                            f"   | Album: {album if album else 'Single'}\n"
                            f"   | Duration: {duration}\n"
                            f"   | Size: {size}\n"
                            f"   | Genres: #PostRock #Ambient\n\n"
                            f"🆔 @FavmeMusic"
                        )
                        
                        try:
                            await app.copy_message(CHANNEL_ID, chat.id, message.id, caption=caption)
                            print(f"✅ Hunted: {post_id}")
                            await asyncio.sleep(4)
                        except: continue
            except: continue

        state["history"] = state["history"][-2000:]
        with open(state_file, "w") as f: json.dump(state, f)

if __name__ == "__main__":
    asyncio.run(music_hunter())
