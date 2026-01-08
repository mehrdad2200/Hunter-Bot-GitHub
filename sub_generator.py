import os
import re

def generate_sub():
    # نام برند و کانال شما
    MY_BRAND = "https://t.me/favproxy"
    
    if os.path.exists("validated_configs.txt"):
        with open("validated_configs.txt", "r", encoding="utf-8") as f:
            configs = f.read().splitlines()

        if configs:
            cleaned_configs = []
            
            # ۱. هدر مخصوص برای شناسایی نام ساب‌لینک در هیدفای و کلاینت‌های مدرن
            profile_header = f"profile-title: {MY_BRAND}"
            cleaned_configs.append(profile_header)
            
            # ۲. اضافه کردن یک پیام نمایشی در ابتدای لیست سرورها
            # این خط باعث می‌شود در لیست سرورها هم آدرس کانالت همیشه بالا باشد
            info_tag = f"vless://ea680e9a-761a-4131-893f-c104446f790c@1.1.1.1:443?encryption=none&security=tls&type=tcp#{MY_BRAND} 💎"
            cleaned_configs.append(info_tag)

            for config in configs:
                if not config.strip():
                    continue
                
                # ۳. عملیات جراحی: حذف اسم‌های قبلی و جایگذاری اسم شما
                # این بخش هر چیزی بعد از علامت # را پاک می‌کند و اسم شما را می‌گذارد
                if "#" in config:
                    base_config = config.split("#")[0]
                    # تمیز کردن اسم سرور و اضافه کردن برند خودت
                    new_config = f"{base_config}#{MY_BRAND} | Hunter"
                    cleaned_configs.append(new_config)
                else:
                    # اگر کانفیگ اسم نداشت، اسم شما را اضافه می‌کند
                    cleaned_configs.append(f"{config}#{MY_BRAND}")

            # ذخیره نهایی در فایل index.html
            with open("index.html", "w", encoding="utf-8") as f:
                f.write("\n".join(cleaned_configs))
            
            print(f"Sub-link updated & Brand cleaned for: {MY_BRAND}")
    else:
        print("validated_configs.txt not found!")

if __name__ == "__main__":
    generate_sub()
