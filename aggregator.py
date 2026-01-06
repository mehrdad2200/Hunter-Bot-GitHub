import asyncio, os, jdatetime, re, random, requests
from pyrogram import Client
from datetime import datetime, timedelta, timezone
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

# GitHub Secrets
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING")
CHANNEL_ID = "favproxy"

# لینک بنرها
IMAGE_LIST = [
    "https://raw.githubusercontent.com/mehrdad2200/Hunter-Bot-GitHub/main/banner1.jpg",
    "https://raw.githubusercontent.com/mehrdad2200/Hunter-Bot-GitHub/main/banner2.jpg",
    "https://raw.githubusercontent.com/mehrdad2200/Hunter-Bot-GitHub/main/banner3.jpg",
    "https://raw.githubusercontent.com/mehrdad2200/Hunter-Bot-GitHub/main/banner4.jpg"
]

# لینک مستقیم یک فونت زیبا (Roboto) برای دانلود خودکار
FONT_URL = "https://github.com/google/fonts/raw/main/apache/roboto/Roboto-Bold.ttf"

app = Client("aggregator", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)

def get_iran_time():
    ir_tz = timezone(timedelta(hours=3, minutes=30))
    now = datetime.now(timezone.utc).astimezone(ir_tz)
    shamsi = jdatetime.datetime.fromgregorian(datetime=now)
    return shamsi.strftime("%Y/%m/%d"), shamsi.strftime("%H:%M")

async def create_image_with_text(img_url, date_str, time_str, count):
    # دانلود عکس بنر
    response = requests.get(img_url)
    img = Image.open(BytesIO(response.content)).convert("RGB")
    draw = ImageDraw.Draw(img)
    
    # دانلود فونت
    font_res = requests.get(FONT_URL)
    font = ImageFont.truetype(BytesIO(font_res.content), 45) # سایز فونت: 45
    
    # متن‌هایی که باید روی عکس نوشته شوند
    text_to_write = f"DATE: {date_str}\nTIME: {time_str}\nTOTAL: {count} CONFIGS"
    
    # تنظیم محل قرارگیری متن (مختصات X و Y)
    # این اعداد را بسته به طرح عکست می‌توانی جابجا کنی
    draw.multiline_text((60, 400), text_to_write, fill=(255, 255, 255), font=font, spacing=15)
    
    # تبدیل عکس به فرمت قابل ارسال برای تلگرام
    bio = BytesIO()
    bio.name = 'processed_banner.jpg'
    img.save(bio, 'JPEG')
    bio.seek(0)
    return bio

async def collect_and_upload():
    async with app:
        configs = []
        one_hour_ago = datetime.now(timezone.utc) - timedelta(hours=1)
        
        async for message in app.get_chat_history(CHANNEL_ID, limit=100):
            if message.date.replace(tzinfo=timezone.utc) < one_hour_ago:
                break
            if message.text:
                links = re.findall(r'(?:vless|vmess|trojan|ss)://[^\s"\'<>]+', message.text)
                configs.extend(links)

        if not configs: return

        date_str, time_str = get_iran_time()
        unique_configs = list(set(configs))
        
        # ساخت عکس با نوشته
        selected_url = random.choice(IMAGE_LIST)
        processed_photo = await create_image_with_text(selected_url, date_str, time_str, len(unique_configs))
        
        # ارسال عکس پردازش شده
        photo_msg = await app.send_photo(
            CHANNEL_ID, 
            photo=processed_photo, 
            caption=f"✅ Updated: {time_str} | @{CHANNEL_ID}"
        )

        # ساخت فایل متنی
        file_name = f"Pack_{time_str.replace(':', '-')}.txt"
        with open(file_name, "w", encoding="utf-8") as f:
            f.write("\n".join(unique_configs))

        await app.send_document(CHANNEL_ID, document=file_name, reply_to_message_id=photo_msg.id)
        os.remove(file_name)

if __name__ == "__main__":
    app.run(collect_and_upload())
