import telebot
from model import predict_toxic
from dotenv import load_dotenv
import os

load_dotenv()
bot = telebot.TeleBot(os.getenv("BOT_TOKEN"))

channel_id = -1002428621580
group_id = -1002351877780
max_tox_percent = 0.60

@bot.message_handler(func=lambda message: message.chat.id == group_id)
def handle_comments(message):
    try:
        if message.reply_to_message and message.reply_to_message.forward_from_chat:
            if message.reply_to_message.forward_from_chat.id == channel_id:
                toxicity = predict_toxic(message.text)
                
                if toxicity >= max_tox_percent:
                    bot.delete_message(message.chat.id, message.message_id)
                    
                    name = f"@{message.from_user.username}" if message.from_user.username else message.from_user.first_name
                    warning = f"Пользователь {name} отправил токсичный комментарий (токсичность: {toxicity:.1%})"

                    bot.reply_to(message.reply_to_message, warning)
                    
    except Exception as e:
        
        print(f"Error: {e}")

if __name__ == "__main__":
    print("Bot started")
    bot.infinity_polling()
