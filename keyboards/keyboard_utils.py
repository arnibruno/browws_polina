from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from lexicon.lexicon import LEXICON_RU


button_enroll: KeyboardButton = KeyboardButton(
    text=LEXICON_RU["keyboard"]['enroll']
)
button_geomap: KeyboardButton = KeyboardButton(
    text=LEXICON_RU["keyboard"]['geomap']
)
button_exwork: KeyboardButton = KeyboardButton(
    text=LEXICON_RU["keyboard"]['exwork']
)
button_price: KeyboardButton = KeyboardButton(
    text=LEXICON_RU["keyboard"]['price']
)
button_contact: KeyboardButton = KeyboardButton(
    text=LEXICON_RU["keyboard"]['contact']
)
button_sale: KeyboardButton = KeyboardButton(
    text=LEXICON_RU["keyboard"]['sale']
)
button_erorr: KeyboardButton = KeyboardButton(
    text="Произошла ошибка☹️"
)

start_geoex_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
start_geoex_builder.row(
    button_geomap, button_exwork,
    button_price, button_contact,
    button_sale, button_erorr,
    button_enroll,
    width=2
)

start_geoex = start_geoex_builder.as_markup(
    resize_keyboard=True
)