import os
from flask import Flask, request, jsonify
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import asyncio

BOT_TOKEN = os.environ.get("BOT_TOKEN")
app = Flask(__name__)
active_queue = []

# Telegram Application
application = Application.builder().token(BOT_TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("TT ISP Bot nung e!\nHman dan: /active ralte")

async def active_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Hman dan: /active ralte")
        return
    username = context.args[0].lower()
    active_queue.append({"user": username, "action": "active"})
    await update.message.reply_text(f"✅ {username}\nQueue ah dah fel. 1 min ah a nung ang.")

application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("active", active_cmd))

@app.route('/')
def home():
    return "TT ISP Bot Running!"

@app.route('/get-commands')
def get_commands():
    global active_queue
    data = list(active_queue)
    active_queue.clear()
    return jsonify({"commands": data})

@app.route('/webhook', methods=['POST'])
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if data:
        async def process():
            update = Update.de_json(data, application.bot)
            await application.initialize()
            await application.process_update(update)
        asyncio.run(process())
    return "ok" def webhook():
    data = request.get_json()
    if data:
        update = Update.de_json(data, application.bot)
        await application.initialize()
        await application.process_update(update)
    return "ok"

@app.route('/set-webhook')
def set_webhook_route():
    async def set_it():
        url = f"https://{request.host}/webhook"
        await application.bot.set_webhook(url)
        return f"Webhook set to {url}"
    return asyncio.run(set_it())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))