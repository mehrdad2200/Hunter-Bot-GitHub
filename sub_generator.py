import asyncio, os, base64, re
from pyrogram import Client

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING")

SOURCES = ["v2ray_outline_config", "V2rayNG_VPNN", "iSegaro", "v2rayNG_Config"]

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
        
        unique_configs = list(dict.fromkeys(found_configs))
        if unique_configs:
            # ۱. ساخت فایل ساب (Base64) برای برنامه ها
            raw_content = "\n".join(unique_configs)
            b64_content = base64.b64encode(raw_content.encode('utf-8')).decode('utf-8')
            with open("index.html", "w") as f:
                f.write(b64_content)
            
            # ۲. تحلیل کشورها برای گزارش تلگرام (بر اساس اسم کانفیگ)
            stats = {"🇩🇪 Germany": 0, "🇫🇮 Finland": 0, "🇳🇱 Netherlands": 0, "🇺🇸 USA": 0, "🇹🇷 Turkey": 0, "🌐 Others": 0}
            for c in unique_configs:
                c_low = c.lower()
                if "germany" in c_low or " de " in c_low: stats["🇩🇪 Germany"] += 1
                elif "finland" in c_low or " fi " in c_low: stats["🇫🇮 Finland"] += 1
                elif "netherlands" in c_low or " nl " in c_low: stats["🇳🇱 Netherlands"] += 1
                elif "usa" in c_low or " us " in c_low: stats["🇺🇸 USA"] += 1
                elif "turkey" in c_low or " tr " in c_low: stats["🇹🇷 Turkey"] += 1
                else: stats["🌐 Others"] += 1
            
            # ذخیره آمار در یک فایل موقت برای استفاده در بات تلگرام
            with open("stats.txt", "w", encoding="utf-8") as f:
                stat_text = "\n".join([f"  └ {k}: {v}" for k, v in stats.items() if v > 0])
                f.write(f"🚀 TOTAL: {len(unique_configs)} Verified Configs\n{stat_text}")

if __name__ == "__main__":
    asyncio.run(get_configs())
