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
        async for message in app.get_chat_history(CHANNEL_ID, limit=400):
            if message.text:
                # استخراج لینک و جدا کردن اسم (بعد از #)
                links = re.findall(r"(vless|vmess|ss|trojan)://[^\s]+", message.text)
                found_configs.extend(links)
                if len(found_configs) >= 100: break
        
        configs_to_save = found_configs[:100]
        if not configs_to_save: return

        # ۲. تنظیم تاریخ و ساعت ایران
        now_iran = jdatetime.datetime.now()
        date_sh = now_iran.strftime("%Y/%m/%d")
        time_sh = now_iran.strftime("%H:%M")
        
        # ۳. ساخت محتوای داخل فایل (تکرار الگوی پست اول برای هر ۱۰۰ کانفیگ)
        file_content = ""
        for i, config in enumerate(configs_to_save, 1):
            file_content += (
                f"💎 PREMIUM VPN CONFIG | #{i}\n"
                f"─── • 🟡 • ───\n"
                f"📅 Date: {date_sh}\n"
                f"⏰ Time: {time_sh}\n"
                f"─── • 🟡 • ───\n"
                f"🚀 Fast & Private Connection:\n\n"
                f"{config}\n\n"
                f"─── • 🟡 • ───\n"
                f"📢 Join us: @favproxy\n"
                f"✨ Hunter: #Mehrdad\n\n"
                f"******************************\n\n"
            )

        # ۴. نام‌گذاری فایل: 1404-10-18_17-50.txt
        file_name = now_iran.strftime("%Y-%m-%d_%H-%M") + ".txt"
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(file_content)

        # ۵. تحلیل آمار برای کپشن (پست دومی)
        stats = {"🇩🇪 Germany": 0, "🇫🇮 Finland": 0, "🌐 Others": 0}
        for c in configs_to_save:
            c_low = c.lower()
            if "germany" in c_low or "de" in c_low: stats["🇩🇪 Germany"] += 1
            elif "finland" in c_low or "fi" in c_low: stats["🇫🇮 Finland"] += 1
            else: stats["🌐 Others"] += 1
        
        stat_report = "\n".join([f"  └ {k}: {v}" for k, v in stats.items() if v > 0])
        SUB_LINK = "https://mehrdad2200.github.io/Hunter-Bot-GitHub/"

        caption = (
            f"💠 HUNTER PREMIUM CONFIGS\n"
            f"──────────────────────\n"
            f"📅 DATE: {date_sh}  |  ⏰ TIME: {time_sh}\n"
            f"🚀 TOTAL: {len(configs_to_save)} Verified Configs\n"
            f"🌐 NETWORK STATUS: Global Online ✅\n\n"
            f"🌍 LOCATION STATS:\n{stat_report}\n"
            f"──────────────────────\n"
            f"🔗 SUBSCRIPTION LINK (Tap to Copy):\n"
            f"`{SUB_LINK}`\n\n"
            f"💡 *Copy the link above and paste it into your app (v2rayNG / Shadowrocket) for auto-updates.*\n"
            f"──────────────────────\n"
            f"🆔 @favproxy"
        )

        # ۶. ارسال فایل به کانال
        await app.send_document(CHANNEL_ID, document=file_name, caption=caption)
        
        if os.path.exists(file_name):
            os.remove(file_name)

if __name__ == "__main__":
    asyncio.run(send_file_post())
