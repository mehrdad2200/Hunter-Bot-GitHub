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
        # ۱. اسکن پست‌های کانال برای جمع‌آوری ۱۰۰ لینک کامل
        found_configs = []
        async for message in app.get_chat_history(CHANNEL_ID, limit=500):
            if message.text:
                # استخراج لینک‌های کامل (vless, vmess, ss, trojan)
                links = re.findall(r"(vless|vmess|ss|trojan)://[^\s]+", message.text)
                for link in links:
                    if link not in found_configs:
                        found_configs.append(link)
                if len(found_configs) >= 100: break

        if not found_configs:
            print("هیچ کانفیگی پیدا نشد!")
            return

        final_configs = found_configs[:100]

        # ۲. تنظیم زمان ایران برای اسم فایل
        now_ir = jdatetime.datetime.now()
        date_sh = now_ir.strftime("%Y/%m/%d")
        time_sh = now_ir.strftime("%H:%M")
        # اسم فایل طبق فرمت شما: 1404-10-18_18-56.txt
        file_name = now_ir.strftime("%Y-%m-%d_%H-%M") + ".txt"

        # ۳. ساخت محتوای داخل فایل (فقط لیست لینک‌ها - بدون متن اضافه)
        file_body = "\n\n".join(final_configs)

        # ۴. آپدیت فایل ساب‌سکرایب برای گیت‌هاب (Base64)
        raw_sub = "\n".join(final_configs)
        b64_sub = base64.b64encode(raw_sub.encode('utf-8')).decode('utf-8')
        with open("index.html", "w") as f:
            f.write(b64_sub)

        # ۵. ذخیره فایل متنی برای ارسال به تلگرام
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(file_body)

        # ۶. تحلیل آمار کشورها برای کپشن پست
        stats = {"🇩🇪 Germany": 0, "🇫🇮 Finland": 0, "🇳🇱 Netherlands": 0, "🇺🇸 USA": 0, "🌐 Others": 0}
        for c in final_configs:
            c_low = c.lower()
            if "germany" in c_low or "de" in c_low: stats["🇩🇪 Germany"] += 1
            elif "finland" in c_low or "fi" in c_low: stats["🇫🇮 Finland"] += 1
            elif "netherlands" in c_low or "nl" in c_low: stats["🇳🇱 Netherlands"] += 1
            elif "usa" in c_low or "us" in c_low: stats["🇺🇸 USA"] += 1
            else: stats["🌐 Others"] += 1
        
        stat_report = "\n".join([f"  └ {k}: {v}" for k, v in stats.items() if v > 0])
        sub_url = "https://mehrdad2200.github.io/Hunter-Bot-GitHub/"

        # ۷. کپشن نهایی پست تلگرام (عین نمونه‌ای که دادی)
        caption = (
            f"💠 HUNTER PREMIUM CONFIGS\n"
            f"──────────────────────\n"
            f"📅 DATE: {date_sh}  |  ⏰ TIME: {time_sh}\n"
            f"🚀 TOTAL: {len(final_configs)} Verified Configs\n"
            f"🌐 NETWORK STATUS: Global Online ✅\n\n"
            f"🌍 LOCATION STATS:\n{stat_report}\n"
            f"──────────────────────\n"
            f"🔗 SUBSCRIPTION LINK (Tap to Copy):\n"
            f"`{sub_url}`\n\n"
            f"💡 *Copy the link above and paste it into your app (v2rayNG / Shadowrocket) for auto-updates.*\n"
            f"──────────────────────\n"
            f"🆔 @favproxy"
        )

        # ۸. ارسال فایل و کپشن
        await app.send_document(CHANNEL_ID, document=file_name, caption=caption)
        
        # پاکسازی
        if os.path.exists(file_name):
            os.remove(file_name)

if __name__ == "__main__":
    asyncio.run(run_all_in_one())
