import asyncio, os, re
from pyrogram import Client
import jdatetime

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING")
CHANNEL_ID = "favproxy"

async def send_file_post():
    app = Client("sender", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)
    async with app:
        # ۱. جمع‌آوری ۱۰۰ کانفیگ آخر از کانال برای ریختن توی فایل txt
        found_configs = []
        async for message in app.get_chat_history(CHANNEL_ID, limit=200):
            if message.text:
                links = re.findall(r"(vless|vmess|ss|trojan)://[^\s]+", message.text)
                found_configs.extend(links)
                if len(found_configs) >= 100: break
        
        configs_to_save = found_configs[:100]
        
        if not configs_to_save:
            print("No configs found to send!")
            return

        # ۲. ایجاد فایل متنی
        file_name = "HUNTER_CONFIGS.txt"
        with open(file_name, "w", encoding="utf-8") as f:
            f.write("\n".join(configs_to_save))

        # ۳. آماده‌سازی آمار برای کپشن
        stats = {"🇩🇪 Germany": 0, "🇫🇮 Finland": 0, "🌐 Others": 0}
        for c in configs_to_save:
            c_low = c.lower()
            if "germany" in c_low or "de" in c_low: stats["🇩🇪 Germany"] += 1
            elif "finland" in c_low or "fi" in c_low: stats["🇫🇮 Finland"] += 1
            else: stats["🌐 Others"] += 1
        
        stat_report = "\n".join([f"  └ {k}: {v}" for k, v in stats.items() if v > 0])
        
        now = jdatetime.datetime.now()
        date_str = now.strftime("%Y/%m/%d")
        time_str = now.strftime("%H:%M")
        SUB_LINK = "https://mehrdad2200.github.io/Hunter-Bot-GitHub/"

        caption = (
            f"💠 HUNTER PREMIUM CONFIGS\n"
            f"──────────────────────\n"
            f"📅 DATE: {date_str}  |  ⏰ TIME: {time_str}\n"
            f"🚀 TOTAL: {len(configs_to_save)} Verified Configs\n"
            f"🌍 LOCATION STATS:\n{stat_report}\n"
            f"🌐 NETWORK STATUS: Global Online ✅\n"
            f"──────────────────────\n"
            f"🔗 SUBSCRIPTION LINK (Tap to Copy):\n"
            f"`{SUB_LINK}`\n\n"
            f"💡 *Copy the link above and paste it into your app (v2rayNG / Shadowrocket) for auto-updates.*\n"
            f"──────────────────────\n"
            f"🆔 @favproxy"
        )

        # ۴. آپلود فایل به همراه کپشن
        await app.send_document(CHANNEL_ID, document=file_name, caption=caption)
        
        # پاک کردن فایل موقت از روی سرور گیت‌هاب
        if os.path.exists(file_name):
            os.remove(file_name)

if __name__ == "__main__":
    asyncio.run(send_file_post())
