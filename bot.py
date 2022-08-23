import logging
import os
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_webhook
from aiogram import Bot, types
from aiogram.types import ContentType

from PythonFiles.callback_handler import callback_handler_processing
from PythonFiles.message_handler import message_handler
import Keyboard.keyboard as keyboard
import PythonFiles.variables as var
import database as db
from PythonFiles.send_message import reply_message
from functions import set_language_dict, set_default_values_entered_mode

API_TOKEN = '5410734233:AAF7Mpwsm5R-VZ_XenQWwRUbnkrVHsyHVqo'

TOKEN = os.getenv('BOT_TOKEN')
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

HEROKU_APP_NAME = os.getenv('HEROKU_APP_NAME')

# webhook settings
WEBHOOK_HOST = f'https://{HEROKU_APP_NAME}.herokuapp.com'
WEBHOOK_PATH = f'/webhook/{TOKEN}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

# webserver settings
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = os.getenv('PORT', default=8000)


async def on_startup(dispatcher=''):
    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)


async def on_shutdown(dispatcher=''):
    await bot.delete_webhook()


db.create_table('users', var.get_users_table_create_columns())  # создрается БД users


# Срабатывает при запуске бота или команде /start или /help
@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    user_id = str(message.from_user.id)
    # check if user exists, if not insert data to table and create personal user table
    # Проверяется в таблице users наличие пользователя с текущим id, если есть то возвращается True
    check_var = db.check_table('users', 'language', 'digit_id', user_id)
    if not check_var:  # тут вписываются значения нового пользователя в таблицу users и создается новая персональная
        # таблица пользователя
        db.insert_values_in_table('users', var.get_user_table_columns(), f"{message.from_user.id}, "
                                                                         f"'@{message.from_user.username}', "
                                                                         f"'{message.from_user.first_name}', "
                                                                         f"'{message.from_user.last_name}', 'UA'")
    db.create_table(f"t{user_id}", var.get_user_personal_create_table_columns())

    set_language_dict(user_id)  # проверяется поле языка для пользователя в БД, на основе полученных данных
    # устанавливается язык словаря для бота; эта ф-ция вызывается везде в обработчиках, для избегания неприятностей
    # если бот остановился
    set_default_values_entered_mode(user_id, 'forced_update')  # чтобы не было проблем при нажатии команд когда
    # выполняется ввод данных
    dictionary_bot = var.dictionary_bot[user_id]
    markup = keyboard.reply_keyboard(var.main_menu_buttons(dictionary_bot), 2, True, False)

    await bot.send_message(message.from_user.id, dictionary_bot['start_message'], reply_markup=markup)


@dp.callback_query_handler()
async def inline_kb_answer_callback_handler(query: types.CallbackQuery):
    answer_data = query.data
    # always answer callback queries, even if you have nothing to say
    set_default_values_entered_mode(query.from_user.id, 'default_update')
    await query.answer(f'You answered with {answer_data!r}')
    await callback_handler_processing(bot, query, answer_data, str(query.from_user.id))


@dp.message_handler()
async def echo(message: types.Message):
    user_id = str(message.from_user.id)
    set_language_dict(user_id)

    await message_handler(bot, message, user_id)


@dp.message_handler(content_types=ContentType.ANY)
async def unknown_message(msg: types.Message):

    await reply_message(msg, 'и шо это', '')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
