import asyncio
import random
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import CommandStart
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from aiogram.client.default import DefaultBotProperties
from apscheduler.schedulers.asyncio import AsyncIOScheduler

API_TOKEN = '8335218158:AAGQsXxGCc0qDOolAW1SZesJBmi0l5gE2Ng'

bot = Bot(
    token=API_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher(storage=MemoryStorage())
dp.message.middleware(CallbackAnswerMiddleware())

scheduler = AsyncIOScheduler()
chat_ids = set()

# Сообщения
auto_messages = [
    "Ты невероятен 🤍",
    "Жизнь становится лучше с тобой 🌸",
    "Пусть твой день будет лёгким как облачко ☁️",
    "Ты приносишь свет в этот мир ☀️"
]

button_messages = [
    "Ты лучший, даже если не веришь в это 💫",
    "Никогда не сомневайся в себе — ты сияешь! ✨",
    "Ты достоин любви, радости и всего хорошего 🌷",
    "Хорошего тебе дня, герой 🤍"
]

# Кнопка
keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Получить тёплое послание 💌", callback_data="motivate")]
    ]
)

@dp.message(CommandStart())
async def start_handler(message: types.Message):
    chat_ids.add(message.chat.id)
    await message.answer("Привет! Я тут, чтобы напоминать тебе, какой ты классный 🫶", reply_markup=keyboard)

@dp.callback_query()
async def button_handler(callback: types.CallbackQuery):
    msg = random.choice(button_messages)
    await callback.message.answer(msg)
    await callback.answer()

async def scheduled_message():
    for chat_id in chat_ids:
        try:
            msg = random.choice(auto_messages)
            await bot.send_message(chat_id, msg)
        except Exception as e:
            print(f"Ошибка при отправке: {e}")

async def main():
    scheduler.add_job(scheduled_message, "interval", hours=3)
    scheduler.start()
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
