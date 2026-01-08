import asyncio, os, re, base64
from pyrogram import Client
import jdatetime

# تنظیمات اصلی
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING")
CHANNEL_ID = "favproxy"

async def run_all_in_one():
    app = Client("hunter_bot", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)
    async with app:
        # ۱. اسکن ۱۰۰ لینک آخر از پست‌های کانال
        final_links = []
        async for message in app.get_chat_history(CHANNEL_ID, limit=500):
            if message.text:
                # استخراج لینک‌های خام
                links = re.findall(r"(vless|vmess|ss|trojan)://[^\s]+", message.text)
                for l in links:
                    if l not in final_links:
                        final_links.append(l)
                if len(final_links) >= 100:
                    break

        configs_list = final_links[:100]
        if not configs_list:
            print("No links found!")
            return

        # ۲. زمان ایران برای اسم فایل و کپشن
        now_ir = jdatetime.datetime.now()
        date_sh = now_ir.strftime("%Y/%m/%d")
        time_sh = now_ir.strftime("%H:%M")
        # اسم فایل: 1404-10-18_18-56.txt
        file_name = now_ir.strftime("%Y-%m-%d_%H-%M") + ".txt"

        # ۳. محتوای فایل (فقط لینک‌های خام پشت سر هم)
        file_body = "\n\n".join(configs_list)

        # ۴. آپدیت فایل ساب‌سکرایب برای گیت‌هاب
        raw_sub = "\n".join(configs_list)
        b64_sub = base64.b64encode(raw_sub.encode('utf-8')).decode('utf-8')
        with open("index.html", "w") as f:
            f.write(b64_sub)

        # ۵. ذخیره فایل تکست
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(file_body)

        # ۶. کپشن پست تلگرام
        sub_url = "https://mehrdad2200.github.io/Hunter-Bot-GitHub/"
        caption = (
            f"💠 HUNTER PREMIUM CONFIGS\n"
            f"──────────────────────\n"
            f"📅 DATE: {date_sh}  |  ⏰ TIME: {time_sh}\n"
            f"🚀 TOTAL: {len(configs_list)} Verified Configs\n"
            f"🌐 NETWORK STATUS: Global Online ✅\n"
            f"──────────────────────\n"
            f"🔗 SUBSCRIPTION LINK (Tap to Copy):\n"
            f"`{sub_url}`\n\n"
            f"💡 *Copy the link above and paste it into your app (v2rayNG / Shadowrocket) for auto-updates.*\n"
            f"──────────────────────\n"
            f"🆔 @favproxy"
        )

        # ۷. ارسال فایل و کپشن
        await app.send_document(CHANNEL_ID, document=file_name, caption=caption)
        
        if os.path.exists(file_name):
            os.remove(file_name)

if __name__ == "__main__":
    asyncio.run(run_all_in_one())
