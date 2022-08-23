from aiogram import types


# when function is calling should enter buttons in tuple, if needs one button in row it should be just string
def reply_keyboard(buttons, row_width, resize, one_time_keyboard):
    keyboard_markup = types.ReplyKeyboardMarkup(row_width=row_width, resize_keyboard=resize,
                                                one_time_keyboard=one_time_keyboard)
    for i in buttons:
        if type(buttons) is str:  # если кнопка одна, то добавляется кнопка и возвращается
            return keyboard_markup.add(buttons)
        if type(i) is tuple:
            keyboard_markup.add(*(types.KeyboardButton(text) for text in i))
        else:
            keyboard_markup.add(i)

    return keyboard_markup


def inline_keyboard(buttons, link_button, row_width):
    keyboard_markup = types.InlineKeyboardMarkup(row_width=row_width)

    if buttons is not None:
        for i in buttons:
            if type(i) is tuple:
                keyboard_markup.add(*(types.InlineKeyboardButton(text, callback_data=data) for text, data in i))
            else:
                # single button should write with list [], for example ['SomeButton', 'data']
                keyboard_markup.add(types.InlineKeyboardButton(i[0], callback_data=i[1]))

    if link_button is not None:
        keyboard_markup.add(types.InlineKeyboardButton(link_button[0], url=link_button[1]),)

    return keyboard_markup
