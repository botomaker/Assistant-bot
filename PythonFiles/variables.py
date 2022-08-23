dictionary_bot = dict()  # словарь для языка бота
language_var = dict()  # Переменная для языка, принимает значение языка которое достается из таблицы БД
enter_mode = dict()  # Переменная для определения режима ввода, принимает значение True/False
entered_data = dict()  # Переменная хранит в себе введенные данные в виде списка
enter_mode_counter = dict()  # Переменная хранит шаг ввода данных
calendar_current_date = dict()  # Переменная
message_to_edit = dict()
show_month_res = dict()
edit_enter_data_mode = dict()  # переменная для ввода данных для события которое нужно изменить


# smiles
check_mark_smile = u'\U00002705'
settings_gear_smile = u'\U00002699'
ukraine_flag_smile = '🇺🇦'
english_flag_smile = '🇬🇧'
events_smile = '📅'
about_bot_smile = '🙋‍♂️'
main_menu_smile = '🏠'
show_events_smile = '🔎'
add_event_smile = '📝'
edit_event_smile = '✏️'
del_event_smile = '❌'
back_button_smile = '🔙'
reminder_button_smile = '🔔'
change_lang_smile = '🗣'
mechanic_hand_smile = '🦾'
hello_hand_smile = '✌️'
man_with_laptop_smile = '👨‍💻'
man_hanging_hand_smile = '🙋‍♂️'
facepalm_man_smile = '🤦‍♂️'
blind_smile = '⚡️'
tornado_smile = '🌪'
money_smile = '💸'
notes_smile = '📋'

'''
###################################################################
###################################################################
###################################################################
BUTTONS ###########################################################
###################################################################
###################################################################
###################################################################
'''


# Кнопки главного меню
def main_menu_buttons(dict_bot):
    return dict_bot['events_button'], (dict_bot['settings_button'], dict_bot['aboutbot_button'])


# Кнопики меню настроек
def settings_menu_buttons(dict_bot):
    return (dict_bot['notification_button'], dict_bot['change_language_button']), dict_bot['back_button']


# Кнопки меню событий
def events_menu_buttons(dict_bot):
    return dict_bot['show_events'], (dict_bot['add_event'], dict_bot['edit_event'], dict_bot['remove_event']), dict_bot[
        'main_menu']


# Кнопки "Сохранить" и "Главное меню", когда ввдено событие
def get_save_final_buttons(dictionary):
    return [(dictionary['yes_btn'], dictionary['main_menu'])]


def get_menu_buttons_list(dictionary):
    return dictionary['aboutbot_button'], dictionary['back_button'], dictionary['settings_button'], \
           dictionary['change_language_button'], dictionary['main_menu'], dictionary['events_button'], \
           dictionary['add_event'], dictionary['show_events']


def get_frequency_buttons_list(dict_bot):
    return dict_bot['yearly_event'], dict_bot['monthly_event'], dict_bot['weekly_event'], dict_bot['daily_event'], \
           dict_bot['one_time_event']


def get_set_reminder_callback_button(dict_bot):
    return dict_bot['set_reminder_inline_btn'], dict_bot['later_reminder_inline_btn']


'''
###################################################################
###################################################################
###################################################################
MESSAGE HANDLER####################################################
###################################################################
###################################################################
###################################################################
'''


#  enter mode text steps
def add_enter_mode_text(counter):
    dictionary = {0: "enter_name_of_the_event", 1: "enter_description_of_the_event", 2: "choose_date_of_the_event",
                  3: "set_reminder_text_add", 4: "select_the_frequency_of_the_event", 5: 'set_date_of_the_reminder',
                  6: 'enter_time_of_the_rimender', 7: "save_data_event"}
    return dictionary[counter]


def get_reply_text_save_add_data(dictionary, enter_data, all_right):
    if enter_data[-1] != '0':
        text = f"<i>{dictionary['save_data_name']}</i>{enter_data[0]}\n" \
               f"<i>{dictionary['save_data_des']}</i>{enter_data[1]}\n<i>{dictionary['save_data_date']}</i>" \
               f"{enter_data[2]}\n<i>{dictionary['frequency_is_txt']}</i>{enter_data[3]}\n<i>" \
               f"{dictionary['date_of_remind']}</i>{enter_data[4]}\n<i>{dictionary['time_of_remind']}</i>" \
               f"{enter_data[5]}"
    else:
        text = f"<i>{dictionary['save_data_name']}</i>{enter_data[0]}\n" \
               f"<i>{dictionary['save_data_des']}</i>{enter_data[1]}\n<i>{dictionary['save_data_date']}</i>" \
               f"{enter_data[2]}"
        if all_right != 'yes_allright':
            text += f"\n{dictionary['reminder_not_insert']}"

    if all_right == 'yes_allright':
        text = f"<b>{dictionary['save_data_event']}</b>\n{text}"
        text += f"\n\n{dictionary['all_right?']}"

    return text


'''
###################################################################
###################################################################
###################################################################
CALLBACK HANDLER###################################################
###################################################################
###################################################################
###################################################################
'''


# кнопки для переключения просмотра событий
def get_buttons_check_events_list():
    return ['prev_event', 'next_event', 'edit_event', 'remove_event', 'yes_remove', 'no_remove']


# Список кнопок в меню просмотра событий
def get_show_event_inline_button_list():
    return ['calendar_btn', 'search_btn']


# Список кнопок для установки оповещения
def get_set_reminder_callback():
    return ['set_reminder_inline_btn', 'later_reminder_inline_btn']


# Список кнопок для установки периодичности
def get_frequency_callback():
    return ['yearly_event', 'monthly_event', 'weekly_event', 'daily_event', 'one_time_event']


#  get callback answer of calendar buttons for inline keyboard
# Список кнопок календраря
def get_calendar_callback_button():
    callback_button = ['year_month', 'prev_month', 'next_month']
    callback_button += [f" {str(x)}" for x in range(1, 32)]
    return callback_button


# инлайн кнопки установки оповещения
def set_reminder_callback_button(dict_bot):
    return [((dict_bot['set_reminder_inline_btn'], 'set_reminder_inline_btn'), (dict_bot['later_reminder_inline_btn'],
                                                                                'later_reminder_inline_btn'))]


#  get and set languages buttons
#  инлайн конпки вібора языка
def languages_callback_button(dict_bot, language):
    if language == 'UA':
        return ((f'Українська {check_mark_smile}', 'UA'), ('English', 'EN')), [dict_bot['main_menu'], 'main_menu']
    elif language == 'EN':
        return (('Українська', 'UA'), (f'English {check_mark_smile}', 'EN')), [dict_bot['main_menu'], 'main_menu']

    # return (('Українська', 'UA'), ('English', 'EN')), ['sa', 's'] works with single button
    # return [((f'Українська {smile}', 'UA'), ('English', 'EN'))]  # works only with tuple


#  инлайн кнопки выбора периодичности
def get_frequency_buttons(dict_bot):
    return [((dict_bot['yearly_event'], 'yearly_event'), (dict_bot['monthly_event'], 'monthly_event'),
             (dict_bot['weekly_event'], 'weekly_event'), (dict_bot['daily_event'], 'daily_event'),
             (dict_bot['one_time_event'], 'one_time_event'))]


def get_show_events_inline_buttons(dict_bot):
    return [((dict_bot['calendar_btn'], 'calendar_btn'), (dict_bot['search_btn'], 'search_btn'))]


# кнопки для переключения просмотра событий
def get_buttons_check_events(number, count, dictionary):
    return [(('<', 'prev_event'), (f"{number}/{count}", ' '), ('>', 'next_event'), (dictionary['edit_event_short'],
            'edit_event'), (dictionary['remove_event_short'], 'remove_event'))]


'''
###################################################################
###################################################################
###################################################################
DICTIONARY ########################################################
###################################################################
###################################################################
###################################################################
'''


'''
    #########           #########     
    ###     ###         ###     ###
    ###      ###        ###      ###
    ###      ###        ###      ###
    ###      ###        ###    ###
    ###      ###        ###     ###
    ###     ###         ###      ###
    #########           ###########
'''


def get_users_table_create_columns():
    return '''
        digit_id INTEGER NOT NULL,
        telegram_id VARCHAR(255) NOT NULL,
        first_name VARCHAR(255) NOT NULL,
        surname VARCHAR(255) NOT NULL,
        language VARCHAR(255) NOT NULL
    '''


def get_user_personal_create_table_columns():
    return '''
        event VARCHAR(255) NOT NULL,
        description VARCHAR(255) NOT NULL,
        date_of_the_event VARCHAR(255) NOT NULL,
        frequency VARCHAR(255) NOT NULL,
        date_of_the_remind VARCHAR(255) NOT NULL,
        time_of_the_remind VARCHAR(255) NOT NULL
    '''


def get_user_table_columns():
    return 'digit_id, telegram_id, first_name, surname, language'


def get_user_personal_table_columns():
    return 'event, description, date_of_the_event, frequency, date_of_the_remind, time_of_the_remind'
