import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.filters.command import Command
from config import API_TOKEN
from database import create_table
from handlers import cmd_start, cmd_quiz, cmd_stats, right_answer, wrong_answer

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Регистрация обработчиков
dp.message.register(cmd_start, Command("start"))
dp.message.register(cmd_quiz, F.text == "Начать игру")
dp.message.register(cmd_quiz, Command("quiz"))
dp.message.register(cmd_stats, F.text == "Статистика")
dp.message.register(cmd_stats, Command("stats"))
dp.callback_query.register(right_answer, F.data == "right_answer")
dp.callback_query.register(wrong_answer, F.data == "wrong_answer")

async def main():
    # Создание таблицы БД
    await create_table()
    
    # Запуск бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())