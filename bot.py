import telebot
from model import predict_toxic
from dotenv import load_dotenv
import os
import time

load_dotenv()
bot = telebot.TeleBot(os.getenv("BOT_TOKEN"))

channel_id = int(os.getenv("CHANNEL_ID"))
group_id = int(os.getenv("GROUP_ID"))
max_tox_percent = float(os.getenv("MAX_TOX_PERCENT"))

@bot.message_handler(func=lambda message: message.chat.id == group_id)
def handle_comments(message):
    try:
        if message.reply_to_message and message.reply_to_message.forward_from_chat:
            if message.reply_to_message.forward_from_chat.id == channel_id:
                toxicity = predict_toxic(message.text)
                
                if toxicity >= max_tox_percent:
                    bot.delete_message(message.chat.id, message.message_id)
                    
                    name = f"@{message.from_user.username}" if message.from_user.username else message.from_user.first_name

                    until_date = int(time.time()) + 86400
                    bot.restrict_chat_member(
                        message.chat.id,
                        message.from_user.id,
                        until_date=until_date,
                        permissions=telebot.types.ChatPermissions(
                            can_send_messages=False,
                            can_send_media_messages=False,
                            can_send_other_messages=False
                        )
                    )

                    warning = f"Пользователь {name} отправил токсичный комментарий (токсичность: {toxicity:.1%}) и заблокирован до {time.strftime('%d.%m.%Y %H:%M', time.localtime(until_date))}"

                    bot.reply_to(message.reply_to_message, warning)
                    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("Bot started")
    bot.infinity_polling()
