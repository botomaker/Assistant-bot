import PythonFiles.variables as var


def set_language(language):
    if language == 'UA':
        return dictionary_UA
    if language == 'EN':
        return dictionary_EN


dictionary_UA = {
    'start_message': f"Привіт!{var.hello_hand_smile}\nЯ Assistant Bot{var.mechanic_hand_smile}, твій особистий помічник"
                     f"{var.man_with_laptop_smile}{var.man_hanging_hand_smile}{var.blind_smile}\n\n"
                     f"Я допомагатиму тобі пам'ятати всі дні народження та кожен важливий день. Також можемо разом "
                     f"контролювати фінанси.{var.money_smile}",
    'main_menu': f"{var.main_menu_smile} Головне меню",
    'events_button': f"{var.events_smile} Події",
    'settings_button': f"{var.settings_gear_smile} Налаштування",
    'aboutbot_button': f"{var.about_bot_smile} Про бота",
    'aboutbot_text': "Бот розроблений для допомоги ведення власних справ.\nПитання, побажання, "
                     "пропозиції надсилайте @botomakerr.",
    'back_button': f"{var.back_button_smile} Назад",
    'reply_answer': f"Нічого не понятно, але очєнь інтєрєсно{var.facepalm_man_smile}",
    'notification_button': f"{var.reminder_button_smile} Встановити сповіщення",
    'change_language_button': f"{var.change_lang_smile} Змінити мову",
    'current_language_message': f"Наразі у вас встановлено українську мову {var.ukraine_flag_smile}",
    'you_choose_language_msg': f"Ви вибрали українську мову! {var.ukraine_flag_smile}",
    'show_events': f"{var.show_events_smile} Переглянути події",
    'add_event': f"{var.add_event_smile} Додати подію",
    'edit_event': f"{var.edit_event_smile} Редагувати подію",
    'remove_event': f"{var.del_event_smile} Видалити подію",
    'edit_event_short': f"{var.edit_event_smile} Редагувати",
    'remove_event_short': f"{var.del_event_smile} Видалити",
    'enter_name_of_the_event': "Введіть назву події:",
    'enter_description_of_the_event': "Введіть короткий опис події:",
    'choose_date_of_the_event': "Оберіть дату події, або введіть її вручну у форматі день.місяць.рік, наприклад, "
                                "24.08.1991:",
    'month': {1: 'Січень', 2: 'Лютий', 3: 'Березень', 4: 'Квітень', 5: 'Травень', 6: 'Червень', 7: 'Липень',
              8: 'Серпень', 9: 'Вересень', 10: 'Жовтень', 11: 'Листопад', 12: 'Грудень'},
    'save_data_event': 'Так виглядає внесена подія:',
    'save_data_name': 'Назва: ',
    'save_data_des': 'Опис: ',
    'save_data_date': 'Дата: ',
    'reminder_date_is_txt': 'Дата повідомлення: ',
    'all_right?': 'Все правильно?',
    'yes_btn': 'Так',
    'incorrect_data_format': 'Некоректний формат дати, спробуйте ще раз',
    'save_event_final_text': 'Подія збережена!',
    'something_happened': 'Щось сталося, можливо бот заснув, спробуйте перезапустити! /restart',
    'select_the_frequency_of_the_event': 'Оберіть періодичність події:',
    'monthly_event': 'щомісячна',
    'yearly_event': 'щорічна',
    'weekly_event': 'кожної неділі',
    'daily_event': 'щоднева',
    'one_time_event': 'одноразова',
    'selected_date_txt': 'Обрана дата: ',
    'frequency_is_txt': 'Вказана періодичність: ',
    'set_date_of_the_reminder': "Вкажіть дату нагадування про подію, або введіть її вручну у форматі день.місяць.рік, "
                                "наприклад, 01.12.2025:",
    'enter_time_of_the_rimender': 'Введіть час сповіщення у форматі година:хвилина, наприклад, 14:45:',
    'enter_correct_frequency': 'Введіть коректну періодичність, або натисніть кнопку з попереднього повідомлення',
    'enter_correct_time': 'Введіть час коректно',
    'date_of_remind': 'Дата сповіщення: ',
    'time_of_remind': 'Час сповіщення: ',
    'enter_correct_date_reminder': 'Введіть коректну дату нагадування:',
    'set_reminder_text_add': 'Встановити нагадування?\nВи можете пропустити цей крок і в будь-який час редагувати '
                             'нагадування',
    'set_reminder_inline_btn': 'Встановити',
    'later_reminder_inline_btn': 'Пізніше',
    'show_month_events_txt1': 'В цьому місяці подій:',
    'show_month_events_txt2': '\nЩоб переглянути всі події в поточному місяці натисніть '
                       'кнопку <strong>«Показати події»</strong>. \n\nНатисніть кнопку <strong>«Календар»</strong>, '
                              'щоб відобразити календар, дні з подіями будуть відмічені 📌\n\nЩоб знайти подію за '
                              'назвою або датою, ввівши її вручну, натисніть кнопку <strong>"Пошук"</strong>.',
    'calendar_btn': 'Календар',
    'show_events_btn': 'Показати події',
    'search_btn': 'Пошук',
    'reminder_not_insert': 'Сповіщення не внесено',
    'events_for_month': 'Події за ',
    'remove_event_txt': 'Ви впевнені, що хочете видалити цю подію?',
    'no_btn': 'Ні',
    'save_current_val': 'Лишити поточне значення',
    'choose_date_of_the_event_short': 'Оберіть дату події:'

}

dictionary_EN = {
    'start_message': f"Hi there!{var.hello_hand_smile}\nI am Assistant Bot{var.mechanic_hand_smile}, your personal "
                     f"assistant{var.man_with_laptop_smile}{var.man_hanging_hand_smile}{var.blind_smile}\n\n",
    'main_menu': f"{var.main_menu_smile} Main menu",
    'events_button': f"{var.events_smile} Events",
    'settings_button': f"{var.settings_gear_smile} Settings",
    'aboutbot_button': f"{var.about_bot_smile} About",
    'aboutbot_text': "The bot is designed to supplement one's own foreign language vocabulary.\nSend questions and "
                     "suggestions to @botomakerr.",
    'back_button': f"{var.back_button_smile} Back",
    'reply_answer': f"Nothing is clear, but very interesting{var.facepalm_man_smile}",
    'notification_button': f"{var.reminder_button_smile} Set notification",
    'change_language_button': f"{var.change_lang_smile} Change language",
    'current_language_message': f"You currently have the English language set {var.english_flag_smile}",
    'you_choose_language_msg': f"You have chosen the English language! {var.english_flag_smile}",
    'show_events': f"{var.show_events_smile} Show events",
    'add_event': f"{var.add_event_smile} Add events",
    'edit_event': f"{var.edit_event_smile} Edit event",
    'remove_event': f"{var.del_event_smile} Remove event",
    'enter_name_of_the_event': "Enter the name of the event:",
    'enter_description_of_the_event': "Enter short description of the event:",
    'choose_date_of_the_event': "Сhoose the date of the event, or enter it manually in the format day.month.year, "
                                "for example 24.08.1991:",
    'month': {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July',
              8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'},
    'save_data_event': 'This is what the saved event looks like:',
    'save_data_name': 'Name: ',
    'save_data_des': 'Description: ',
    'save_data_date': 'Date: ',
    'all_right?': 'All right?',
    'yes_btn': 'Yes',
    'incorrect_data_format': 'Incorrect date format, please try again',
    'save_event_final_text': 'Event saved!',
    'something_happened': 'Something happened, maybe the bot fell asleep, try restarting! /restart',
    'select_the_frequency_of_the_event': 'Select the frequency of the event:',
    'monthly_event': 'monthly',
    'yearly_event': 'yearly',
    'weekly_event': 'weekly',
    'daily_event': 'daily',
    'one_time_event': 'one time',
    'selected_date_txt': 'Date is: ',
    'frequency_is_txt': 'Frequency is: ',
    'set_date_of_the_reminder': "Set the date of the reminder, or enter it manually in the format day.month.year, "
                                "for example 12.10.2031:",
    'enter_time_of_the_rimender': 'Enter time of the reminder in the format hour:minute, for example, 14:45:',
    'enter_correct_frequency': 'Enter correct frequency or click button upon',
    'reminder_date_is_txt': 'Date of the remind is: ',
    'enter_correct_time': 'Enter the time correctly',
    'enter_correct_date_reminder': 'Enter correct date of the reminder:',
    'date_of_remind': 'Data of the reminder: ',
    'time_of_remind': 'Time of the reminder: ',
    'set_reminder_text_add': 'Set reminder?\nYou can skip this step and edit it at any time',
    'set_reminder_inline_btn': 'Set',
    'later_reminder_inline_btn': 'Later',
    'show_month_events_txt1': 'This month events: ',
    'show_month_events_txt2': '\n\nTo view all events in the current month, click <strong>"Show events"</strong> '
                              'button. \nOr click the <strong>"Calendar"</strong> button to display the calendar, days '
                              'with events will be marked 📌 \n\nPress the <strong>"Search"</strong> button to enter '
                              'the name or date of the event manually.',
    'calendar_btn': 'Calendar',
    'show_events_btn': 'Show events',
    'search_btn': 'Search',

}
