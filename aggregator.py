import asyncio, os, jdatetime, re, random
from pyrogram import Client
from datetime import datetime, timedelta, timezone

# GitHub Secrets
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING")
CHANNEL_ID = "favproxy" # آیدی کانال خودت بدون @

app = Client("aggregator", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)

def get_iran_time():
    ir_tz = timezone(timedelta(hours=3, minutes=30))
    now = datetime.now(timezone.utc).astimezone(ir_tz)
    shamsi = jdatetime.datetime.fromgregorian(datetime=now)
    return shamsi.strftime("%Y/%m/%d"), shamsi.strftime("%H:%M")

async def collect_and_upload():
    async with app:
        configs = []
        one_hour_ago = datetime.now(timezone.utc) - timedelta(hours=1)
        
        # جمع‌آوری پیام‌های یک ساعت اخیر
        async for message in app.get_chat_history(CHANNEL_ID, limit=200):
            if message.date.replace(tzinfo=timezone.utc) < one_hour_ago:
                break
            if message.text:
                # استخراج لینک‌های V2ray
                links = re.findall(r'(?:vless|vmess|trojan|ss)://[^\s"\'<>]+', message.text)
                configs.extend(links)

        if not configs:
            print("No configs found in the last hour.")
            return

        unique_configs = list(set(configs)) # حذف تکراری‌ها
        date_str, time_str = get_iran_time()

        # لیست کپشن‌های گرافیکی خفن و رندوم
        captions = [
            f"🚀 **V2RAY HOURLY UPDATE**\n\n📅 Date: `{date_str}`\n⏰ Time: `{time_str}`\n💎 Total: `{len(unique_configs)}` Configs\n\n⚡️ @{CHANNEL_ID}",
            f"📦 **NEW CONFIG PACK**\n\n📅 تاریخ: `{date_str}`\n🕒 ساعت: `{time_str}`\n✅ تعداد کانفیگ: `{len(unique_configs)}` عدد\n\n🛡 @{CHANNEL_ID}",
            f"🔥 **SUPER FAST CONFIGS**\n\n📆 `{date_str}` | 🕒 `{time_str}`\n✨ Total: `{len(unique_configs)}` New Links\n\n📥 Download file below ↓\n\n🆔 @{CHANNEL_ID}"
        ]
        
        selected_caption = random.choice(captions)

        # ساخت فایل متنی
        file_name = f"Configs_{time_str.replace(':', '-')}.txt"
        with open(file_name, "w", encoding="utf-8") as f:
            f.write("\n\n".join(unique_configs))

        # ارسال فایل به کانال
        await app.send_document(
            CHANNEL_ID, 
            document=file_name, 
            caption=selected_caption
        )
        
        # پاک کردن فایل از سرور بعد از ارسال
        os.remove(file_name)

if __name__ == "__main__":
    app.run(collect_and_upload())
