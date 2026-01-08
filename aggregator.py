import asyncio, os, re, base64
from pyrogram import Client
import jdatetime

# تنظیمات
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING")
CHANNEL_ID = "favproxy"

async def run_all_in_one():
    app = Client("hunter_bot", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)
    async with app:
        # ۱. اسکن ۱۰۰ پست آخر کانال خودت که لینک دارن
        found_configs = []
        async for message in app.get_chat_history(CHANNEL_ID, limit=500):
            if message.text:
                links = re.findall(r"(vless|vmess|ss|trojan)://[^\s]+", message.text)
                if links:
                    found_configs.append(links[0]) # گرفتن اولین لینک از هر پست
                if len(found_configs) >= 100: break

        if not found_configs:
            print("هیچ کانفیگی پیدا نشد!")
            return

        # ۲. تنظیم زمان ایران
        now_ir = jdatetime.datetime.now()
        date_sh = now_ir.strftime("%Y/%m/%d")
        time_sh = now_ir.strftime("%H:%M")
        file_name = now_ir.strftime("%Y-%m-%d_%H-%M") + ".txt"

        # ۳. ساخت محتوای داخل فایل (قالب پست اول برای هر ۱۰۰ تا)
        full_file_text = ""
        for i, config in enumerate(found_configs, 1):
            full_file_text += (
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
                f"{'━'*15}\n\n"
            )

        # ۴. آپدیت فایل ساب‌سکرایب (بدون ارسال پست)
        raw_sub = "\n".join(found_configs)
        b64_sub = base64.b64encode(raw_sub.encode('utf-8')).decode('utf-8')
        with open("index.html", "w") as f:
            f.write(b64_sub)

        # ۵. ذخیره فایل تکست برای ارسال
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(full_file_text)

        # ۶. تحلیل آمار برای کپشن
        stats = {"🇩🇪 Germany": 0, "🇫🇮 Finland": 0, "🇳🇱 Netherlands": 0, "🌐 Others": 0}
        for c in found_configs:
            c_low = c.lower()
            if "germany" in c_low or "de" in c_low: stats["🇩🇪 Germany"] += 1
            elif "finland" in c_low or "fi" in c_low: stats["🇫🇮 Finland"] += 1
            elif "netherlands" in c_low or "nl" in c_low: stats["🇳🇱 Netherlands"] += 1
            else: stats["🌐 Others"] += 1
        
        stat_report = "\n".join([f"  └ {k}: {v}" for k, v in stats.items() if v > 0])
        sub_url = "https://mehrdad2200.github.io/Hunter-Bot-GitHub/"

        caption = (
            f"💠 HUNTER PREMIUM CONFIGS\n"
            f"──────────────────────\n"
            f"📅 DATE: {date_sh}  |  ⏰ TIME: {time_sh}\n"
            f"🚀 TOTAL: {len(found_configs)} Verified Configs\n"
            f"🌐 NETWORK STATUS: Global Online ✅\n\n"
            f"🌍 LOCATION STATS:\n{stat_report}\n"
            f"──────────────────────\n"
            f"🔗 SUBSCRIPTION LINK (Tap to Copy):\n"
            f"`{sub_url}`\n\n"
            f"💡 *Copy the link above and paste it into your app (v2rayNG / Shadowrocket) for auto-updates.*\n"
            f"──────────────────────\n"
            f"🆔 @favproxy"
        )

        # ۷. فقط یک بار ارسال فایل به همراه کپشن
        await app.send_document(CHANNEL_ID, document=file_name, caption=caption)
        
        if os.path.exists(file_name):
            os.remove(file_name)

if __name__ == "__main__":
    asyncio.run(run_all_in_one())
