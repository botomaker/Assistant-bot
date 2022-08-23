import Keyboard.keyboard as keyboard
import PythonFiles.variables as var
from PythonFiles.menu_buttons_handler import process_menu_buttons_handler, enter_mode_add_processing, \
    enter_mode_edit_event_processing
from PythonFiles.send_message import message_with_text, simple_message, reply_message, delete_message, edit_message
from functions import set_default_values_entered_mode


async def message_handler(bot, message, user_id):
    # идёт сброс всех переменных, на случай если бот остановился
    set_default_values_entered_mode(user_id, 'default_update')

    send_message_type_list = []  # переменная куда будут заносится сообщения для отправки, в виде списка, потому что
    # может быть несколько сообщений
    sent_message = ''

    # main menu button
    if message.text == var.dictionary_bot[user_id]['main_menu']:
        set_default_values_entered_mode(user_id, 'forced_update')
        try:
            send_message_type_list.append([var.message_to_edit[user_id][-1], '', 'delete_message'])
        except BaseException:
            pass
        text = message.text
        markup = keyboard.reply_keyboard(var.main_menu_buttons(var.dictionary_bot[user_id]), 2, True, False)
        temp_list = [text, markup, 'simple_message']
        send_message_type_list.append(temp_list)

    # Enter edit mode
    elif len(var.edit_enter_data_mode) >= 0 and var.edit_enter_data_mode[user_id]:
        send_message_type_list = enter_mode_edit_event_processing(message, var.dictionary_bot[user_id], user_id)


    # Enter mode
    # Выполняется проверка есть ли данные в enter_mode и включен ли enter_mode для конкретного пользователя
    elif len(var.enter_mode) >= 0 and var.enter_mode[user_id]:
        send_message_type_list = enter_mode_add_processing(message, var.dictionary_bot[user_id], user_id)

    # Menu buttons processing
    elif message.text in var.get_menu_buttons_list(var.dictionary_bot[user_id]):
        var.enter_mode_counter[user_id] = 1
        send_message_type_list = process_menu_buttons_handler(message, var.dictionary_bot[user_id],
                                                              var.language_var[user_id], user_id)

    # random words
    # на рандомные слова бот отвечает репли месседжем
    else:
        try:
            if var.show_month_res[user_id]['current_counter'] >= 0:
                send_message_type_list.append([var.message_to_edit[user_id][-1], '', 'delete_message'])
        except BaseException:
            pass
        finally:
            text = var.dictionary_bot[user_id]['reply_answer']
            markup = keyboard.reply_keyboard(var.main_menu_buttons(var.dictionary_bot[user_id]), 2, True, False)
            temp_list = [text, markup, "reply_message"]
            send_message_type_list.append(temp_list)

    # send message block
    for i in send_message_type_list:
        try:
            if i[2] == "edit_message_text":
                sent_message = edit_message(bot, i[3], i[4], i[0], i[1])
            elif i[2] == "message_with_text":
                sent_message = message_with_text(bot, message, i[0], i[1])
            elif i[2] == "simple_message":
                sent_message = simple_message(bot, user_id, i[0], i[1])
            elif i[2] == "reply_message":
                sent_message = reply_message(message, i[0], i[1])
            elif i[2] == 'delete_message':
                sent_message = delete_message(bot, user_id, i[0])

            await sent_message

        except BaseException:
            pass

    print('''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''')
    print(f"Enter_mode of user - {user_id}: {var.enter_mode[user_id]}")
    print(f"Entered_data of user - {user_id}: {var.entered_data[user_id]}")
    print(f"Enter_mode_counter of user - {user_id}: {var.enter_mode_counter[user_id]}")
    print(f"Calendar_current_date of user - {user_id}: {var.calendar_current_date}")
    print('''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''')
