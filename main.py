import logging
import json
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from config import BOT_TOKEN, OPENROUTER_API_KEY

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN, default=types.DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
dp = Dispatcher()

WELCOME_MESSAGE = (
    "👋 Привет! Я *НейроБахта* — твой AI помощник на базе `deepseek-r1`.

"
    "🧠 Просто задай мне вопрос или напиши что-нибудь.
"
    "🔁 Чтобы *сбросить контекст*, используй команду /reset.

"
    "*Правила общения:*
"
    "1. Нельзя отправлять вредоносные, запрещённые или экстремистские запросы
"
    "2. Не нарушай правила Telegram и закона
"
    "3. Я могу ошибаться — проверяй важную информацию
"
)

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(WELCOME_MESSAGE)

@dp.message()
async def handle_message(message: Message):
    user_message = message.text

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://your-site.com",
        "X-Title": "NeiroBaxtaBot",
    }

    data = {
        "model": "deepseek/deepseek-r1-0528:free",
        "messages": [{"role": "user", "content": user_message}],
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, data=json.dumps(data))
        result = response.json()
        reply = result["choices"][0]["message"]["content"]
        await message.answer(reply)
    except Exception as e:
        logging.error("Ошибка при обращении к API:", exc_info=e)
        await message.answer("Произошла ошибка при обращении к нейросети. Попробуйте позже.")

if __name__ == "__main__":
    dp.run_polling(bot)