import os
import time
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

TOKEN = "8865382059:AAFXBJwmxFtmnL66PWznsUe1p8cJfXQpSv8"

user_sticker_count = {}

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message
    if not message or not message.from_user:
        return
        
    user_id = message.from_user.id
    chat_id = message.chat_id
    current_time = time.time()

    try:
        member = await context.bot.get_chat_member(chat_id, user_id)
        if member.status in ['creator', 'administrator']:
            return
    except:
        pass

    if message.text and ("http" in message.text.lower() or "t.me" in message.text.lower()):
        try:
            await message.delete()
            await context.bot.restrict_chat_member(chat_id, user_id, permissions={"can_send_messages": False}, until_date=int(current_time + 18000))
            await context.bot.send_message(chat_id, f"@{message.from_user.username or message.from_user.first_name} လင့်ခ်ချလို့ ဖျက်ပြီး ၅ နာရီ Mute လိုက်ပါပြီ။")
        except:
            pass
        return

    if message.forward_date:
        try:
            await message.delete()
            await context.bot.restrict_chat_member(chat_id, user_id, permissions={"can_send_messages": False}, until_date=int(current_time + 600))
            await context.bot.send_message(chat_id, f"@{message.from_user.username or message.from_user.first_name} Forward လုပ်လို့ ၁၀ မိနစ် Mute လိုက်ပါပြီ။")
        except:
            pass
        return

    banned_words = ["လိုး", "စောက်", "လီး", "ဖူးကား", "အပြာ"]
    if message.text:
        for word in banned_words:
            if word in message.text:
                try:
                    await message.delete()
                    await context.bot.ban_chat_member(chat_id, user_id)
                    await context.bot.send_message(chat_id, f"@{message.from_user.username or message.from_user.first_name} ကို ၁၈+ စာသားကြောင့် အပြီး Ban လိုက်ပါပြီ။")
                except:
                    pass
                return

    if message.sticker:
        if user_id not in user_sticker_count:
            user_sticker_count[user_id] = []
        
        user_sticker_count[user_id] = [t for t in user_sticker_count[user_id] if current_time - t < 60]
        user_sticker_count[user_id].append(current_time)

        if len(user_sticker_count[user_id]) >= 5:
            try:
                await context.bot.restrict_chat_member(chat_id, user_id, permissions={"can_send_messages": False}, until_date=int(current_time + 1200))
                await context.bot.send_message(chat_id, f"@{message.from_user.username or message.from_user.first_name} Sticker ၅ ခုထက်ပိုပို့လို့ မိနစ် ၂၀ Mute လိုက်ပါပြီ။")
                user_sticker_count[user_id] = []
            except:
                pass
            return

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.ALL, handle_message))
    
    from flask import Flask
    import threading
    flask_app = Flask('')
    @flask_app.route('/')
    def home(): return "Bot Is Running"
    def run(): flask_app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
    threading.Thread(target=run).start()

    app.run_polling()

if __name__ == '__main__':
    main()
