import PythonFiles.variables as var


async def simple_message(bot, chat_id, text, markup):
    return await bot.send_message(chat_id, text, parse_mode="HTML", reply_markup=markup,
                                  disable_web_page_preview=True)


async def message_with_text(bot, message, text, markup):
    user_id = str(message.from_user.id)
    kek = await bot.send_message(user_id, text, parse_mode="HTML", reply_markup=markup,
                                 disable_web_page_preview=True)
    # запоминается сообщение, которое нужно будет изменить
    var.message_to_edit[user_id].append(kek['message_id'])


async def reply_message(message, text, markup):
    return await message.reply(text, parse_mode="HTML", reply_markup=markup, disable_web_page_preview=True)


async def edit_message(bot, chat_id, message_id, text, markup):

    return await bot.edit_message_text(text=text, chat_id=chat_id, parse_mode="HTML", message_id=message_id,
                                       reply_markup=markup)


async def delete_message(bot, chat_id, message_id):
    return await bot.delete_message(chat_id=chat_id, message_id=message_id)
