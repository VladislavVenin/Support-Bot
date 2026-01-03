# VK/Telegram support bot
Боты для ответов на часто задаваемые вопросы для VK и Telegram

## Установка
### Python
Проект был собран на python 3.10, для корректной работы запускайте все скрипты именно на этой версии

Установите зависимости:
```
pip install -r requirements.txt
```
### DialogFlow & GCloud
Боты работают с api DialogFlow

- [Создайте проект в DialogFlow](https://cloud.google.com/dialogflow/docs/quick/setup)
- [Создайте агента](https://cloud.google.com/dialogflow/docs/quick/build-agent)
- Натренируйте агента через скрипт `learning.py` или вручную, через вкладку `Intents`
- [Создайте токен](https://docs.cloud.google.com/docs/authentication/api-keys)

### Переменные окружения
Для работы скриптов требуется создать `.env` файл со следующими переменными окружения:

- `TG_TOKEN` - Токен вашего Telegram бота, его можно получить у  [BotFather](https://t.me/BotFather)
- `VK_TOKEN` - Токен вашей группы VK, содать его можно в меню `упраления` вашей группы (`Дополнительно\Работа с API`)
- `PROJECT_ID` - ID вашего Google Cloud проекта, узнать его можно в настройках проекта DialogFlow
- `GOOGLE_APPLICATION_CREDENTIALS` - Путь к api ключам GCloud

## Запуск

### learning.py
Скрипт для обучения агента по тренировочным фразам. Пример структуры файла с фразами есть в `questions.json`

Для скрипта можно указать альтернативный путь до `.json` файла с фразами с помощью ключа `-p`/`--path`. Стандартный путь: `./questions.json`
```
python learning.py -p some/folders/my_file.json
```

### telegram_bot.py
Скрипт запускающий вашего бота в Telegram
```
python telegram_bot.py
```

### vk_bot.py
Скрипт запускающий бота в вашей группе VK
```
python vk_bot.py
```