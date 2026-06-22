import os
import time
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# သင့်ရဲ့ Token ကို တစ်ခါတည်း အသေထည့်ပေးထားပါတယ်
TOKEN = "8865382059:AAFXBJwmxFtmnL66PWznsUe1p8cJfXQpSv8"

user_sticker_count = {}

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message
    if not message or not message.from_user:
        return
        
    user_id = message.from_user.id
    chat_id = message.chat_id
    current_time = time.time()

    # Group Admin တွေဆိုရင် Bot က ဖမ်းမှာမဟုတ်ပါဘူး (ကျော်သွားမယ်)
    try:
        member = await context.bot.get_chat_member(chat_id, user_id)
        if member.status in ['creator', 'administrator']:
            return
    except:
        pass

    # ၁။ Link လာချရင် ဖျက်ပြီး ၅ နာရီ Mute မယ်
    if message.text and ("http" in message.text.lower() or "t.me" in message.text.lower()):
        try:
            await message.delete()
            await context.bot.restrict_chat_member(chat_id, user_id, permissions={"can_send_messages": False}, until_date=int(current_time + 18000))
            await context.bot.send_message(chat_id, f"@{message.from_user.username or message.from_user.first_name} လင့်ခ်ချလို့ ဖျက်ပြီး ၅ နာရီ Mute လိုက်ပါပြီ။")
        except:
            pass
        return

    # ၂။ Forward လာချရင် ၁၀ မိနစ် Mute မယ်
    if message.forward_date:
        try:
            await message.delete()
            await context.bot.restrict_chat_member(chat_id, user_id, permissions={"can_send_messages": False}, until_date=int(current_time + 600))
            await context.bot.send_message(chat_id, f"@{message.from_user.username or message.from_user.first_name} Forward လုပ်လို့ ၁၀ မိနစ် Mute လိုက်ပါပြီ။")
        except:
            pass
        return

    # ၃။ 18+ စာသား Auto Ban
    banned_words =
