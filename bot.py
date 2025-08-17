import asyncio
import random
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import CommandStart
from aiogram.client.default import DefaultBotProperties
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiohttp import web

API_TOKEN = 'твой_токен_бота'  # <-- сюда вставь свой токен, который у тебя был

# Загружаем фразы из файла
with open("messages.txt", "r", encoding="utf-8") as file:
    phrases = [line.strip() for line in file if line.strip()]

bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())

scheduler = AsyncIOScheduler()
chat_ids = set()

# Кнопка с новым текстом и милым смайликом
keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="хочу мимими 🥺", callback_data="motivate")]
    ]
)

@dp.message(CommandStart())
async def start_handler(message: types.Message):
    chat_ids.add(message.chat.id)
    await message.answer("приветики! я тут, что бы напоминать тебе какой ты у меня любими 🐾🤍", reply_markup=keyboard)

@dp.callback_query()
async def button_handler(callback: types.CallbackQuery):
    msg = random.choice(phrases)
    await callback.message.answer(msg)
    await callback.answer()

async def scheduled_message():
    for chat_id in chat_ids:
        try:
            msg = random.choice(phrases)
            await bot.send_message(chat_id, msg)
        except Exception as e:
            print(f"Ошибка при отправке: {e}")

async def handle(request):
    return web.Response(text="OK")

async def start():
    scheduler.add_job(scheduled_message, "interval", hours=3)
    scheduler.start()
    await dp.start_polling(bot)

async def main():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 10000)
    await site.start()

    await start()

if __name__ == '__main__':
    asyncio.run(main())
