import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == "private":
        await update.message.reply_text(
            "🤖 Forward Tag Remover Bot\n\n"
            "➕ Mujhe channel ya group ka ADMIN banao\n"
            "🧹 Main forwarded posts ka tag hata deta hoon\n\n"
            "Developer: BhaiKiMasti"
        )

async def remove_forward(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.channel_post or update.message
    if not msg:
        return

    # ✅ Forward check (channel compatible)
    if msg.forward_origin:
        try:
            await context.bot.copy_message(
                chat_id=msg.chat_id,
                from_chat_id=msg.chat_id,
                message_id=msg.message_id
            )
            await msg.delete()
            logging.info("Forward removed successfully")

        except Exception as e:
            logging.error(f"Delete/Copy error: {e}")

if __name__ == "__main__":
    if not BOT_TOKEN:
        print("❌ BOT_TOKEN missing!")
        exit()

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    # 🔥 VERY IMPORTANT
    app.add_handler(MessageHandler(filters.ALL, remove_forward))

    print("🚀 Bot running...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)
    
