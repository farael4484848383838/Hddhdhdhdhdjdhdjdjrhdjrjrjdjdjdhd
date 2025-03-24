import logging
import requests
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message

# === Конфигурация ===
TELEGRAM_BOT_TOKEN = "7900325694:AAGv2au462kNIf6IxsUOHxHcCiebVgr7adI"  # Замени на свой Telegram API-токен
API_TOKEN = "7645306994:lC7Eop9N"  # Замени на токен LeakOsint API
API_URL = "https://leakosintapi.com/"  # URL API

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)

# === Функция для запроса к API ===
def search_osint(query, limit=100, lang="en"):
    data = {
        "token": API_TOKEN,
        "request": query,
        "limit": limit,
        "lang": lang
    }
    try:
        response = requests.post(API_URL, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

# === Обработчик команды /start ===
@dp.message_handler(commands=['start'])
async def send_welcome(message: Message):
    await message.reply("Привет! Отправь мне запрос (например, email, телефон, имя), и я попробую найти информацию.")

# === Обработчик сообщений (поисковые запросы) ===
@dp.message_handler()
async def handle_query(message: Message):
    query = message.text.strip()
    if not query:
        await message.reply("Введите корректный запрос.")
        return

    await message.reply("🔍 Ищу информацию...")

    result = search_osint(query)
    
    if "error" in result:
        await message.reply(f"⚠ Ошибка: {result['error']}")
    else:
        response_text = f"🔎 Результаты для запроса `{query}`:\n\n{result}"
        await message.reply(response_text, parse_mode="Markdown")

# === Запуск бота ===
async def main():
    await dp.start_polling()

if __name__ == "__main__":
    asyncio.run(main())