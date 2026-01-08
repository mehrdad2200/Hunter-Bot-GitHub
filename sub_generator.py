import asyncio, os, re
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
                async for message in app.get_chat_history(source, limit=100):
                    if message.text:
                        # پیدا کردن تمام لینک‌های V2ray
                        links = re.findall(r"(vless|vmess|ss|trojan)://[^\s]+", message.text)
                        found_configs.extend(links)
            except: continue
        
        # حذف تکراری‌ها
        unique_configs = list(set(found_configs))
        
        if unique_configs:
            # ذخیره به صورت متن خام (دقیقاً مثل نمونه‌ای که فرستادی)
            # دیگه از base64 استفاده نمی‌کنیم
            raw_content = "\n".join(unique_configs)
            
            with open("index.html", "w", encoding="utf-8") as f:
                f.write(raw_content)
            print(f"✅ Sub updated with {len(unique_configs)} raw configs.")

if __name__ == "__main__":
    asyncio.run(get_configs())
