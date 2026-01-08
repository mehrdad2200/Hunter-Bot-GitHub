import asyncio, os, re, socket
from pyrogram import Client

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING")
CHANNEL_ID = "favproxy"

async def check_port(host, port, timeout=2.0):
    """بررسی باز بودن پورت سرور (TCP Ping)"""
    try:
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(host, port), timeout=timeout
        )
        writer.close()
        await writer.wait_closed()
        return True
    except:
        return False

def extract_host_port(config):
    """استخراج هاست و پورت از انواع کانفیگ"""
    try:
        # استخراج بخش بعد از @ و قبل از ? یا :
        match = re.search(r'@([^:/]+):(\d+)', config)
        if match:
            return match.group(1), int(match.group(2))
    except:
        pass
    return None, None

async def main():
    app = Client("checker_task", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)
    async with app:
        configs = []
        async for message in app.get_chat_history(CHANNEL_ID, limit=150):
            if message.text:
                links = re.findall(r'(?:vless|vmess|trojan|ss)://[^\s"\'<>]+', message.text)
                configs.extend(links)
        
        unique_configs = list(set(configs))
        valid_configs = []
        
        print(f"Checking {len(unique_configs)} configs for stability...")
        
        for link in unique_configs:
            host, port = extract_host_port(link)
            if host and port:
                # تست پورت (اگر باز بود یعنی سرور زنده است)
                is_alive = await check_port(host, port)
                if is_alive:
                    valid_configs.append(link)
            elif len(link) > 30: # برای لینک‌هایی که فرمت پیچیده دارند
                valid_configs.append(link)

        with open("validated_configs.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(valid_configs))
            
        with open("hourly_stats.log", "a") as f:
            f.write(f"{len(valid_configs)}\n")
        
        print(f"Finished. {len(valid_configs)} stable configs saved.")

if __name__ == "__main__":
    asyncio.run(main())
