import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Logging taake Railway logs mein clear nazar aaye kya ho raha hai
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.effective_message
    await msg.reply_text("🚀 Bot Active! Channels aur Groups mein admin banayein.")

async def remove_forward(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # 'effective_message' use karne se update.message aur update.channel_post dono handle ho jate hain
    msg = update.effective_message
    
    if not msg:
        return

    # Check if the message is forwarded
    if msg.forward_date or msg.forward_from_chat or msg.forward_from:
        try:
            # Copy bina tag ke
            await context.bot.copy_message(
                chat_id=msg.chat_id,
                from_chat_id=msg.chat_id,
                message_id=msg.message_id
            )
            # Purana delete
            await msg.delete()
        except Exception as e:
            logging.error(f"Error logic: {e}")

if __name__ == "__main__":
    if not BOT_TOKEN:
        print("❌ Token missing in Railway Variables!")
    else:
        # 'allowed_updates' har tarah ki activity pakadne ke liye zaroori hai
        app = ApplicationBuilder().token(BOT_TOKEN).build()
        
        app.add_handler(CommandHandler("start", start))
        
        # filters.FORWARDED saare forwarded messages ko filter karega
        app.add_handler(MessageHandler(filters.FORWARDED & ~filters.COMMAND, remove_forward))

        print("🤖 Bot is starting... Noob mode off!")
        app.run_polling(allowed_updates=Update.ALL_TYPES)
