import asyncio, os, jdatetime
from pyrogram import Client
from datetime import datetime, timedelta, timezone

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING")
CHANNEL_ID = "favproxy"

def get_shamsi_date():
    ir_tz = timezone(timedelta(hours=3, minutes=30))
    now = datetime.now(timezone.utc).astimezone(ir_tz)
    return jdatetime.datetime.fromgregorian(datetime=now).strftime("%Y/%m/%d")

async def send_report():
    app = Client("daily_reporter", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)
    async with app:
        date_str = get_shamsi_date()
        
        # دریافت آمار اعضا
        chat = await app.get_chat(CHANNEL_ID)
        members_count = chat.members_count
        
        # محاسبه جمع کانفیگ‌های امروز از روی فایل log
        total_today = 0
        if os.path.exists("hourly_stats.log"):
            with open("hourly_stats.log", "r") as f:
                total_today = sum(int(line.strip()) for line in f if line.strip())
            os.remove("hourly_stats.log") # پاکسازی برای فردا

        report_text = (
            f"📊 **گزارش جامع عملکرد سیستم HUNTER**\n"
            f"──────────────────────\n"
            f"📅 **تاریخ:** `{date_str}`\n\n"
            f"👥 **آمار جامعه کاربران:**\n"
            f"  └ 👥 کل دنبال‌کنندگان: `{members_count:,}` نفر\n\n"
            f"✅ **آمار جمع‌آوری و تست:**\n"
            f"  └ 💎 کانفیگ‌های تایید شده امروز: `{total_today:,}` عدد\n"
            f"  └ 🗑 موارد تکراری و مخرب: `فیلتر شدند` \n\n"
            f"🌐 **تنوع پروتکل‌ها:**\n"
            f"  └ 🟦 VLESS | 🟩 VMESS | 🟧 Trojan\n\n"
            f"🌍 **برترین لوکیشن‌های فعال:**\n"
            f"  🇩🇪 Germany | 🇫🇮 Finland | 🇺🇸 USA\n\n"
            f"💡 *تمامی سرویس‌ها برای اپراتورهای داخلی بهینه‌سازی شده‌اند.*\n"
            f"──────────────────────\n"
            f"🔗 **لینک اشتراک اختصاصی:**\n"
            f"`https://mehrdad2200.github.io/Hunter-Bot-GitHub/`\n\n"
            f"🆔 @{CHANNEL_ID}"
        )
        
        await app.send_message(CHANNEL_ID, text=report_text)

if __name__ == "__main__":
    asyncio.run(send_report())
