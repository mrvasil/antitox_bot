import telebot
from model import predict_toxic
from config_manager import add_channel_group_pair, get_channel_group_pairs
from dotenv import load_dotenv
import os
import time

load_dotenv()
bot = telebot.TeleBot(os.getenv("BOT_TOKEN"))
max_tox_percent = 0.60

@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.type == 'private':
        bot.reply_to(message, 
            "Привет! Я бот для автоматического удаления токсичных комментариев.\n\n"
            "Для настройки, отправьте мне в одном сообщении ID канала и группы. А также добавьте бота в группу с правами администратора.\n\n"
            "Пример:\n"
            "channel:-1005252525252\ngroup:-1005252525252",
            parse_mode='Markdown'
        )

@bot.message_handler(func=lambda message: message.chat.type == 'private')
def handle_config(message):
    text = message.text.strip()
    lines = text.split('\n')
    
    if len(lines) != 2:
        bot.reply_to(message, "Пожалуйста, отправьте ID канала и группы в одном сообщении, каждый с новой строки")
        return
    
    channel_line = lines[0].strip()
    group_line = lines[1].strip()
    
    if not (channel_line.startswith('channel:') and group_line.startswith('group:')):
        bot.reply_to(message, "Неверный формат. Используйте:\nchannel:ID_КАНАЛА\ngroup:ID_ГРУППЫ")
        return
    
    try:
        channel_id = int(channel_line.split(':')[1])
        group_id = int(group_line.split(':')[1])

        add_channel_group_pair(channel_id, group_id)
        bot.reply_to(message, 
            f"Настройка завершена!\n"
            f"Канал ID: {channel_id}\n"
            f"Группа ID: {group_id}\n\n"
            f"Вы можете добавить еще одну пару, отправив новую конфигурацию"
        )
    except:
        bot.reply_to(message, "Неверный формат. Используйте:\nchannel:ID_КАНАЛА\ngroup:ID_ГРУППЫ")

@bot.message_handler(func=lambda message: message.chat.type == 'group' or message.chat.type == 'supergroup')
def handle_comments(message):
    try:
        if message.reply_to_message and message.reply_to_message.forward_from_chat:
            channel_id = str(message.reply_to_message.forward_from_chat.id)
            config = get_channel_group_pairs()
            
            if channel_id in config and message.chat.id == config[channel_id]:
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
