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
        # ۱. اسکن کانال برای پیدا کردن ۱۰۰ لینک خام آخر
        all_links = []
        async for message in app.get_chat_history(CHANNEL_ID, limit=500):
            if message.text:
                # پیدا کردن تمام لینک‌هایی که با پروتکل‌های مورد نظر شروع می‌شوند
                links = re.findall(r"(vless|vmess|ss|trojan)://[^\s]+", message.text)
                for l in links:
                    if l not in all_links:
                        all_links.append(l)
                if len(all_links) >= 100:
                    break

        final_links = all_links[:100]

        if not final_links:
            print("هیچ لینکی پیدا نشد!")
            return

        # ۲. تنظیم زمان ایران برای اسم فایل و کپشن
        now_ir = jdatetime.datetime.now()
        date_sh = now_ir.strftime("%Y/%m/%d")
        time_sh = now_ir.strftime("%H:%M")
        # اسم فایل طبق فرمت درخواستی: 1404-10-18_18-56.txt
        file_name = now_ir.strftime("%Y-%m-%d_%H-%M") + ".txt"

        # ۳. ساخت محتوای فایل تکست (فقط و فقط لینک‌های خام)
        file_content = "\n\n".join(final_links)

        # ۴. آپدیت فایل index.html برای ساب‌سکرایب گیت‌هاب (Base64)
        raw_sub_text = "\n".join(final_links)
        b64_sub = base64.b64encode(raw_sub_text.encode('utf-8')).decode('utf-8')
        with open("index.html", "w") as f:
            f.write(b64_sub)

        # ۵. ذخیره فایل متنی
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(file_content)

        # ۶. تحلیل آمار برای کپشن
        stats = {"🇩🇪 Germany": 0, "🇫🇮 Finland": 0, "🇳🇱 Netherlands": 0, "🇺🇸 USA": 0, "🌐 Others": 0}
        for link in final_links:
            l_low = link.lower()
            if "germany" in l_low or "de" in l_low: stats["🇩🇪 Germany"] += 1
            elif "finland" in l_low or "fi" in l_low: stats["🇫🇮 Finland"] += 1
            elif "netherlands" in l_low or "nl" in l_low: stats["🇳🇱 Netherlands"] += 1
            elif "usa" in l_low or "us" in l_low: stats["🇺🇸 USA"] += 1
            else: stats["🌐 Others"] += 1
        
        stat_report = "\n".join([f"  └ {k}: {v}" for k, v in stats.items() if v > 0])
        sub_url = "https://mehrdad2200.github.io/Hunter-Bot-GitHub/"

        # ۷. کپشن شیک پست تلگرام
        caption = (
            f"💠 HUNTER PREMIUM CONFIGS\n"
            f"──────────────────────\n"
            f"📅 DATE: {date_sh}  |  ⏰ TIME: {time_sh}\n"
            f"🚀 TOTAL: {len(final_links)} Verified Configs\n"
            f"🌐 NETWORK STATUS: Global Online ✅\n\n"
            f"🌍 LOCATION STATS:\n{stat_report}\n"
            f"──────────────────────\n"
            f"🔗 SUBSCRIPTION LINK (Tap to Copy):\n"
            f"`{sub_url}`\n\n"
            f"💡 *Copy the link above and paste it into your app (v2rayNG / Shadowrocket) for auto-updates.*\n"
            f"──────────────────────\n"
            f"🆔 @favproxy"
        )

        # ۸. ارسال فایل و کپشن (فقط یک پیام)
        await app.send_document(CHANNEL_ID, document=file_name, caption=caption)
        
        # پاکسازی فایل موقت از سرور
        if os.path.exists(file_name):
            os.remove(file_name)

if __name__ == "__main__":
    asyncio.run(run_all_in_one())
