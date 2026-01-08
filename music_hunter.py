import asyncio, os, random, json
from pyrogram import Client
from openai import OpenAI

# تنظیمات اصلی
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING")
# پیشنهاد: آیدی عددی کانال را بگذار (مثلاً -100123456789) اگر یوزرنیم کار نکرد
CHANNEL_ID = "FavmeMusic" 

KEYS = {
    "GEMINI": os.environ.get("GEMINI_KEY"),
    "GROQ": os.environ.get("GROQ_KEY"),
    "CEREBRAS": os.environ.get("CEREBRAS_KEY"),
    "OPENROUTER": os.environ.get("OPENROUTER_KEY")
}

async def generate_human_text(prompt):
    if KEYS["GEMINI"]:
        try:
            client = OpenAI(base_url="https://generativelanguage.googleapis.com/v1beta/openai/", api_key=KEYS["GEMINI"])
            resp = client.chat.completions.create(model="gemini-1.5-flash", messages=[{"role": "user", "content": prompt}])
            return resp.choices[0].message.content
        except: pass
    
    # لایه رزرو (Groq)
    if KEYS["GROQ"]:
        try:
            client = OpenAI(base_url="https://api.groq.com/openai/v1", api_key=KEYS["GROQ"])
            resp = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model="llama-3.3-70b-versatile")
            return resp.choices[0].message.content
        except: pass
    return "یک قطعه موسیقی پیشنهادی برای شما."

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
        
        # کوئری‌های بسیار قوی برای تحریک موتور جستجوی تلگرام
        search_terms = ["t.me/", "https://t.me/", ".mp3", "music", "جدید", "آهنگ", "track", "remix"]
        random.shuffle(search_terms)
        
        count = 0
        sources_this_run = []

        print("--- 🛰 Global Scanning in Progress ---")

        for query in search_terms:
            if count >= 50: break
            
            try:
                # استفاده از افست رندوم برای اینکه هر بار نتایج متفاوتی از کل تلگرام بگیرد
                async for message in app.search_global(query, limit=100):
                    if count >= 50: break
                    
                    # شرط: حتما فایل صوتی باشد و از چت‌های شخصی نباشد (فقط کانال‌های عمومی)
                    if message.audio and str(message.chat.type) in ["ChatType.CHANNEL", "channel"]:
                        f_id = message.audio.file_unique_id
                        chat_id = message.chat.id
                        
                        if f_id not in state["history"] and chat_id not in sources_this_run:
                            source_display = f"@{message.chat.username}" if message.chat.username else message.chat.title
                            
                            count += 1
                            state["history"].append(f_id)
                            sources_this_run.append(chat_id)
                            
                            f_name = message.audio.file_name or "Unknown"
                            prompt = f"فایل '{f_name}'. معرفی ۳ خطی صمیمی فارسی. آخرش هشتگ خواننده و سبک."
                            
                            ai_text = await generate_human_text(prompt)
                            final_caption = f"{ai_text}\n\n🔹 منبع شکار: {source_display}\n🆔 @FavmeMusic"
                            
                            await app.copy_message(CHANNEL_ID, message.chat.id, message.id, caption=final_caption)
                            print(f"✅ Found & Posted: {f_name} from {source_display}")
                            await asyncio.sleep(4) 
            except Exception as e:
                print(f"Error on query {query}: {e}")
                continue

        state["history"] = state["history"][-2000:]
        with open(state_file, "w") as f: json.dump(state, f)

if __name__ == "__main__":
    asyncio.run(music_hunter())
