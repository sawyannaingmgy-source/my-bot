import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Logging စနစ် ထည့်သွင်းခြင်း (Render logs မှာ ကြည့်လို့ရအောင်)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# /start command ပေးရင် တုံ့ပြန်မယ့် code
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('မင်္ဂလာပါ! ကျွန်တော်ကတော့ သင့်ရဲ့ Bot ဖြစ်ပါတယ်။')

# /help command ပေးရင် တုံ့ပြန်မယ့် code
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('ဘာကူညီပေးရမလဲခင်ဗျာ။')

# စာပြန်ပို့ရင် လိုက်ပြောမယ့် code (Echo)
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"သင် ပို့လိုက်တဲ့စာကတော့: {update.message.text}")

def main() -> None:
    # သင့်ရဲ့ Bot Token
    TOKEN = "8865382059:AAFXBJwmxFtmnL66PWznsUe1p8cJfXQpSv8"
    
    # Application တည်ဆောက်ခြင်း (v20+ Syntax အသစ်)
    application = Application.builder().token(TOKEN).build()

    # Command များနှင့် Message Handler များ ထည့်သွင်းခြင်း
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Bot ကို စတင် run ခြင်း
    print("Bot စတင် အလုပ်လုပ်နေပါပြီ...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()

