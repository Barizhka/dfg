import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from config import *
logging.basicConfig(level=logging.INFO)

bot = Bot(token=bottoken)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    with open('image.png', 'rb') as photo:
        keyboard = InlineKeyboardMarkup(row_width=1)
        web_app_button = InlineKeyboardButton(
            text="Открыть кейс",
            web_app=WebAppInfo(url=weburl) 
        )
        channel_button = InlineKeyboardButton(
            text="Наш канал",
            url=youchannel
        )
        keyboard.add(web_app_button, channel_button)
        
        await message.answer_photo(
            photo,
            caption="🎁🎁🎁\n\nДОБРО ПОЖАЛОВАТЬ\n\nАктуальные раздачи:\n\n💍 Кольцо за подписку на канал.\nстоим. 100 ⭐️\n\n🔹 Инструкция: /help\n🔹 Вызвать меню повторно: /start",
            reply_markup=keyboard
        )

@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    keyboard = InlineKeyboardMarkup()
    back_button = InlineKeyboardButton(text="Назад", callback_data="back_to_start")
    keyboard.add(back_button)
    
    await message.answer(
        f"❔❔❔\n\nИНСТРУКЦИЯ:\n\n1️⃣ Перейдите в настройки\n2️⃣ Нажмите на вкладку Telegram Для бизнеса\n3️⃣ Выберите раздел Чат-боты\n4️⃣ В поисковую строку введите @{youbot}\n5️⃣ Нажмите на кнопку Добавить \n☑️ Поставьте галочку рядом с Управление подарками и звездами\n\n✅ Все готово! Бот должен автоматически отправить вам награду если вы выполнили условия раздачи\n\n⭕️ ВАЖНО: Чтобы избежать абуза нашей системы, вы можете получить раздачу только имея премиум-статус в Telegram",
        reply_markup=keyboard
    )

@dp.callback_query_handler(lambda c: c.data == 'back_to_start')
async def process_callback_back(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await send_welcome(callback_query.message)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)