import asyncio, os, jdatetime
from pyrogram import Client
from datetime import datetime, timedelta, timezone

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
    if not os.path.exists("validated_configs.txt"): return
    with open("validated_configs.txt", "r", encoding="utf-8") as f:
        unique_configs = f.read().splitlines()
    if not unique_configs: return

    async with app:
        date_str, time_str = get_iran_time()
        sub_link = "https://mehrdad2200.github.io/Hunter-Bot-GitHub/"
        caption_text = (
            f"💠 **HUNTER PREMIUM CONFIGS**\n"
            f"──────────────────────\n"
            f"📅 **DATE:** `{date_str}`\n"
            f"⏰ **TIME:** `{time_str}`\n"
            f"🚀 **TOTAL:** `{len(unique_configs)}` Healthy Configs\n"
            f"──────────────────────\n"
            f"🔗 **SUBSCRIPTION LINK (Tap to Copy):**\n"
            f"`{sub_link}`\n\n"
            f"💡 *Paste this link in v2rayNG or Shadowrocket.*\n"
            f"──────────────────────\n"
            f"🆔 @{CHANNEL_ID}"
        )
        file_name = f"{date_str.replace('/', '-')}_{time_str.replace(':', '-')}.txt"
        with open(file_name, "w", encoding="utf-8") as f:
            f.write("\n\n".join(unique_configs))
        await app.send_document(CHANNEL_ID, document=file_name, caption=caption_text)
        os.remove(file_name)

if __name__ == "__main__":
    app.run(collect_and_upload())
