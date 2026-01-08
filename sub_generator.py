import asyncio, os, re
from pyrogram import Client

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING")
CHANNEL_ID = "favproxy"

app = Client("sub_gen", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)

async def generate_sub():
    async with app:
        configs = []
        # ۱۰۰ پیام آخر کانال برای ساب‌لینک
        async for message in app.get_chat_history(CHANNEL_ID, limit=100):
            if message.text:
                links = re.findall(r'(?:vless|vmess|trojan|ss)://[^\s"\'<>]+', message.text)
                configs.extend(links)

        unique_configs = list(set(configs))
        with open("index.html", "w", encoding="utf-8") as f:
            f.write("\n".join(unique_configs))

if __name__ == "__main__":
    app.run(generate_sub())
