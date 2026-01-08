import asyncio, os, jdatetime, re
from pyrogram import Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime, timedelta, timezone

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING")
CHANNEL_ID = "favproxy"

# نقشه پرچم‌ها برای لوکیشن‌ها
FLAG_MAP = {
    'DE': '🇩🇪 Germany', 'FI': '🇫🇮 Finland', 'US': '🇺🇸 USA', 
    'TR': '🇹🇷 Turkey', 'NL': '🇳🇱 Netherlands', 'FR': '🇫🇷 France',
    'GB': '🇬🇧 UK', 'SG': '🇸🇬 Singapore', 'JP': '🇯🇵 Japan'
}

def detect_locations(configs):
    stats = {}
    for config in configs:
        found = False
        for code, name in FLAG_MAP.items():
            if code in config.upper() or name.split()[1].upper() in config.upper():
                stats[name] = stats.get(name, 0) + 1
                found = True
                break
        if not found:
            stats['🌐 Others'] = stats.get('🌐 Others', 0) + 1
    
    location_report = ""
    for loc, count in sorted(stats.items(), key=lambda x: x[1], reverse=True):
        location_report += f"  └ {loc}: `{count}`\n"
    return location_report

async def collect_and_upload():
    if not os.path.exists("validated_configs.txt"): return
    with open("validated_configs.txt", "r", encoding="utf-8") as f:
        unique_configs = f.read().splitlines()
    if not unique_configs: return

    app = Client("aggregator", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)
    async with app:
        # تنظیم زمان ایران
        ir_tz = timezone(timedelta(hours=3, minutes=30))
        now = datetime.now(timezone.utc).astimezone(ir_tz)
        shamsi = jdatetime.datetime.fromgregorian(datetime=now)
        date_str = shamsi.strftime("%Y/%m/%d")
        time_str = shamsi.strftime("%H:%M")
        
        loc_stats = detect_locations(unique_configs)
        sub_link = "https://mehrdad2200.github.io/Hunter-Bot-GitHub/"

        # متن کپشن با استایل جدید
        caption_text = (
            f"💠 **HUNTER PREMIUM CONFIGS**\n"
            f"──────────────────────\n"
            f"📅 **DATE:** `{date_str}`  |  ⏰ **TIME:** `{time_str}`\n"
            f"🚀 **TOTAL:** `{len(unique_configs)}` Verified Configs\n"
            f"🌐 **NETWORK STATUS:** `Global Online` ✅\n\n"
            f"🌍 **LOCATION STATS:**\n"
            f"{loc_stats}"
            f"──────────────────────\n"
            f"🆔 @{CHANNEL_ID}"
        )

        # دکمه‌های شیشه‌ای زیر پست
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("📋 Copy Sub-Link", url=f"https://t.me/share/url?url={sub_link}")],
            [InlineKeyboardButton("📢 Channel", url=f"https://t.me/{CHANNEL_ID}")]
        ])

        file_name = f"{date_str.replace('/', '-')}_{time_str.replace(':', '-')}.txt"
        with open(file_name, "w", encoding="utf-8") as f:
            f.write("\n\n".join(unique_configs))
        
        # ارسال فایل به همراه کپشن و دکمه‌ها
        await app.send_document(
            CHANNEL_ID, 
            document=file_name, 
            caption=caption_text,
            reply_markup=buttons
        )
        
        # پاکسازی فایل موقت
        if os.path.exists(file_name):
            os.remove(file_name)

if __name__ == "__main__":
    asyncio.run(collect_and_upload())
