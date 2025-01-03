<h2>Telegram bot for monitoring toxic comments.</h2>

<h3>Quick start:</h3>

```
echo "BOT_TOKEN=52:ZZZ_ASD" > .env
docker-compose up -d    
```


Dataset - https://www.kaggle.com/datasets/blackmoon/russian-language-toxic-comments

Сhannel for testing the bot - https://t.me/antitoxasd


<br>
<h3>Developed as part of a info subject task:</h3>
    <b>Робокоп</b><br>
    Напишите телеграм бота, который реагирует на каждый новый комментарий в телеграм канале и банит пользователя, если комментарий токсичный.

    5 баллов - конфигурация канала и бота;
    5 баллов - упаковка модели в восстановимый бинарный формат (для использования без переобучения при запуске бота);
    5 баллов - автобан.