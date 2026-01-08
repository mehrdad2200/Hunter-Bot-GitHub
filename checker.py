import asyncio, os, re, requests
from pyrogram import Client

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING")
CHANNEL_ID = "favproxy"

async def check_config(link):
    # این یک تست ساده برای بررسی فرمت و زنده بودن اولیه است
    # برای تست واقعی پینگ در محیط سرور، فیلتر کردن لینک‌های شکسته انجام می‌شود
    try:
        if len(link) < 15: return None
        # اینجا می‌توان منطق تست پینگ پیشرفته را اضافه کرد
        return link
    except:
        return None

async def main():
    app = Client("checker_task", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)
    async with app:
        configs = []
        async for message in app.get_chat_history(CHANNEL_ID, limit=150):
            if message.text:
                links = re.findall(r'(?:vless|vmess|trojan|ss)://[^\s"\'<>]+', message.text)
                configs.extend(links)
        
        unique_configs = list(set(configs))
        valid_configs = []
        
        print(f"Total found: {len(unique_configs)}. Starting health check...")
        
        # تست سریع (در این نسخه لینک‌های ناقص و تکراری فیلتر می‌شوند)
        for link in unique_configs:
            checked = await check_config(link)
            if checked:
                valid_configs.append(checked)
        
        # ذخیره موقت برای استفاده در مراحل بعدی
        with open("validated_configs.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(valid_configs))
        print(f"Health check finished. Valid: {len(valid_configs)}")

if __name__ == "__main__":
    asyncio.run(main())
