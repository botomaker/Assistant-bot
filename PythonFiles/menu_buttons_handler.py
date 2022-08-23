from PythonFiles.variables import main_menu_buttons, settings_menu_buttons, events_menu_buttons, \
    languages_callback_button
import Keyboard.keyboard as keyboard
import PythonFiles.variables as var
import database as db
from functions import set_default_values_entered_mode, calendar_buttons_creating, \
    switch_month, check_datetime_format, get_select_event_count, get_select_events_data, get_current_date


##########################################
# Функция обработки нажатий на кнопки меню
##########################################
def process_menu_buttons_handler(message, dictionary_bot, language, user_id):
    send_message_type_list = []

    # about bot button
    if message.text == dictionary_bot['aboutbot_button']:
        text = dictionary_bot['aboutbot_text']
        markup = keyboard.reply_keyboard([dictionary_bot['back_button']], 2, True, False)
        temp_list = [text, markup, 'message_with_text']
        send_message_type_list.append(temp_list)

    # back button
    elif message.text == dictionary_bot['back_button']:
        text = message.text
        markup = keyboard.reply_keyboard(main_menu_buttons(dictionary_bot), 2, True, False)
        temp_list = [text, markup, 'simple_message']
        send_message_type_list.append(temp_list)

    # settings button
    elif message.text == dictionary_bot['settings_button']:
        text = message.text
        markup = keyboard.reply_keyboard(settings_menu_buttons(dictionary_bot), 2, True, True)
        temp_list = [text, markup, 'simple_message']
        send_message_type_list.append(temp_list)

    # change language button
    elif message.text == dictionary_bot['change_language_button']:
        text = dictionary_bot['current_language_message']
        markup = keyboard.inline_keyboard(languages_callback_button(dictionary_bot, language), None, 3)
        temp_list = [text, markup, 'message_with_text']
        send_message_type_list.append(temp_list)

    # events button
    elif message.text == dictionary_bot['events_button']:
        text = message.text
        markup = keyboard.reply_keyboard(events_menu_buttons(dictionary_bot), 3, True, True)
        temp_list = [text, markup, 'simple_message']
        send_message_type_list.append(temp_list)

    # add_event button
    elif message.text == dictionary_bot['add_event']:
        var.enter_mode[user_id] = True
        text = dictionary_bot['enter_name_of_the_event']
        markup = keyboard.reply_keyboard(dictionary_bot['main_menu'], 1, True, True)
        temp_list = [text, markup, 'message_with_text']
        send_message_type_list.append(temp_list)

    elif message.text == dictionary_bot['show_events']:
        count_of_event = get_select_event_count(user_id)

        text = f"{dictionary_bot['show_month_events_txt1']} {count_of_event}{var.notes_smile}"
        markup = keyboard.reply_keyboard(dictionary_bot['main_menu'], 1, True, True)
        temp_list = [text, markup, 'message_with_text']
        send_message_type_list.append(temp_list)

        text = dictionary_bot['show_month_events_txt2']
        markup = keyboard.inline_keyboard(var.get_show_events_inline_buttons(dictionary_bot), None, 2)
        temp_list = [text, markup, 'message_with_text']
        send_message_type_list.append(temp_list)

    return send_message_type_list


##################################################################
# Функция обработки вводимых сообщений в режиме добавления событий
##################################################################
def enter_mode_add_processing(message, dictionary_bot, user_id):
    # var.enter_mode_counter - счётчик шагов ввода
    # для вывода текста используется словарь add_enter_mode_text в файле variables, каждый шаг отвечает определенному
    # ключу слвоаря

    send_message_type_list = []

    ######################################################################################################
    ######################################################################################################
    # STEP 1 - Ввод короткого описания
    ######################################################################################################
    ######################################################################################################
    if var.enter_mode_counter[user_id] == 1:  # STEP 1
        text = dictionary_bot[var.add_enter_mode_text(var.enter_mode_counter[user_id])]
        markup = ''
        temp_list = [text, markup, 'message_with_text']
        send_message_type_list.append(temp_list)

        var.enter_mode_counter[user_id] = 2
        var.entered_data[user_id].append(message.text)  # эта переменная сохраняет введенные пользователем значения

    ######################################################################################################
    ######################################################################################################
    # STEP 2 - Выбор даты события
    ######################################################################################################
    ######################################################################################################
    elif var.enter_mode_counter[user_id] == 2:  # STEP 2

        text = dictionary_bot[var.add_enter_mode_text(var.enter_mode_counter[user_id])]
        # markup делается inline клавиатурой в виде календаря
        markup = keyboard.inline_keyboard(calendar_buttons_creating(dictionary_bot, user_id, None, None), None, 7)
        temp_list = [text, markup, 'message_with_text']

        send_message_type_list.append(temp_list)

        var.enter_mode_counter[user_id] = 3
        var.entered_data[user_id].append(message.text)  # эта переменная сохраняет введенные пользователем значения

    ################################################################################################################
    ################################################################################################################
    # STEP 3 - Проверяется введенная дата и в случае успеха изменяется сообщение с календарем(удаляется клавиатура и
    # новая надпись вписывается) и присылается следующее сообщение "выбрать периодичность события"
    ################################################################################################################
    ################################################################################################################
    elif var.enter_mode_counter[user_id] == 3:  # STEP 3
        # check data input format
        if check_datetime_format(str(message.text)):
            if var.edit_enter_data_mode[user_id]:
                pass
            text = var.dictionary_bot[user_id][var.add_enter_mode_text(var.enter_mode_counter[user_id])]
            markup = keyboard.inline_keyboard(var.set_reminder_callback_button(var.dictionary_bot[user_id]), None, 2)
            temp_list = [text, markup, 'message_with_text']
            send_message_type_list.append(temp_list)

            var.entered_data[user_id].append(message.text)  # эта переменная сохраняет введенные пользователем значения

            text = var.dictionary_bot[user_id]['selected_date_txt'] + str(var.entered_data[user_id][2])

            temp_list = [text, '', 'edit_message_text', user_id, var.message_to_edit[user_id][-1]]
            send_message_type_list.append(temp_list)
            var.enter_mode_counter[user_id] = 4

        #  if data input is incorrect
        else:
            var.enter_mode_counter[user_id] = 3
            text = dictionary_bot['incorrect_data_format']
            markup = ''
            temp_list = [text, markup, 'reply_message']
            send_message_type_list.append(temp_list)

    ######################################################################################################
    ######################################################################################################
    # STEP 4
    ######################################################################################################
    ######################################################################################################
    elif var.enter_mode_counter[user_id] == 4:  # STEP 4
        print(str(message.text))
        if str(message.text).title() in var.get_set_reminder_callback_button(var.dictionary_bot[user_id]):
            if str(message.text).title() == var.get_set_reminder_callback_button(var.dictionary_bot[user_id])[0]:
                text = dictionary_bot[var.add_enter_mode_text(var.enter_mode_counter[user_id])]
                # markup делается inline клавиатурой в виде календаря
                markup = keyboard.inline_keyboard(var.get_frequency_buttons(dictionary_bot), None, 2)
                temp_list = [text, markup, 'message_with_text']
                send_message_type_list.append(temp_list)

                text = var.dictionary_bot[user_id][var.add_enter_mode_text(var.enter_mode_counter[user_id] - 1)]

                temp_list = [text, '', 'edit_message_text', user_id, var.message_to_edit[user_id][-1]]
                send_message_type_list.append(temp_list)

                var.enter_mode_counter[user_id] = 5

            elif str(message.text).title() == var.get_set_reminder_callback_button(var.dictionary_bot[user_id])[1]:
                text = var.dictionary_bot[user_id][var.add_enter_mode_text(var.enter_mode_counter[user_id] - 1)]
                temp_list = [text, '', 'edit_message_text', user_id, var.message_to_edit[user_id][-1]]
                send_message_type_list.append(temp_list)

                var.entered_data[user_id] += ['0', '0', '0']
                text = var.get_reply_text_save_add_data(var.dictionary_bot[user_id], var.entered_data[user_id],
                                                        'yes_allright')
                markup = keyboard.reply_keyboard(var.get_save_final_buttons(var.dictionary_bot[user_id]), 2, True,
                                                 False)
                temp_list = [text, markup, 'message_with_text']
                send_message_type_list.append(temp_list)

                var.enter_mode_counter[user_id] = 8
        else:
            send_message_type_list.append([var.message_to_edit[user_id][-1], '', 'delete_message'])

            text = dictionary_bot['reply_answer']
            markup = ''
            temp_list = [text, markup, 'reply_message']
            send_message_type_list.append(temp_list)

            text = var.dictionary_bot[user_id][var.add_enter_mode_text(var.enter_mode_counter[user_id] - 1)]
            markup = keyboard.inline_keyboard(var.set_reminder_callback_button(var.dictionary_bot[user_id]), None, 2)
            temp_list = [text, markup, 'message_with_text']
            send_message_type_list.append(temp_list)

    ######################################################################################################
    ######################################################################################################
    # STEP 5 - Проверяется корректность данных периодичности события и предлагается выбор даты напоминания
    # (опять календарь создается)
    ######################################################################################################
    ######################################################################################################
    elif var.enter_mode_counter[user_id] == 5:  # STEP 5
        if str(message.text).lower() in var.get_frequency_buttons_list(var.dictionary_bot[user_id]):

            text = dictionary_bot[var.add_enter_mode_text(var.enter_mode_counter[user_id])]
            # markup делается inline клавиатурой в виде календаря
            markup = keyboard.inline_keyboard(calendar_buttons_creating(dictionary_bot, user_id, None, None), None, 7)
            temp_list = [text, markup, 'message_with_text']
            send_message_type_list.append(temp_list)

            var.entered_data[user_id].append(message.text)  # эта переменная сохраняет введенные пользователем значения

            text = var.dictionary_bot[user_id]['frequency_is_txt'] + str(var.entered_data[user_id][3])

            temp_list = [text, '', 'edit_message_text', user_id, var.message_to_edit[user_id][-1]]
            send_message_type_list.append(temp_list)
            var.enter_mode_counter[user_id] = 6

        else:
            var.enter_mode_counter[user_id] = 5
            text = dictionary_bot['enter_correct_frequency']
            markup = ''
            temp_list = [text, markup, 'reply_message']
            send_message_type_list.append(temp_list)

    ####################################################################################################################
    ####################################################################################################################
    # STEP 6 - Проверется введенная дата напоминания, в случае  успеха изменяется сообщение с календарем(удаляется
    # клавиатура и новая надпись вписывается) и присылается следующее сообщение "Укажите время напоминания в формате..."
    ####################################################################################################################
    ####################################################################################################################
    elif var.enter_mode_counter[user_id] == 6:  # STEP 6
        if check_datetime_format(str(message.text)):
            text = var.dictionary_bot[user_id]['enter_time_of_the_rimender']
            temp_list = [text, '', 'message_with_text']
            send_message_type_list.append(temp_list)

            var.entered_data[user_id].append(message.text)  # эта переменная сохраняет введенные пользователем значения

            text = var.dictionary_bot[user_id]['reminder_date_is_txt'] + str(var.entered_data[user_id][4])

            temp_list = [text, '', 'edit_message_text', user_id, var.message_to_edit[user_id][-1]]
            send_message_type_list.append(temp_list)
            var.enter_mode_counter[user_id] = 7
        else:
            var.enter_mode_counter[user_id] = 6
            text = dictionary_bot['enter_correct_date_reminder']
            markup = ''
            temp_list = [text, markup, 'reply_message']
            send_message_type_list.append(temp_list)

    ##################################################################################################################
    ##################################################################################################################
    # ЗРОБИТИ ОБРОБКУ
    # STEP 7 - Проверется введенное время напоминания и в случе успеха присылается финальная фраза режима ввода данных
    ##################################################################################################################
    ##################################################################################################################
    elif var.enter_mode_counter[user_id] == 7:  # STEP 7
        if check_datetime_format(str(message.text)):
            var.entered_data[user_id].append(message.text)  # эта переменная сохраняет введенные пользователем значения

            text = var.get_reply_text_save_add_data(dictionary_bot, var.entered_data[user_id], 'yes_allright')
            markup = keyboard.reply_keyboard(var.get_save_final_buttons(dictionary_bot), 2, True, False)
            temp_list = [text, markup, 'message_with_text']
            send_message_type_list.append(temp_list)

            var.enter_mode_counter[user_id] = 8
        else:
            var.enter_mode_counter[user_id] = 7
            text = dictionary_bot['enter_correct_time']
            markup = ''
            temp_list = [text, markup, 'reply_message']
            send_message_type_list.append(temp_list)

    else:
        if message.text == dictionary_bot['yes_btn']:
            print('yes')
            text = dictionary_bot['save_event_final_text']
            markup = keyboard.reply_keyboard(var.main_menu_buttons(dictionary_bot), 2, True, False)
            temp_list = [text, markup, 'message_with_text']
            send_message_type_list.append(temp_list)

            db.insert_values_in_table(f"t{user_id}", var.get_user_personal_table_columns(),
                                      f"'{var.entered_data[user_id][0]}', "
                                      f"'{var.entered_data[user_id][1]}', "
                                      f"'{var.entered_data[user_id][2]}', "
                                      f"'{var.entered_data[user_id][3]}', "
                                      f"'{var.entered_data[user_id][4]}', "
                                      f"'{var.entered_data[user_id][5]}'")

            set_default_values_entered_mode(user_id, 'forced_update')

        else:
            set_default_values_entered_mode(user_id, 'forced_update')
            text = dictionary_bot['reply_answer']
            markup = keyboard.reply_keyboard(var.main_menu_buttons(dictionary_bot), 2, True, False)
            temp_list = [text, markup, 'reply_message']
            send_message_type_list.append(temp_list)

    return send_message_type_list


######################################################
# Функция обработки нажатий на inline кнопки календаря
######################################################
def calendar_buttons_processing(answer_data, user_id, dictionary_bot):
    send_message_type_list = []
    # if bot off если переменная enter_mode_counter = 0, то это значит, что бот приостановился или тп,
    # происходит обработка с reply_message
    if var.enter_mode_counter[user_id] == 1:
        text = var.dictionary_bot[user_id]['something_happened']
        markup = ''
        temp_list = [text, markup, 'edit_message_text']
        send_message_type_list.append(temp_list)

    # switch months переключение месяцев, получаются текущие установленные год и месяц в боте (из ф-ции
    # создания кнопок календаря) и в ф-ции switch_month происходит увеличение/уменьшение месяца
    elif answer_data == 'prev_month' or answer_data == 'next_month':
        year, month = int(var.calendar_current_date[user_id]['year']), \
                      int(var.calendar_current_date[user_id]['month'])

        year, month = switch_month(year, month, str(answer_data))
        res = get_select_events_data(user_id, year, month)
        var.show_month_res[user_id]['res'] = res
        var.show_month_res[user_id]['count'] = len(res)
        var.show_month_res[user_id]['current_counter'] = 0

        k = []
        for i in res:
            k.append(i[2][:2])
        k = list(map(int, k))

        text = var.dictionary_bot[user_id]['choose_date_of_the_event']
        markup = keyboard.inline_keyboard(calendar_buttons_creating(var.dictionary_bot[user_id], user_id, year, month,
                                                                    k), None, 7)
        temp_list = [text, markup, 'edit_message_text']
        send_message_type_list.append(temp_list)

    elif answer_data == 'year_month':
        year, month = int(var.calendar_current_date[user_id]['year']), \
                      int(var.calendar_current_date[user_id]['month'])
        text = f"{dictionary_bot['events_for_month']}{dictionary_bot['month'][int(month)]} {year}"
        markup = ''
        temp_list = [text, markup, 'edit_message_text']
        send_message_type_list.append(temp_list)

        res = get_select_events_data(user_id)
        var.show_month_res[user_id]['res'] = res
        var.show_month_res[user_id]['count'] = len(res)
        var.show_month_res[user_id]['current_counter'] = 0

        text = var.get_reply_text_save_add_data(dictionary_bot, res[0], 'no_allright')
        markup = keyboard.inline_keyboard(
            var.get_buttons_check_events(var.show_month_res[user_id]['current_counter'] + 1,
                                         var.show_month_res[user_id]['count'],
                                         dictionary_bot), None, 3)

        temp_list = [text, markup, 'message_with_text']
        send_message_type_list.append(temp_list)


    # Обработка кнопок календаря (числа)
    else:
        #  идет обрезка кнопки так как она создается с пробелом в начале ' 9' и проверка, является ли цифрой
        if str(answer_data)[1:].isdigit():
            year = var.calendar_current_date[user_id]['year']
            month = var.calendar_current_date[user_id]['month']

            # добавляется нолик к месяцу
            if len(str(month)) == 1:
                month = f"0{month}"
            answer_data = answer_data[1:]

            # добавляется нолик к дню
            if len(str(answer_data)) == 1:
                answer_data = f"0{str(answer_data)}"
            date_res = f"{answer_data}.{month}.{year}"

            # добавляется дата в массив со всеми введенными данными
            var.entered_data[user_id].append(date_res)
            text = ''

            if var.enter_mode_counter[user_id] == 3:

                # изменяется сообщение с календарем (убирается inline keyboard и изменяется текст)
                if not var.edit_enter_data_mode[user_id]:
                    text = var.dictionary_bot[user_id]['selected_date_txt'] + str(var.entered_data[user_id][2])
                else:
                    send_message_type_list.append(['', '', 'delete_message'])

                    text = var.dictionary_bot[user_id]['selected_date_txt'] + str(var.entered_data[user_id][2])
                    markup = keyboard.reply_keyboard(dictionary_bot['main_menu'], 1, True, True)
                    temp_list = [text, markup, 'message_with_text']
                    send_message_type_list.append(temp_list)

                # создается текст и кнопки для выбора устанавливать напоминание или нет
                text1 = var.dictionary_bot[user_id][var.add_enter_mode_text(var.enter_mode_counter[user_id])]
                markup = keyboard.inline_keyboard(var.set_reminder_callback_button(var.dictionary_bot[user_id]),
                                                  None,
                                                  2)
                temp_list = [text1, markup, 'message_with_text']
                send_message_type_list.append(temp_list)

                var.enter_mode_counter[user_id] = 4

            elif var.enter_mode_counter[user_id] == 6:
                text = var.dictionary_bot[user_id]['enter_time_of_the_rimender']
                temp_list = [text, '', 'message_with_text']
                send_message_type_list.append(temp_list)

                text = var.dictionary_bot[user_id]['reminder_date_is_txt'] + str(var.entered_data[user_id][4])
                var.enter_mode_counter[user_id] = 7

            if not var.edit_enter_data_mode[user_id]:
                markup = ''

                temp_list = [text, markup, 'edit_message_text']
                send_message_type_list.append(temp_list)
            else:
                send_message_type_list.append(['', '', 'delete_message'])
                year, month = int(var.calendar_current_date[user_id]['year']), \
                              int(var.calendar_current_date[user_id]['month'])

                res = get_select_events_data(user_id, year, month)

                kek = []
                for i in res:
                    if answer_data == i[2][:2]:
                        kek.append(i)

                var.show_month_res[user_id]['res'] = kek
                var.show_month_res[user_id]['count'] = len(kek)
                var.show_month_res[user_id]['current_counter'] = 0

                text = var.get_reply_text_save_add_data(dictionary_bot, kek[0], 'no_allright')
                markup = keyboard.inline_keyboard(
                    var.get_buttons_check_events(var.show_month_res[user_id]['current_counter'] + 1,
                                                 var.show_month_res[user_id]['count'],
                                                 dictionary_bot), None, 3)
                temp_list = [text, markup, 'message_with_text']
                send_message_type_list.append(temp_list)

    return send_message_type_list


################################################################
# Функция обработки inline кнопок установить напоминание или нет
################################################################
def reminder_set_callback_processing(answer_data, user_id):
    send_message_type_list = []

    if var.enter_mode_counter[user_id] == 1:
        text = var.dictionary_bot[user_id]['something_happened']
        markup = ''
        temp_list = [text, markup, 'edit_message_text']
        send_message_type_list.append(temp_list)

    else:
        if answer_data == var.get_set_reminder_callback()[0]:
            send_message_type_list.append([var.message_to_edit[user_id][-1], '', 'delete_message'])

            var.enter_mode_counter[user_id] = 5

            text = var.dictionary_bot[user_id][var.add_enter_mode_text(var.enter_mode_counter[user_id])]
            # markup делается inline клавиатурой в виде календаря
            markup = keyboard.inline_keyboard(var.get_frequency_buttons(var.dictionary_bot[user_id]), None, 2)
            temp_list = [text, markup, 'message_with_text']
            send_message_type_list.append(temp_list)
        elif answer_data == var.get_set_reminder_callback()[1]:
            text = var.dictionary_bot[user_id][var.add_enter_mode_text(var.enter_mode_counter[user_id] - 1)]
            temp_list = [text, '', 'edit_message_text', user_id, var.message_to_edit[user_id][-1]]
            send_message_type_list.append(temp_list)
            var.entered_data[user_id] += ['0', '0', '0']
            text = var.get_reply_text_save_add_data(var.dictionary_bot[user_id], var.entered_data[user_id],
                                                    'yes_allright')
            markup = keyboard.reply_keyboard(var.get_save_final_buttons(var.dictionary_bot[user_id]), 2, True, False)
            temp_list = [text, markup, 'message_with_text']
            send_message_type_list.append(temp_list)

            var.enter_mode_counter[user_id] = 8

    return send_message_type_list


#########################################################
# Функция обработки inline кнопок установки периодичности
#########################################################
def frequency_callback_processing(answer_data, user_id):
    send_message_type_list = []

    if var.enter_mode_counter[user_id] == 1:
        text = var.dictionary_bot[user_id]['something_happened']
        markup = ''
        temp_list = [text, markup, 'edit_message_text']
        send_message_type_list.append(temp_list)

    else:
        var.entered_data[user_id].append(var.dictionary_bot[user_id][answer_data])
        text = var.dictionary_bot[user_id]['frequency_is_txt'] + str(var.entered_data[user_id][3])
        markup = ''
        temp_list = [text, markup, 'edit_message_text']
        send_message_type_list.append(temp_list)
        var.enter_mode_counter[user_id] = 6

        text = var.dictionary_bot[user_id]['set_date_of_the_reminder']
        markup = keyboard.inline_keyboard(calendar_buttons_creating(var.dictionary_bot[user_id], user_id, None,
                                                                    None), None, 7)
        temp_list = [text, markup, 'message_with_text']
        send_message_type_list.append(temp_list)

    return send_message_type_list


####################################################################
# Функция обработки inline кнопок показать события, календарь, поиск
####################################################################
def show_events_button_processing(answer_data, dictionary_bot, user_id):
    send_message_type_list = []

    # если нажата кнопка календарь
    if answer_data == var.get_show_event_inline_button_list()[0]:
        var.edit_enter_data_mode[user_id] = True
        res = get_select_events_data(user_id)
        var.show_month_res[user_id]['res'] = res
        var.show_month_res[user_id]['count'] = len(res)
        var.show_month_res[user_id]['current_counter'] = 0

        k = []
        for i in res:
            k.append(i[2][:2])
        k = list(map(int, k))

        temp_list = ['', '', 'delete_message']
        send_message_type_list.append(temp_list)

        text = dictionary_bot['choose_date_of_the_event_short']
        # markup делается inline клавиатурой в виде календаря
        markup = keyboard.inline_keyboard(calendar_buttons_creating(dictionary_bot, user_id, None, None, k), None, 7)
        temp_list = [text, markup, 'message_with_text']
        send_message_type_list.append(temp_list)

    return send_message_type_list


def change_event_month(answer_data, user_id, dictionary_bot):
    send_message_type_list = []

    if var.enter_mode_counter[user_id] == 1:
        text = var.dictionary_bot[user_id]['something_happened']
        markup = ''
        temp_list = [text, markup, 'edit_message_text']
        send_message_type_list.append(temp_list)

    else:
        if answer_data == 'prev_event':

            if var.show_month_res[user_id]['current_counter'] != 0:
                var.show_month_res[user_id]['current_counter'] -= 1
                text = var.get_reply_text_save_add_data(dictionary_bot, var.show_month_res[user_id]['res']
                [var.show_month_res[user_id]['current_counter']], 'no_allright')
                markup = keyboard.inline_keyboard(
                    var.get_buttons_check_events(var.show_month_res[user_id]['current_counter'] + 1,
                                                 var.show_month_res[user_id]['count'],
                                                 dictionary_bot), None, 3)

                temp_list = [text, markup, 'edit_message_text']
                send_message_type_list.append(temp_list)
            else:
                return ''

        elif answer_data == 'next_event':
            if var.show_month_res[user_id]['current_counter'] != var.show_month_res[user_id]['count'] - 1:
                var.show_month_res[user_id]['current_counter'] += 1
                text = var.get_reply_text_save_add_data(dictionary_bot, var.show_month_res[user_id]['res']
                [var.show_month_res[user_id]['current_counter']], 'no_allright')
                markup = keyboard.inline_keyboard(
                    var.get_buttons_check_events(var.show_month_res[user_id]['current_counter'] + 1,
                                                 var.show_month_res[user_id]['count'],
                                                 dictionary_bot), None, 3)

                temp_list = [text, markup, 'edit_message_text']
                send_message_type_list.append(temp_list)
            else:
                return ''

        elif answer_data == 'remove_event':
            text = var.get_reply_text_save_add_data(dictionary_bot, var.show_month_res[user_id]['res']
            [var.show_month_res[user_id]['current_counter']], 'no_allright')
            text += f"\n\n{dictionary_bot['remove_event_txt']}"
            markup = keyboard.inline_keyboard([((dictionary_bot['yes_btn'], 'yes_remove'), (dictionary_bot['no_btn'],
                                                                                            'no_remove'))], None, 3)
            temp_list = [text, markup, 'edit_message_text']
            send_message_type_list.append(temp_list)

        elif answer_data == 'no_remove':
            send_message_type_list.append([var.message_to_edit[user_id][-1], '', 'delete_message'])
            text = var.get_reply_text_save_add_data(dictionary_bot, var.show_month_res[user_id]['res']
            [var.show_month_res[user_id]['current_counter']], 'no_allright')

            markup = keyboard.inline_keyboard(
                var.get_buttons_check_events(var.show_month_res[user_id]['current_counter'] + 1,
                                             var.show_month_res[user_id]['count'],
                                             dictionary_bot), None, 3)

            temp_list = [text, markup, 'message_with_text']
            send_message_type_list.append(temp_list)

        elif answer_data == 'yes_remove':
            event_name = var.show_month_res[user_id]['res'][var.show_month_res[user_id]['current_counter']][0]
            date_event = var.show_month_res[user_id]['res'][var.show_month_res[user_id]['current_counter']][2]
            var.show_month_res[user_id]['res'].pop(var.show_month_res[user_id]['current_counter'])
            print(var.show_month_res[user_id]['res'])
            var.show_month_res[user_id]['current_counter'] = 0
            var.show_month_res[user_id]['count'] = len(var.show_month_res[user_id]['res'])

            db.delete_values_from_table(f't{user_id}', 'event', event_name, 'date_of_the_event', date_event)

            send_message_type_list.append([var.message_to_edit[user_id][-1], '', 'delete_message'])

            text = \
                var.get_reply_text_save_add_data(dictionary_bot, var.show_month_res[user_id]['res']
                [var.show_month_res[user_id]['current_counter']], 'no_allright')

            markup = keyboard.inline_keyboard(
                var.get_buttons_check_events(var.show_month_res[user_id]['current_counter'] + 1,
                                             var.show_month_res[user_id]['count'],
                                             dictionary_bot), None, 3)

            temp_list = [text, markup, 'message_with_text']
            send_message_type_list.append(temp_list)

        elif answer_data == 'edit_event':
            text = var.get_reply_text_save_add_data(dictionary_bot, var.show_month_res[user_id]['res']
            [var.show_month_res[user_id]['current_counter']], 'no_allright')
            markup = ''
            temp_list = [text, markup, 'edit_message_text']
            send_message_type_list.append(temp_list)

            var.enter_mode[user_id] = True
            var.edit_enter_data_mode[user_id] = True

            var.enter_mode_counter[user_id] = 1
            text = dictionary_bot[var.add_enter_mode_text(0)]
            markup = keyboard.reply_keyboard([dictionary_bot['save_current_val'], dictionary_bot['main_menu']], 1,
                                             True, False)

            temp_list = [text, markup, 'message_with_text']
            send_message_type_list.append(temp_list)

    return send_message_type_list


def enter_mode_edit_event_processing(message, dictionary_bot, user_id):
    send_message_type_list = []
    ######################################################################################################
    ######################################################################################################
    # STEP 1 - Ввод короткого описания
    ######################################################################################################
    ######################################################################################################
    if var.enter_mode_counter[user_id] == 1:  # STEP 1
        text = dictionary_bot[var.add_enter_mode_text(var.enter_mode_counter[user_id])]
        markup = keyboard.reply_keyboard([dictionary_bot['save_current_val'], dictionary_bot['main_menu']], 1, True,
                                         False)
        temp_list = [text, markup, 'message_with_text']
        send_message_type_list.append(temp_list)

        if message.text == dictionary_bot['save_current_val']:
            get_name_of_edit_event = \
                var.show_month_res[user_id]['res'][var.show_month_res[user_id]['current_counter']][0]
            var.entered_data[user_id].append(get_name_of_edit_event)
        else:
            var.entered_data[user_id].append(message.text)

        var.enter_mode_counter[user_id] = 2

    ######################################################################################################
    ######################################################################################################
    # STEP 2 - Выбор даты события
    ######################################################################################################
    ######################################################################################################
    elif var.enter_mode_counter[user_id] == 2:  # STEP 2

        text = '👍'
        # markup делается inline клавиатурой в виде календаря
        get_name_of_edit_event = var.show_month_res[user_id]['res'][var.show_month_res[user_id]['current_counter']][
            2]
        markup = keyboard.reply_keyboard([get_name_of_edit_event, dictionary_bot['main_menu']], 1, True, False)

        temp_list = [text, markup, 'message_with_text']
        send_message_type_list.append(temp_list)

        text = dictionary_bot[var.add_enter_mode_text(var.enter_mode_counter[user_id])]
        # markup делается inline клавиатурой в виде календаря
        markup = keyboard.inline_keyboard(calendar_buttons_creating(dictionary_bot, user_id, None, None), None, 7)
        temp_list = [text, markup, 'message_with_text']

        send_message_type_list.append(temp_list)

        var.enter_mode_counter[user_id] = 3

        if message.text == dictionary_bot['save_current_val']:
            get_name_of_edit_event = \
                var.show_month_res[user_id]['res'][var.show_month_res[user_id]['current_counter']][1]
            var.entered_data[user_id].append(get_name_of_edit_event)
        else:
            var.entered_data[user_id].append(message.text)  # эта переменная сохраняет введенные пользователем значения

    ################################################################################################################
    ################################################################################################################
    # STEP 3 - Проверяется введенная дата и в случае успеха изменяется сообщение с календарем(удаляется клавиатура и
    # новая надпись вписывается) и присылается следующее сообщение "выбрать периодичность события"
    ################################################################################################################
    ################################################################################################################
    elif var.enter_mode_counter[user_id] == 3:  # STEP 3
        # check data input format
        if check_datetime_format(str(message.text)):
            send_message_type_list.append([var.message_to_edit[user_id][-1], '', 'delete_message'])
            var.entered_data[user_id].append(message.text)  # эта переменная сохраняет введенные пользователем значения

            text = var.dictionary_bot[user_id]['selected_date_txt'] + str(var.entered_data[user_id][2])
            markup = keyboard.reply_keyboard(dictionary_bot['main_menu'], 1, True, True)

            temp_list = [text, markup, 'message_with_text']
            send_message_type_list.append(temp_list)

            text = var.dictionary_bot[user_id][var.add_enter_mode_text(var.enter_mode_counter[user_id])]
            markup = keyboard.inline_keyboard(var.set_reminder_callback_button(var.dictionary_bot[user_id]), None, 2)
            temp_list = [text, markup, 'message_with_text']
            send_message_type_list.append(temp_list)

            text = var.dictionary_bot[user_id]['selected_date_txt'] + str(var.entered_data[user_id][2])

            temp_list = [text, '', 'edit_message_text', user_id, var.message_to_edit[user_id][-1]]
            send_message_type_list.append(temp_list)
            var.enter_mode_counter[user_id] = 4

        #  if data input is incorrect
        else:
            var.enter_mode_counter[user_id] = 3
            text = dictionary_bot['incorrect_data_format']
            markup = ''
            temp_list = [text, markup, 'reply_message']
            send_message_type_list.append(temp_list)

    ######################################################################################################
    ######################################################################################################
    # STEP 4
    ######################################################################################################
    ######################################################################################################
    elif var.enter_mode_counter[user_id] == 4:  # STEP 4
        print(str(message.text))
        if str(message.text).title() in var.get_set_reminder_callback_button(var.dictionary_bot[user_id]):
            if str(message.text).title() == var.get_set_reminder_callback_button(var.dictionary_bot[user_id])[0]:
                text = dictionary_bot[var.add_enter_mode_text(var.enter_mode_counter[user_id])]
                # markup делается inline клавиатурой в виде календаря
                markup = keyboard.inline_keyboard(var.get_frequency_buttons(dictionary_bot), None, 2)
                temp_list = [text, markup, 'message_with_text']
                send_message_type_list.append(temp_list)

                text = var.dictionary_bot[user_id][var.add_enter_mode_text(var.enter_mode_counter[user_id] - 1)]

                temp_list = [text, '', 'edit_message_text', user_id, var.message_to_edit[user_id][-1]]
                send_message_type_list.append(temp_list)

                var.enter_mode_counter[user_id] = 5

            elif str(message.text).title() == var.get_set_reminder_callback_button(var.dictionary_bot[user_id])[1]:
                text = var.dictionary_bot[user_id][var.add_enter_mode_text(var.enter_mode_counter[user_id] - 1)]
                temp_list = [text, '', 'edit_message_text', user_id, var.message_to_edit[user_id][-1]]
                send_message_type_list.append(temp_list)

                var.entered_data[user_id] += ['0', '0', '0']
                text = var.get_reply_text_save_add_data(var.dictionary_bot[user_id], var.entered_data[user_id],
                                                        'yes_allright')
                markup = keyboard.reply_keyboard(var.get_save_final_buttons(var.dictionary_bot[user_id]), 2, True,
                                                 False)
                temp_list = [text, markup, 'message_with_text']
                send_message_type_list.append(temp_list)

                var.enter_mode_counter[user_id] = 8
        else:
            send_message_type_list.append([var.message_to_edit[user_id][-1], '', 'delete_message'])

            text = dictionary_bot['reply_answer']
            markup = ''
            temp_list = [text, markup, 'reply_message']
            send_message_type_list.append(temp_list)

            text = var.dictionary_bot[user_id][var.add_enter_mode_text(var.enter_mode_counter[user_id] - 1)]
            markup = keyboard.inline_keyboard(var.set_reminder_callback_button(var.dictionary_bot[user_id]), None, 2)
            temp_list = [text, markup, 'message_with_text']
            send_message_type_list.append(temp_list)

    ######################################################################################################
    ######################################################################################################
    # STEP 5 - Проверяется корректность данных периодичности события и предлагается выбор даты напоминания
    # (опять календарь создается)
    ######################################################################################################
    ######################################################################################################
    elif var.enter_mode_counter[user_id] == 5:  # STEP 5
        if str(message.text).lower() in var.get_frequency_buttons_list(var.dictionary_bot[user_id]):

            text = dictionary_bot[var.add_enter_mode_text(var.enter_mode_counter[user_id])]
            # markup делается inline клавиатурой в виде календаря
            markup = keyboard.inline_keyboard(calendar_buttons_creating(dictionary_bot, user_id, None, None), None, 7)
            temp_list = [text, markup, 'message_with_text']
            send_message_type_list.append(temp_list)

            var.entered_data[user_id].append(message.text)  # эта переменная сохраняет введенные пользователем значения

            text = var.dictionary_bot[user_id]['frequency_is_txt'] + str(var.entered_data[user_id][3])

            temp_list = [text, '', 'edit_message_text', user_id, var.message_to_edit[user_id][-1]]
            send_message_type_list.append(temp_list)
            var.enter_mode_counter[user_id] = 6

        else:
            var.enter_mode_counter[user_id] = 5
            text = dictionary_bot['enter_correct_frequency']
            markup = ''
            temp_list = [text, markup, 'reply_message']
            send_message_type_list.append(temp_list)

    ####################################################################################################################
    ####################################################################################################################
    # STEP 6 - Проверется введенная дата напоминания, в случае  успеха изменяется сообщение с календарем(удаляется
    # клавиатура и новая надпись вписывается) и присылается следующее сообщение "Укажите время напоминания в формате..."
    ####################################################################################################################
    ####################################################################################################################
    elif var.enter_mode_counter[user_id] == 6:  # STEP 6
        if check_datetime_format(str(message.text)):
            text = var.dictionary_bot[user_id]['enter_time_of_the_rimender']
            temp_list = [text, '', 'message_with_text']
            send_message_type_list.append(temp_list)

            var.entered_data[user_id].append(message.text)  # эта переменная сохраняет введенные пользователем значения

            text = var.dictionary_bot[user_id]['reminder_date_is_txt'] + str(var.entered_data[user_id][4])

            temp_list = [text, '', 'edit_message_text', user_id, var.message_to_edit[user_id][-1]]
            send_message_type_list.append(temp_list)
            var.enter_mode_counter[user_id] = 7
        else:
            var.enter_mode_counter[user_id] = 6
            text = dictionary_bot['enter_correct_date_reminder']
            markup = ''
            temp_list = [text, markup, 'reply_message']
            send_message_type_list.append(temp_list)

    ##################################################################################################################
    ##################################################################################################################
    # ЗРОБИТИ ОБРОБКУ
    # STEP 7 - Проверется введенное время напоминания и в случе успеха присылается финальная фраза режима ввода данных
    ##################################################################################################################
    ##################################################################################################################
    elif var.enter_mode_counter[user_id] == 7:  # STEP 7
        if check_datetime_format(str(message.text)):
            var.entered_data[user_id].append(message.text)  # эта переменная сохраняет введенные пользователем значения

            text = var.get_reply_text_save_add_data(dictionary_bot, var.entered_data[user_id], 'yes_allright')
            markup = keyboard.reply_keyboard(var.get_save_final_buttons(dictionary_bot), 2, True, False)
            temp_list = [text, markup, 'message_with_text']
            send_message_type_list.append(temp_list)

            var.enter_mode_counter[user_id] = 8
        else:
            var.enter_mode_counter[user_id] = 7
            text = dictionary_bot['enter_correct_time']
            markup = ''
            temp_list = [text, markup, 'reply_message']
            send_message_type_list.append(temp_list)

    else:
        if message.text == dictionary_bot['yes_btn']:
            print('yes')
            text = dictionary_bot['save_event_final_text']
            markup = keyboard.reply_keyboard(var.main_menu_buttons(dictionary_bot), 2, True, False)
            temp_list = [text, markup, 'message_with_text']
            send_message_type_list.append(temp_list)

            event_name = var.show_month_res[user_id]['res'][var.show_month_res[user_id]['current_counter']][0]
            date_event = var.show_month_res[user_id]['res'][var.show_month_res[user_id]['current_counter']][2]

            db.delete_values_from_table(f't{user_id}', 'event', event_name, 'date_of_the_event', date_event)

            db.insert_values_in_table(f"t{user_id}", var.get_user_personal_table_columns(),
                                      f"'{var.entered_data[user_id][0]}', "
                                      f"'{var.entered_data[user_id][1]}', "
                                      f"'{var.entered_data[user_id][2]}', "
                                      f"'{var.entered_data[user_id][3]}', "
                                      f"'{var.entered_data[user_id][4]}', "
                                      f"'{var.entered_data[user_id][5]}'")

            set_default_values_entered_mode(user_id, 'forced_update')

        else:
            set_default_values_entered_mode(user_id, 'forced_update')
            text = dictionary_bot['reply_answer']
            markup = keyboard.reply_keyboard(var.main_menu_buttons(dictionary_bot), 2, True, False)
            temp_list = [text, markup, 'reply_message']
            send_message_type_list.append(temp_list)

    return send_message_type_list
