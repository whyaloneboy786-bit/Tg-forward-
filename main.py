import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Logs enable karein taake Railway dashboard mein error dikhe
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == "private":
        await update.message.reply_text(
            "🤖 Forward Tag Remover Bot\n\n"

        "👨‍💻 Developer: Dead person"

        "📢 Support Channel: @moviesupdatehub\n\n"

        "Add me as admin in groups/channels.\n"
async def remove_forward(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.effective_message
    if not msg or not msg.forward_date: # Sirf forwarded messages ko touch karega
        return

    try:
        await context.bot.copy_message(
            chat_id=msg.chat_id,
            from_chat_id=msg.chat_id,
            message_id=msg.message_id
        )
        await msg.delete()
    except Exception as e:
        logging.error(f"Error: {e}")

if __name__ == "__main__":
    if not BOT_TOKEN:
        print("CRITICAL ERROR: BOT_TOKEN is missing in Railway Variables!")
    else:
        app = ApplicationBuilder().token(BOT_TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(MessageHandler(filters.ALL & (~filters.COMMAND), remove_forward))

        print("🤖 Bot is starting...")
        app.run_polling()
