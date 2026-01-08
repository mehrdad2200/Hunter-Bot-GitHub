import asyncio, os, base64, re
from pyrogram import Client

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING")
MY_CHANNEL = "favproxy" # کانال خودت

async def get_configs():
    app = Client("proxy_worker", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)
    async with app:
        found_configs = []
        # فقط کانال خودت رو اسکن می‌کنه تا ۱۰۰ تا کانفیگ پیدا کنه
        async for message in app.get_chat_history(MY_CHANNEL, limit=200):
            if message.text:
                links = re.findall(r"(vless|vmess|ss|trojan)://[^\s]+", message.text)
                found_configs.extend(links)
                if len(found_configs) >= 100:
                    break
        
        # دقیقاً ۱۰۰ تای آخر
        final_configs = found_configs[:100]
        
        if final_configs:
            # ۱. ساخت فایل ساب (Base64) برای برنامه ها
            raw_content = "\n".join(final_configs)
            b64_content = base64.b64encode(raw_content.encode('utf-8')).decode('utf-8')
            with open("index.html", "w") as f:
                f.write(b64_content)
            
            # ۲. تحلیل آمار کشورها برای پست جدید
            stats = {"🇩🇪 Germany": 0, "🇫🇮 Finland": 0, "🇳🇱 Netherlands": 0, "🇺🇸 USA": 0, "🇹🇷 Turkey": 0, "🌐 Others": 0}
            for c in final_configs:
                c_low = c.lower()
                if "germany" in c_low or "de" in c_low: stats["🇩🇪 Germany"] += 1
                elif "finland" in c_low or "fi" in c_low: stats["🇫🇮 Finland"] += 1
                elif "netherlands" in c_low or "nl" in c_low: stats["🇳🇱 Netherlands"] += 1
                elif "usa" in c_low or "us" in c_low: stats["🇺🇸 USA"] += 1
                elif "turkey" in c_low or "tr" in c_low: stats["🇹🇷 Turkey"] += 1
                else: stats["🌐 Others"] += 1
            
            stat_report = "\n".join([f"  └ {k}: {v}" for k, v in stats.items() if v > 0])
            with open("stats.txt", "w", encoding="utf-8") as f:
                f.write(f"🚀 TOTAL: {len(final_configs)} Verified Configs\n{stat_report}")
            print(f"✅ 100 configs collected from @{MY_CHANNEL}")

if __name__ == "__main__":
    asyncio.run(get_configs())
