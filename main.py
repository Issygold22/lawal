import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
    ContextTypes
)

# Configuration (Set via Render environment variables)
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHANNEL_USERNAME = "@YourChannel"  # Replace with your channel
GROUP_USERNAME = "@YourGroup"      # Replace with your group
TWITTER_LINK = "https://twitter.com/YourTwitter"

# States for conversation
START, SUBMIT_WALLET = range(2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Send instructions and require joins"""
    keyboard = [
        [InlineKeyboardButton("📢 Join Channel", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")],
        [InlineKeyboardButton("👥 Join Group", url=f"https://t.me/{GROUP_USERNAME[1:]}")],
        [InlineKeyboardButton("🐦 Follow Twitter", url=TWITTER_LINK)],
        [InlineKeyboardButton("✅ I've Joined", callback_data="joined")]
    ]
    
    await update.message.reply_text(
        "🎉 Welcome to Airdrop Bot!\n"
        "To qualify:\n"
        "1. Join our official channel\n"
        "2. Join our Telegram group\n"
        "3. Follow us on Twitter\n\n"
        "Click ✅ after completing all steps",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    
    return START

async def handle_join_confirmation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Request wallet address after join confirmation"""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("⬇️ Please send your SOLANA wallet address now:")
    return SUBMIT_WALLET

async def handle_wallet_submission(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Process wallet submission"""
    wallet = update.message.text
    # Normally you'd validate wallet format here
    await update.message.reply_text(
        "🎉 Congratulations! 10 SOL is on its way to your wallet!\n"
        f"Wallet: `{wallet}`\n\n"
        "⚠️ Note: This is a simulation. No actual SOL will be sent.",
        parse_mode="Markdown"
    )
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancel the conversation"""
    await update.message.reply_text("Process cancelled.")
    return ConversationHandler.END

def main() -> None:
    """Run bot"""
    # Create Application
    application = Application.builder().token(TOKEN).build()
    
    # Conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            START: [CallbackQueryHandler(handle_join_confirmation, pattern="^joined$")],
            SUBMIT_WALLET: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_wallet_submission)]
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )
    
    application.add_handler(conv_handler)
    
    # Start polling (for development)
    print("Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()
