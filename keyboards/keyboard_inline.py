from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from datetime import datetime

from lexicon.lexicon import LEXICON_RU
from database import sqlite
from FSM.users import FSMUsersAnEyebrow
from FSM.admin import FSMAdminClientSucsess
from database import models

"""Кнопки ссылок на соц-сети при нажатии на клавиатуру 'контакты'."""

url_telegram: InlineKeyboardButton = InlineKeyboardButton(
    text=LEXICON_RU["inlinebutton"]["url_telegram"],
    url="t.me/@liin_ampolina"
)
url_whatsapp: InlineKeyboardButton = InlineKeyboardButton(
    text=LEXICON_RU["inlinebutton"]["url_whatsapp"],
    url="https://wa.me/79384099727"
)
url_instagram: InlineKeyboardButton = InlineKeyboardButton(
    text=LEXICON_RU["inlinebutton"]["url_instagram"],
    url="https://instagram.com/browws_polina?igshid=YmMyMTA2M2Y="
)

start_keyboard_url_contact: InlineKeyboardBuilder = InlineKeyboardBuilder()
start_keyboard_url_contact.row(
    url_telegram, 
    url_whatsapp, 
    url_instagram,
    width=1
)

start_keyboard_url_inst: InlineKeyboardBuilder = InlineKeyboardBuilder()
start_keyboard_url_inst.row(
    url_instagram,
    width=1
)

keyboard_url_contact = start_keyboard_url_contact.as_markup(
    resize_keyboard=True
)


"""Кнопки администратора."""

# инлайн кнопки выбора что хочет сделать администартор
def admin_send_move():

    admin_send_move: InlineKeyboardBuilder = InlineKeyboardBuilder()

    price_save: InlineKeyboardButton = InlineKeyboardButton(
        text=LEXICON_RU['admin']['price_save'],
        callback_data="price_save"
    )
    price_del: InlineKeyboardButton = InlineKeyboardButton(
        text=LEXICON_RU['admin']['price_del'],
        callback_data="price_del"
    )

    time_save: InlineKeyboardButton = InlineKeyboardButton(
        text="Добавить время работы",
        callback_data="time_save"
    )
    time_del: InlineKeyboardButton = InlineKeyboardButton(
        text="Удалить дату работы",
        callback_data="time_del"
    )

    sale_save: InlineKeyboardButton = InlineKeyboardButton(
        text="Добавить в раздел скидки любой текст",
        callback_data="sale_save"
    )
    sale_del: InlineKeyboardButton = InlineKeyboardButton(
        text="Удалить весь текст в разделе 'скидки'",
        callback_data="sale_del"
    )


    admin_send_move.row(
        price_save, price_del,
        time_save, time_del,
        sale_save, sale_del,
        width=2
    )

    return admin_send_move

# Инлайн кнопки дат, перед удалением через админку
def date_del_keyboard():
    all_date_time = models.get_date_time()

    date_del_keyboard = InlineKeyboardBuilder()
    if all_date_time:
        for date in all_date_time:
            button = InlineKeyboardButton(text=f"{date.weekday}", callback_data=f"{date.weekday}")
            date_del_keyboard.row(button)
    return date_del_keyboard

# Инлайн кнопи с услугами перед удалением
def price_del_keyboard():
    all_price = models.get_prices()

    price_del_keyboard: InlineKeyboardBuilder = InlineKeyboardBuilder()
    if all_price:
        for price in all_price:
            button: InlineKeyboardButton = InlineKeyboardButton(text=f"{price.service}", callback_data=f"{price.service}")
            price_del_keyboard.row(button)
    return price_del_keyboard            


# Кнопка назад
def get_back_button(state):
    keyboard = InlineKeyboardBuilder()
    callback_data = f"back:{state}"
    button_back = InlineKeyboardButton(text="назад", callback_data=callback_data)
    return button_back


# Кнопка с услугами и ценами
def keyboard_user_price():
    prices = models.get_prices()
    keyboard_user_price = InlineKeyboardBuilder()    
    buttons = [
        InlineKeyboardButton(text=f"{row.service} - {row.price} рублей", callback_data=f"price:{row.service}:{row.price}")
        for row in prices
    ]
    keyboard_user_price.row(*buttons, width=1)
    return keyboard_user_price

# Кнопки с датами
def date_keyboard():
    all_date_time = models.get_date_time()
    date_keyboard = InlineKeyboardBuilder()
    back_keyboard = get_back_button(FSMUsersAnEyebrow.service)
    if all_date_time:
        for date in all_date_time:
            button = InlineKeyboardButton(text=datetime.strptime(date.weekday, '%d-%m-%Y').strftime('%d-%m-%Y'), callback_data=f"{date.weekday}")
            date_keyboard.row(button)
        date_keyboard.row(back_keyboard)    
        return date_keyboard    

# Кнопки с временем 
def time_keyboard(db_time, date_):
    time_keyboard = InlineKeyboardBuilder()
    back_keyboard = get_back_button(FSMUsersAnEyebrow.date)
    
    if db_time is None or len(db_time) == 0:
        button = InlineKeyboardButton(text="Нет свободного времени", callback_data=f"not_time")
        time_keyboard.row(button, width=1)
        time_keyboard.row(back_keyboard)
    else:
        for time in db_time:
            button = InlineKeyboardButton(text=datetime.strptime(time, '%H:%M').strftime('%H:%M'), callback_data=f"{date_},{time}")
            time_keyboard.row(button, width=2)
        
        time_keyboard.row(back_keyboard)
    
    return time_keyboard   

# Кнопка подтверждения записи
def sucsess_keyboard():
    sucsess_keyboard = InlineKeyboardBuilder()
    #back_keyboard = get_back_button(FSMUsersAnEyebrow.time)
    button_yes = InlineKeyboardButton(text="Да, подтверждаю запись", callback_data="suc_yes")
    button_no = InlineKeyboardButton(text="Нет, предумал/а", callback_data="suc_no")
    sucsess_keyboard.row(button_yes, button_no, width=2)
    #sucsess_keyboard.row(back_keyboard)
    return sucsess_keyboard

# Кнопка подтверждения jgkfns
def pay_keyboard():
    pay_keyboard = InlineKeyboardBuilder()
    button_yes = InlineKeyboardButton(text="Оплатил/а", callback_data="pay_yes")
    button_no = InlineKeyboardButton(text="Передумал/а", callback_data="pay_no")
    pay_keyboard.row(button_yes, button_no, width=2)
    return pay_keyboard

# Кнопка записаться на брови
def keyboard_price_enwork():
    keyboard_price_enwork = InlineKeyboardBuilder()
    button_enwork = InlineKeyboardButton(text="Записаться на бровки", callback_data="enwork_brows")
    keyboard_price_enwork.row(button_enwork)
    return keyboard_price_enwork


def client_sucsess():
    client_user_id = models.get_enwork_client()
    client_sucsess = InlineKeyboardBuilder()
    if client_user_id:
        for client in client_user_id:
            button = InlineKeyboardButton(text=f"Клиент - {client.client_user_id} - {client.client_name}", callback_data=f"{client.client_user_id}")
            client_sucsess.row(button)   
        return client_sucsess

def client_del_or_pay(client_user_id):
    client_user_id = models.client_user_id(client_user_id)
    client_del_or_pay = InlineKeyboardBuilder()
    if client_user_id:
        button_unsucsess = InlineKeyboardButton(text="Удалить клиента из базы", callback_data="client_unsuc")
        client_del_or_pay.row(button_unsucsess, width=1)
    else:
        print('NO')
    return client_del_or_pay