import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Logs enable karein taake Railway dashboard mein sab dikhe
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Bot Active! Mujhe group/channel mein Admin banayein.")

async def remove_forward(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.effective_message
    
    # Check karein ke message forwarded hai ya nahi
    if msg.forward_date or msg.forward_from or msg.forward_from_chat:
        try:
            # Pehle message copy karein (bina tag ke)
            await context.bot.copy_message(
                chat_id=msg.chat_id,
                from_chat_id=msg.chat_id,
                message_id=msg.message_id
            )
            # Purana forwarded message delete kar dein
            await msg.delete()
            logging.info(f"Forward tag removed in {msg.chat_id}")
        except Exception as e:
            logging.error(f"Error: {e}")

if __name__ == "__main__":
    if not BOT_TOKEN:
        print("❌ BOT_TOKEN missing!")
    else:
        app = ApplicationBuilder().token(BOT_TOKEN).build()
        
        app.add_handler(CommandHandler("start", start))
        
        # Ye filter sirf forwarded messages ko pakre ga
        app.add_handler(MessageHandler(filters.FORWARDED & ~filters.COMMAND, remove_forward))

        print("🚀 Bot is running...")
        app.run_polling()
