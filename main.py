import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Railway logs mein error dekhne ke liye
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Command check for both message and channel_post
    msg = update.message or update.channel_post
    if msg:
        await msg.reply_text("🤖 Bot Active! I will remove forward tags from Groups and Channels.")

async def remove_forward(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Sabse zaroori line: Channel posts ko pakadne ke liye
    msg = update.channel_post or update.message
    
    if not msg:
        return

    # Check if forwarded
    if msg.forward_date or msg.forward_from_chat or msg.forward_from:
        try:
            # Copy message without tag
            await context.bot.copy_message(
                chat_id=msg.chat_id,
                from_chat_id=msg.chat_id,
                message_id=msg.message_id
            )
            # Delete original forwarded message
            await msg.delete()
        except Exception as e:
            logging.error(f"Error: {e}")

if __name__ == "__main__":
    if not BOT_TOKEN:
        print("❌ BOT_TOKEN missing in Railway Variables!")
    else:
        # allowed_updates=[update.ALL_TYPES] channels ke liye lazmi hai
        app = ApplicationBuilder().token(BOT_TOKEN).build()
        
        app.add_handler(CommandHandler("start", start))
        
        # filters.ALL use kar rahe hain taake koi bhi forward miss na ho
        app.add_handler(MessageHandler(filters.FORWARDED, remove_forward))

        print("🚀 Bot is starting...")
        # Railway ke liye updates enable karein
        app.run_polling(allowed_updates=Update.ALL_TYPES)
