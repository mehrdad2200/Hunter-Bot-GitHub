import requests, re, random, asyncio, jdatetime, os
from datetime import datetime, timezone, timedelta
from pyrogram import Client

# دریافت امن اطلاعات از Secrets گیت‌هاب
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING")
CHANNEL_ID = "favproxy" 

SOURCES = [
    "https://raw.githubusercontent.com/parvinxs/Submahsanetxsparvin/refs/heads/main/Sub.mahsa.xsparvin",
    "https://github.com/Joker-funland/V2ray-configs/raw/main/configs"
]

def get_iran_time_date():
    ir_tz = timezone(timedelta(hours=3, minutes=30))
    now_ir = datetime.now(timezone.utc).astimezone(ir_tz)
    shamsi = jdatetime.datetime.fromgregorian(datetime=now_ir)
    return shamsi.strftime("%Y/%m/%d"), shamsi.strftime("%H:%M")

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)

async def scan_and_send():
    date_now, time_now = get_iran_time_date()
    all_found = []
    for url in SOURCES:
        try:
            r = requests.get(f"{url}?v={random.random()}", timeout=15)
            if r.status_code == 200:
                found = re.findall(r'(?:vless|vmess|trojan|ss)://[^\s"\'<>]+', r.text)
                all_found.extend(found)
        except: continue

    if not all_found: return
    
    random.shuffle(all_found)
    selected = list(set(all_found))[:20] # ۲۰ عدد کانفیگ تازه

    for index, config in enumerate(selected, 1):
        message_text = (
            f"💎 **PREMIUM VPN CONFIG | #{index:02}**\n"
            f"─── • 🟡 • ───\n"
            f"📅 **Date:** `{date_now}`\n"
            f"⏰ **Time:** `{time_now}`\n"
            f"─── • 🟡 • ───\n"
            f"🚀 **Fast & Private Connection:**\n"
            f"```\n{config}\n```\n"
            f"─── • 🟡 • ───\n"
            f"📢 **Join us:** @{CHANNEL_ID}\n"
            f"✨ **Hunter:** #Mehrdad"
        )
        try:
            await app.send_message(CHANNEL_ID, message_text)
            await asyncio.sleep(3) # فاصله ۳ ثانیه
        except: break

async def main():
    async with app:
        await scan_and_send()

if __name__ == "__main__":
    app.run(main())
