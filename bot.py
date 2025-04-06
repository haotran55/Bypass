import re
import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import os

TOKEN = os.environ.get("BOT_TOKEN")  # Lưu TOKEN trong Render Environment

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Gửi link yeumoney.net để mình thử xử lý giúp bạn.")

def bypass_yeumoney_requests(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    try:
        session = requests.Session()
        response = session.get(url, headers=headers, timeout=10)

        if response.status_code != 200:
            return "Không thể truy cập link."

        soup = BeautifulSoup(response.text, "html.parser")

        meta = soup.find("meta", attrs={"http-equiv": "refresh"})
        if meta:
            content = meta.get("content")
            match = re.search(r'url=(.*)', content, re.IGNORECASE)
            if match:
                redirect_url = match.group(1)
                return f"🔁 Link chuyển hướng: {redirect_url}"

        for a in soup.find_all("a", href=True):
            if "go.php?" in a["href"] or "redirect" in a["href"]:
                return f"🔗 Link tiếp theo: {a['href']}"

        return "Không tìm thấy link cuối cùng. Có thể cần JavaScript."

    except Exception as e:
        return f"Lỗi: {e}"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    match = re.search(r"https?://yeumoney\.net/\S+", text)
    if match:
        url = match.group(0)
        await update.message.reply_text("⏳ Đang xử lý link...")
        final = bypass_yeumoney_requests(url)
        await update.message.reply_text(final)
    else:
        await update.message.reply_text("Vui lòng gửi link hợp lệ từ yeumoney.net.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    print("Bot đang chạy...")
    app.run_polling()
