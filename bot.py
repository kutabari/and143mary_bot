import asyncio
import random
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from apscheduler.schedulers.asyncio import AsyncIOScheduler

API_TOKEN = '8335218158:AAGQsXxGCc0qDOolAW1SZesJBmi0l5gE2Ng'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
scheduler = AsyncIOScheduler()
chat_ids = set()

# Милости по времени
auto_messages = [
    "Ты невероятен 🤍",
    "Жизнь становится лучше с тобой 🌸",
    "Пусть твой день будет лёгким как облачко ☁️",
    "Ты приносишь свет в этот мир ☀️"
]

# Послания по кнопке
button_messages = [
    "Ты лучший, даже если не веришь в это 💫",
    "Никогда не сомневайся в себе — ты сияешь! ✨",
    "Ты достоин любви, радости и всего хорошего 🌷",
    "Хорошего тебе дня, герой 🤍"
]

# Кнопка
keyboard = InlineKeyboardMarkup().add(
    InlineKeyboardButton("Получить тёплое послание 💌", callback_data="motivate")
)

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    chat_ids.add(message.chat.id)
    await message.answer("Привет! Я тут, чтобы напоминать тебе, какой ты классный 🫶", reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data == "motivate")
async def button_handler(callback_query: types.CallbackQuery):
    msg = random.choice(button_messages)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, msg)

# Авторассылка
async def scheduled_message():
    for chat_id in chat_ids:
        msg = random.choice(auto_messages)
        try:
            await bot.send_message(chat_id, msg)
        except Exception as e:
            print(f"Ошибка для chat_id {chat_id}: {e}")

async def main():
    scheduler.add_job(scheduled_message, "interval", hours=3)
    scheduler.start()
    await dp.start_polling()

if __name__ == '__main__':
    asyncio.run(main())
