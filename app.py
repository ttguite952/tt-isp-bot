import os
import asyncio
from flask import Flask, jsonify
from threading import Thread
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN")
app = Flask(__name__)
active_queue = []

@app.route('/')
def home():
    return "TT ISP Bot Running!"

@app.route('/get-commands')
def get_commands():
    global active_queue
    data = list(active_queue)
    active_queue.clear()
    return jsonify({"commands": data})

async def start(update, context):
    await update.message.reply_text(
"TT ISP Bot nung e!\nHman dan: /active ralte")

async def active_cmd(update, context):
    if not context.args:
        await update.message.reply_text(
"Hman dan: /active ralte")
        return
    username = context.args[0].lower()
    active_queue.append({"user": username,
"action": "active"})
    await update.message.reply_text(f"✅ {username}\nQueue ah dah fel. 1 min ah a nung ang.")

def run_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    application = Application.builder().token(
BOT_TOKEN).build()
    application.add_handler(CommandHandler(
"start", start))
    application.add_handler(CommandHandler(
"active", active_cmd))
    application.run_polling()

if BOT_TOKEN:
    t = Thread(target=run_bot, daemon=True)
    t.start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ
.get("PORT", 10000)))