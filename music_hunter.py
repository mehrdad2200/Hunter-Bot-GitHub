import asyncio, os, random, json, re
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

# منابعی که مهرداد فرستاد (اولویت اول)
PRIORITY_SOURCES = [
    "https://t.me/+750iUoFndkc5NDc8",
    "https://t.me/+TdHVAC-9SYAyMWI0",
    "musicbazpage",
    "InnerSpce"
]

async def generate_favme_style_text(file_name):
    """تولید متن به سبک کانال Favme: کوتاه، خاص و هنری"""
    prompt = f"""
    نام فایل موسیقی: {file_name}
    یک جمله بسیار کوتاه (حداکثر ۱۰ کلمه) بنویس که حال و هوای این آهنگ را توصیف کند.
    سبک نوشتن: هنری، کمی غمگین یا عاشقانه، شبیه کپشن پست های تلگرامی خاص. 
    اصلا نگو 'این آهنگ فلان است'. 
    مثال: 'غرق در سکوتِ میانِ نت‌ها.' یا 'انعکاسِ یک خاطره در شب.'
    فقط و فقط جمله را بنویس، بدون هیچ مقدمه یا هشتگ اضافی.
    """
    try:
        client = OpenAI(base_url="https://generativelanguage.googleapis.com/v1beta/openai/", api_key=KEYS["GEMINI"])
        resp = client.chat.completions.create(model="gemini-1.5-flash", messages=[{"role": "user", "content": prompt}])
        return resp.choices[0].message.content.strip()
    except:
        return ""

async def music_hunter():
    app = Client("music_hunter_bot", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)
    async with app:
        state_file = "hunter_state.json"
        
        # مدیریت وضعیت (تاریخچه و شماره پست دائمی)
        if os.path.exists(state_file):
            try:
                with open(state_file, "r") as f: state = json.load(f)
            except: state = {"history": [], "post_count": 0}
        else: state = {"history": [], "post_count": 0}
        
        state.setdefault("history", [])
        state.setdefault("post_count", 0)

        count_in_this_run = 0
        print(f"--- 🚀 Hunter Started. Starting from Post: {state['post_count'] + 1} ---")

        # اسکن منابع اولویت‌دار
        for source in PRIORITY_SOURCES:
            if count_in_this_run >= 50: break
            try:
                # ورود به لینک‌های خصوصی یا عمومی
                chat = await app.get_chat(source)
                async for message in app.get_chat_history(chat.id, limit=40):
                    if count_in_this_run >= 50: break
                    
                    if message.audio and message.audio.file_unique_id not in state["history"]:
                        f_id = message.audio.file_unique_id
                        state["history"].append(f_id)
                        state["post_count"] += 1
                        count_in_this_run += 1
                        
                        f_name = message.audio.file_name or "Unknown"
                        ai_text = await generate_favme_style_text(f_name)
                        
                        # فرمت کپشن دقیقاً طبق سلیقه مهرداد
                        source_display = f"@{chat.username}" if chat.username else chat.title
                        formatted_count = str(state["post_count"]).zfill(2) # تبدیل به 01, 02...
                        
                        caption = f"{formatted_count}. {ai_text}\n\n🔹 منبع: {source_display}\n🆔 @FavmeMusic"
                        
                        await app.copy_message(CHANNEL_ID, chat.id, message.id, caption=caption)
                        print(f"✅ Posted #{formatted_count}: {f_name}")
                        await asyncio.sleep(4)
            except Exception as e:
                print(f"Error on source {source}: {e}")
                continue

        # ذخیره نهایی وضعیت (تاریخچه و شماره آخرین پست)
        state["history"] = state["history"][-2000:]
        with open(state_file, "w") as f: json.dump(state, f)
        print(f"--- Finished! Next Post ID will be: {state['post_count'] + 1} ---")

if __name__ == "__main__":
    asyncio.run(music_hunter())
