import asyncio, os, re
from pyrogram import Client

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING")
CHANNEL_ID = "favproxy"

async def main():
    app = Client("checker_task", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)
    async with app:
        configs = []
        async for message in app.get_chat_history(CHANNEL_ID, limit=150):
            if message.text:
                links = re.findall(r'(?:vless|vmess|trojan|ss)://[^\s"\'<>]+', message.text)
                configs.extend(links)
        
        unique_configs = list(set(configs))
        valid_configs = [link for link in unique_configs if len(link) > 25]
        
        # ذخیره کانفیگ‌های تایید شده
        with open("validated_configs.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(valid_configs))
            
        # ذخیره آمار ساعتی در یک فایل متنی (برای گزارش شبانه)
        with open("hourly_stats.log", "a") as f:
            f.write(f"{len(valid_configs)}\n")

if __name__ == "__main__":
    asyncio.run(main())
