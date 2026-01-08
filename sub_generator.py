import os

def generate_sub():
    MY_BRAND = "https://t.me/favproxy"
    SUB_LINK = "https://mehrdad2200.github.io/Hunter-Bot-GitHub/"
    
    if os.path.exists("validated_configs.txt"):
        with open("validated_configs.txt", "r", encoding="utf-8") as f:
            configs = f.read().splitlines()

        if configs:
            total_count = len(configs)
            # تمیز کردن و آماده‌سازی کانفیگ‌ها برای خروجی خام
            raw_configs_list = [f"{c.split('#')[0]}#{MY_BRAND} | Hunter" if "#" in c else f"{c}#{MY_BRAND}" for c in configs]
            raw_configs_string = "\\n".join(raw_configs_list)

            # ساخت فایل داشبورد با منطق تشخیص معکوس (بسیار دقیق‌تر)
            dashboard_html = f"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HUNTER Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <script>
        // --- منطق فوق هوشمند تشخیص ---
        const ua = navigator.userAgent;
        // اکثر اپلیکیشن‌های وی‌پی‌ان کلمه Mozilla را ندارند یا ساختار متفاوتی دارند
        // اگر مرورگر معمولی نباشد، محتوا را با کانفیگ عوض می‌کنیم
        if (!ua.includes("Mozilla")) {{
            document.open();
            document.write(`{raw_configs_string}`);
            document.close();
        }}
    </script>
    <style>
        body {{ background-color: #0f172a; color: #f8fafc; font-family: Tahoma, sans-serif; }}
        .glass {{ background: rgba(30, 41, 59, 0.7); backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.1); }}
    </style>
</head>
<body class="p-4 md:p-8">
    <div class="max-w-4xl mx-auto">
        <header class="flex justify-between items-center mb-8 glass p-6 rounded-2xl shadow-2xl border-r-4 border-blue-500">
            <div>
                <h1 class="text-2xl font-bold text-blue-400 text-left">HUNTER <span class="text-white">DASHBOARD</span></h1>
                <p class="text-sm text-slate-400">وضعیت لحظه‌ای سرورهای اختصاصی</p>
            </div>
            <div class="text-green-400 text-sm flex items-center gap-2">
                <span class="relative flex h-3 w-3">
                  <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
                  <span class="relative inline-flex rounded-full h-3 w-3 bg-green-500"></span>
                </span>
                شبکه پایدار
            </div>
        </header>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
            <div class="glass p-8 rounded-2xl text-center">
                <div class="text-5xl font-black text-blue-500 mb-2">{total_count}</div>
                <div class="text-slate-400 font-bold text-lg text-sm">سرور فعال</div>
            </div>
            <div class="glass p-8 rounded-2xl text-center">
                <div class="text-5xl font-black text-green-500 mb-2">100%</div>
                <div class="text-slate-400 font-bold text-lg text-sm">ضمانت اتصال</div>
            </div>
        </div>

        <div class="glass p-8 rounded-3xl text-center border-2 border-dashed border-blue-500/30">
            <h2 class="text-xl font-bold mb-4">لینک اشتراک برای کپی در اپلیکیشن</h2>
            <div class="bg-slate-900 p-4 rounded-xl text-blue-400 mb-6 break-all text-left font-mono text-xs border border-blue-900/50">
                {SUB_LINK}
            </div>
            <button onclick="navigator.clipboard.writeText('{SUB_LINK}'); alert('لینک کپی شد!')" 
                    class="bg-blue-600 w-full py-4 rounded-xl font-bold hover:bg-blue-500 transition-all shadow-lg shadow-blue-500/20 active:scale-95">
                <i class="fas fa-copy ml-2"></i> کپی لینک هوشمند
            </button>
        </div>

        <footer class="mt-8 text-center text-slate-500 text-xs">
            HUNTER PROJECT &copy; 2026 | @favproxy
        </footer>
    </div>
</body>
</html>"""

            with open("index.html", "w", encoding="utf-8") as f:
                f.write(dashboard_html)
            
            print(f"Professional Dashboard generated with {total_count} configs.")
    else:
        print("Error: validated_configs.txt not found!")

if __name__ == "__main__":
    generate_sub()
