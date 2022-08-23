import PythonFiles.variables as var
from Keyboard import keyboard
from PythonFiles.menu_buttons_handler import calendar_buttons_processing, frequency_callback_processing, \
    reminder_set_callback_processing, show_events_button_processing, change_event_month
from PythonFiles.send_message import simple_message, message_with_text, delete_message, edit_message
from functions import set_language_dict, set_default_values_entered_mode
import database as db


async def callback_handler_processing(bot, query, answer_data, user_id):
    try:
        set_language_dict(user_id)
        set_default_values_entered_mode(user_id, 'default_update')

        send_message_type_list = []
        sent_message = ''

        #############################################################
        #  language settings ########################################
        #  Выполняется установка языка в боте с помощью inline кнопок
        #############################################################
        if answer_data == 'UA' or answer_data == 'EN':
            db.update_table_values('users', 'language', str(answer_data), 'digit_id', f"{user_id}")
            set_language_dict(user_id)
            text = var.dictionary_bot[user_id]['current_language_message']
            markup = keyboard.inline_keyboard(var.languages_callback_button(var.dictionary_bot[user_id],
                                                                            var.language_var[user_id]), None, 3)
            temp_list = [text, markup, 'edit_message_text']

            send_message_type_list.append(temp_list)
        ################################
        #  calendar's buttons processing
        ################################
        elif answer_data in var.get_calendar_callback_button():
            send_message_type_list = calendar_buttons_processing(answer_data, user_id, var.dictionary_bot[user_id])
        ##########################
        #  frequency inline button
        ##########################
        elif answer_data in var.get_set_reminder_callback():
            send_message_type_list = reminder_set_callback_processing(answer_data, user_id)
        elif answer_data in var.get_frequency_callback():
            send_message_type_list = frequency_callback_processing(answer_data, user_id)

        elif answer_data in var.get_show_event_inline_button_list():
            var.enter_mode_counter[user_id] = 10
            send_message_type_list = show_events_button_processing(answer_data, var.dictionary_bot[user_id], user_id)

        elif answer_data in var.get_buttons_check_events_list():
            send_message_type_list = change_event_month(answer_data, user_id, var.dictionary_bot[user_id])

        ############################
        #  main menu inline keyboard
        ############################
        elif answer_data == 'main_menu':

            text = var.dictionary_bot[user_id]['main_menu']
            markup = keyboard.reply_keyboard(var.main_menu_buttons(var.dictionary_bot[user_id]), 2, True, False)
            temp_list = [text, markup, 'simple_message']
            send_message_type_list.append(temp_list)

            text = var.dictionary_bot[user_id]['current_language_message']
            markup = ''
            temp_list = [text, markup, 'edit_message_text']
            send_message_type_list.append(temp_list)

        #####################
        #  send message block
        #####################
        for i in send_message_type_list:
            if i[2] == "edit_message_text":
                sent_message = edit_message(bot, query.from_user.id, query.message.message_id, i[0], i[1])
            elif i[2] == "simple_message":
                sent_message = simple_message(bot, query.from_user.id, i[0], i[1])
            elif i[2] == "message_with_text":
                sent_message = message_with_text(bot, query, i[0], i[1])
            elif i[2] == 'delete_message':
                sent_message = delete_message(bot, query.from_user.id, query.message.message_id)

            await sent_message

        print('''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''')
        print(f"Enter_mode of user - {user_id}: {var.enter_mode[user_id]}")
        print(f"Entered_data of user - {user_id}: {var.entered_data[user_id]}")
        print(f"Enter_mode_counter of user - {user_id}: {var.enter_mode_counter[user_id]}")
        print(f"Calendar_current_date of user - {user_id}: {var.calendar_current_date}")
        print('''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''')
    except BaseException:
        pass
