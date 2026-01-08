import asyncio, os, base64, re
from pyrogram import Client

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING")

SOURCES = [
    "v2ray_outline_config", "V2rayNG_VPNN", "v2ray_swat", 
    "FreeVlessConfig", "v2rayNG_Config", "iSegaro"
]

async def get_configs():
    app = Client("proxy_worker", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)
    async with app:
        found_configs = []
        for source in SOURCES:
            try:
                async for message in app.get_chat_history(source, limit=50):
                    if message.text:
                        links = re.findall(r"(vless|vmess|ss|trojan)://[^\s]+", message.text)
                        found_configs.extend(links)
            except: continue
        
        unique_configs = list(set(found_configs))
        if unique_configs:
            raw_content = "\n".join(unique_configs)
            b64_content = base64.b64encode(raw_content.encode('utf-8')).decode('utf-8')
            with open("index.html", "w") as f:
                f.write(b64_content)
            print(f"✅ Sub updated with {len(unique_configs)} configs.")

if __name__ == "__main__":
    asyncio.run(get_configs())
