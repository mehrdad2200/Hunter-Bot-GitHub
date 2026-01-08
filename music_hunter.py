import asyncio, os, random, json
from pyrogram import Client
from openai import OpenAI
from datetime import datetime, timedelta

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
    """تولید متن با سیستم Failover"""
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
    
    return "یک قطعه شنیدنی تقدیم به شما.\n\n#موسیقی"

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
        
        print("--- 📡 Live Sniffing Started ---")
        count = 0
        limit_time = datetime.now() - timedelta(hours=2) # فقط آهنگ‌های ۲ ساعت اخیر

        # چک کردن تمام گفتگوها (کانال‌هایی که عضو هستی)
        async for dialog in app.get_dialogs():
            if count >= 50: break
            
            # فقط کانال‌ها (Type Channel)
            if str(dialog.chat.type) in ["ChatType.CHANNEL", "channel"]:
                try:
                    # بررسی ۱۰ پیام آخر هر کانال برای سرعت بالا
                    async for message in app.get_chat_history(dialog.chat.id, limit=10):
                        if message.audio:
                            f_id = message.audio.file_unique_id
                            
                            # اگر تکراری نبود و جدید بود
                            if f_id not in state["history"]:
                                count += 1
                                state["history"].append(f_id)
                                
                                source_name = dialog.chat.title
                                source_link = f"@{dialog.chat.username}" if dialog.chat.username else "Private Source"
                                
                                prompt = f"آهنگ '{message.audio.file_name}' از کانال '{source_name}'. یک معرفی ۳ خطی صمیمی و جذاب فارسی بنویس. آخرش هشتگ خواننده و سبک بزن."
                                ai_text = await generate_human_text(prompt)
                                
                                final_caption = f"{ai_text}\n\n🎵 منبع شکار: {source_link}\n🆔 @FavmeMusic"
                                
                                await app.copy_message(CHANNEL_ID, dialog.chat.id, message.id, caption=final_caption)
                                print(f"✅ Hunted from {source_name}: {message.audio.file_name}")
                                await asyncio.sleep(3)
                except:
                    continue

        state["history"] = state["history"][-2000:]
        with open(state_file, "w") as f: json.dump(state, f)
        print(f"--- ✨ Hunting Session Finished. Total: {count} ---")

if __name__ == "__main__":
    asyncio.run(music_hunter())
