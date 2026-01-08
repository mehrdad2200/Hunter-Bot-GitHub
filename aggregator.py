import asyncio, os, jdatetime, re, random
from pyrogram import Client
from datetime import datetime, timedelta, timezone

# GitHub Secrets
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING")
CHANNEL_ID = "favproxy"

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
        
        async for message in app.get_chat_history(CHANNEL_ID, limit=200):
            if message.date.replace(tzinfo=timezone.utc) < one_hour_ago:
                break
            if message.text:
                links = re.findall(r'(?:vless|vmess|trojan|ss)://[^\s"\'<>]+', message.text)
                configs.extend(links)

        if not configs: return

        unique_configs = list(set(configs))
        date_str, time_str = get_iran_time()
        sub_link = f"https://mehrdad2200.github.io/Hunter-Bot-GitHub/"

        # کپشن مدرن و شیک با قابلیت کپی سریع لینک
        caption_text = (
            f"💠 **HUNTER PREMIUM CONFIGS**\n"
            f"──────────────────────\n"
            f"📅 **DATE:** `{date_str}`\n"
            f"⏰ **TIME:** `{time_str}`\n"
            f"🚀 **TOTAL:** `{len(unique_configs)}` Configs\n"
            f"──────────────────────\n"
            f"🔗 **SUBSCRIPTION LINK (Tap to Copy):**\n"
            f"`{sub_link}`\n\n"
            f"💡 *Copy the link above and paste it into your app (v2rayNG / Shadowrocket) for auto-updates.*\n"
            f"──────────────────────\n"
            f"🆔 @{CHANNEL_ID}"
        )

        # نام فایل: 1404-10-20_08-49.txt
        file_name = f"{date_str.replace('/', '-')}_{time_str.replace(':', '-')}.txt"

        with open(file_name, "w", encoding="utf-8") as f:
            f.write("\n\n".join(unique_configs))

        await app.send_document(CHANNEL_ID, document=file_name, caption=caption_text)
        os.remove(file_name)

if __name__ == "__main__":
    app.run(collect_and_upload())
