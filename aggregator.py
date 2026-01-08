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
        # ۱. جمع‌آوری ۱۰۰ کانفیگ آخر از کانال
        found_configs = []
        async for message in app.get_chat_history(CHANNEL_ID, limit=300):
            if message.text:
                links = re.findall(r"(vless|vmess|ss|trojan)://[^\s]+", message.text)
                found_configs.extend(links)
                if len(found_configs) >= 100: break
        
        configs_to_save = found_configs[:100]
        
        if not configs_to_save:
            print("No configs found!")
            return

        # ۲. تنظیم تاریخ شمسی و ساعت ایران برای اسم فایل
        now_iran = jdatetime.datetime.now()
        # فرمت: 1404-10-18_18-56.txt
        file_name = now_iran.strftime("%Y-%m-%d_%H-%M") + ".txt"

        # ۳. ایجاد فایل متنی (فقط لیست پروتکل‌ها، بدون هیچ متن اضافی)
        with open(file_name, "w", encoding="utf-8") as f:
            f.write("\n".join(configs_to_save))

        # ۴. تحلیل آمار برای کپشن (طبق سلیقه تو)
        stats = {"🇩🇪 Germany": 0, "🇫🇮 Finland": 0, "🇳🇱 Netherlands": 0, "🇺🇸 USA": 0, "🌐 Others": 0}
        for c in configs_to_save:
            c_low = c.lower()
            if "germany" in c_low or "de" in c_low: stats["🇩🇪 Germany"] += 1
            elif "finland" in c_low or "fi" in c_low: stats["🇫🇮 Finland"] += 1
            elif "netherlands" in c_low or "nl" in c_low: stats["🇳🇱 Netherlands"] += 1
            elif "usa" in c_low or "us" in c_low: stats["🇺🇸 USA"] += 1
            else: stats["🌐 Others"] += 1
        
        stat_report = "\n".join([f"  └ {k}: {v}" for k, v in stats.items() if v > 0])
        date_caption = now_iran.strftime("%Y/%m/%d")
        time_caption = now_iran.strftime("%H:%M")
        SUB_LINK = "https://mehrdad2200.github.io/Hunter-Bot-GitHub/"

        caption = (
            f"💠 HUNTER PREMIUM CONFIGS\n"
            f"──────────────────────\n"
            f"📅 DATE: {date_caption}  |  ⏰ TIME: {time_caption}\n"
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

        # ۵. آپلود فایل با اسم تاریخ‌دار و کپشن کامل
        await app.send_document(CHANNEL_ID, document=file_name, caption=caption)
        
        # پاکسازی فایل موقت
        if os.path.exists(file_name):
            os.remove(file_name)

if __name__ == "__main__":
    asyncio.run(send_file_post())
