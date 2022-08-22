from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ContentType

API_TOKEN = '5410734233:AAF7Mpwsm5R-VZ_XenQWwRUbnkrVHsyHVqo'

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


# Срабатывает при запуске бота или команде /start или /help
@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):

    await bot.send_message(message.from_user.id, 'hello')


@dp.callback_query_handler()
async def inline_kb_answer_callback_handler(query: types.CallbackQuery):
    pass


@dp.message_handler()
async def echo(message: types.Message):
    await bot.send_message(message.from_user.id, 'kek')


@dp.message_handler(content_types=ContentType.ANY)
async def unknown_message(msg: types.Message):
    pass

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
