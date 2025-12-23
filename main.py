from keep_alive import keep_alive

keep_alive()  # Starts the Flask server

import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

BOT_TOKEN = os.getenv("BOT_TOKEN")  # Ensure your bot token is set in environment variables

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type != "private":
        return

    await update.message.reply_text(
        "🤖 Forward Tag Remover Bot\n\n"
        "👨‍💻 Developer: BhaiKiMasti\n"
        "📢 Support Channel: @moviesupdatehub\n\n"
        "Add me as admin in groups/channels.\n"
        "I remove forward tags automatically."
    )

# Handler to remove forward tags
async def remove_forward(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.effective_message
    chat = update.effective_chat

    if chat.type not in ["group", "supergroup", "channel"]:
        return

    # Only process forwarded messages
    if msg.forward_from or msg.forward_from_chat:
        try:
            # Copy the message without forward tag
            await context.bot.copy_message(
                chat_id=chat.id,
                from_chat_id=chat.id,
                message_id=msg.message_id
            )
            # Delete only the forwarded message
            await msg.delete()
        except Exception as e:
            print("Error removing forward tag:", e)

# Initialize bot
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.ALL, remove_forward))

print("🤖 Bot running...")
app.run_polling()

