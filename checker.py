import asyncio, os, re
from pyrogram import Client

# تنظیمات از گیت‌هاب سکرت
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING")
CHANNEL_ID = "favproxy"

async def main():
    app = Client("checker_task", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)
    async with app:
        configs = []
        # بررسی پیام‌های اخیر کانال
        async for message in app.get_chat_history(CHANNEL_ID, limit=150):
            if message.text:
                # استخراج لینک‌های v2ray
                links = re.findall(r'(?:vless|vmess|trojan|ss)://[^\s"\'<>]+', message.text)
                configs.extend(links)
        
        # حذف تکراری‌ها
        unique_configs = list(set(configs))
        valid_configs = []
        
        # فیلتر اولیه (لینک‌های بسیار کوتاه یا ناقص حذف می‌شوند)
        for link in unique_configs:
            if len(link) > 25: 
                valid_configs.append(link)
        
        # ذخیره در فایل واسط برای بقیه اسکریپت‌ها
        with open("validated_configs.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(valid_configs))
        
        print(f"Done! Found {len(valid_configs)} valid configs.")

if __name__ == "__main__":
    asyncio.run(main())
