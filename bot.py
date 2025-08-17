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
from aiohttp import web  # 👈 Для фейкового HTTP-сервера

API_TOKEN = '8335218158:AAGQsXxGCc0qDOolAW1SZesJBmi0l5gE2Ng'

bot = Bot(
    token=API_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher(storage=MemoryStorage())
dp.message.middleware(CallbackAnswerMiddleware())

scheduler = AsyncIOScheduler()
chat_ids = set()

# Сообщения для авторассылки (оставляем как есть)
auto_messages = [
    "Ты невероятен 🤍",
    "Жизнь становится лучше с тобой 🌸",
    "Пусть твой день будет лёгким как облачко ☁️",
    "Ты приносишь свет в этот мир ☀️"
]

# Сообщения для кнопки мотивации (оставляем как есть)
button_messages = [
    "Ты лучший, даже если не веришь в это 💫",
    "Никогда не сомневайся в себе — ты сияешь! ✨",
    "Ты достоин любви, радости и всего хорошего 🌷",
    "Хорошего тебе дня, герой 🤍"
]

# Считаем мимими-фразы из файла messages.txt
with open("messages.txt", encoding="utf-8") as f:
    mimi_phrases = [line.strip() for line in f if line.strip()]

# Клавиатура с двумя кнопками: мотивация и мимими
keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Получить тёплое послание 💌", callback_data="motivate")],
        [InlineKeyboardButton(text="хочу мимими 🥺", callback_data="mimimi")]
    ]
)

@dp.message(CommandStart())
async def start_handler(message: types.Message):
    chat_ids.add(message.chat.id)
    await message.answer("Привет! Я тут, чтобы напоминать тебе, какой ты классный 🫶\n\nНажми кнопку ниже, чтобы получить мотивацию или мимими!", reply_markup=keyboard)

@dp.callback_query()
async def button_handler(callback: types.CallbackQuery):
    if callback.data == "motivate":
        msg = random.choice(button_messages)
        await callback.message.answer(msg)
        await callback.answer()
    elif callback.data == "mimimi":
        if mimi_phrases:
            msg = random.choice(mimi_phrases)
            await callback.message.answer(msg)
        else:
            await callback.message.answer("Мимими пока нет, скоро добавим! 🥹")
        await callback.answer()

async def scheduled_message():
    for chat_id in chat_ids:
        try:
            msg = random.choice(auto_messages)
            await bot.send_message(chat_id, msg)
        except Exception as e:
            print(f"Ошибка при отправке: {e}")

# 👇 Фейковый HTTP-сервер для Render
async def handle(request):
    return web.Response(text="OK")

async def start():
    scheduler.add_job(scheduled_message, "interval", hours=3)
    scheduler.start()
    await dp.start_polling(bot)

# 👇 Запуск Telegram-бота и веб-сервера
async def main():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 10000)  # Порт 10000
    await site.start()

    await start()

if __name__ == '__main__':
    asyncio.run(main())
