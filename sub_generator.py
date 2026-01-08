import os

def generate_sub():
    # خواندن کانفیگ‌های تایید شده
    if os.path.exists("validated_configs.txt"):
        with open("validated_configs.txt", "r", encoding="utf-8") as f:
            content = f.read()

        # ساخت فایل index.html برای نمایش در لینک مستقیم
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(content)
        print("index.html created successfully.")
    else:
        print("No validated_configs.txt found to generate sub.")

if __name__ == "__main__":
    generate_sub()
