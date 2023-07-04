from database import sqlite

LEXICON_COMMANDS_RU = {
    "/start": "Привет, {first_name} \U0001F497\n"
    "Добро пожаловать к browws_polina.\nЯ мастер бровист из Краснодара.\U0001F469\n\n"
    "Занимаюсь бровками любой сложности. Всегда слушаю и выполняю любые идеи и мечты клиентов. \U0001F31F "
    "Выполняю свою работу быстро и качественно. Создаю максимально натуральные брови.\n\n"
    "Для новых клиентов действует скидка 10% \U0001F525, обязательно ею воспользуйся)",
    "/help": "xz U+1F917",
}

LEXICON_ANSWER_RU = {
    "geoanswer": "Студия находится по адресу:\n<b>ул. Генерала Трошева 17</b>",        
}

LEXICON_KEYBOARD_RU = {
    "enroll": "Записаться на брови \U0001F917",
    "geomap": "Адрес студии \U0001F5FA",
    "exwork": "Примеры работ \U0001F9D0",
    "price": "Стоимость 💸",
    "contact": "Контакты 📱",
    "sale": "Скидки 😍",
    "information": "Информация",
    "error": "Если в боте произошла ошибка, вы не можете записаться на брови, не понимаете куда нажимать, произвели оплату, а с вами никто не связался, вы всегда можете мне написать - https://t.me/liin_ampolina\n\nЕсли вдруг и я долго не отвечаю, пишите сюда - @zaletelo\n\nP.S.   @zaletelo - создатель этого бота, если вам тоже нужен бот, простой сайт или какая-то программа, можете обращаться😉"    
}

LEXICON_INLINEBUTTON_RU = {
    "url_telegram": "Чат Telegram",
    "url_whatsapp": "Чат WhatsApp",
    "url_instagram": "Мой Instagram",
    "contact_text": "Соц-сети для связи со мной 📲",
    "price_text": "Стоимость💸\n\n"
}

LEXICON_ADMIN = {
    "price_save": "Добавить услугу",
    "price_del": "Удалить услугу",
}

LEXICON_RU = {
    "commands": LEXICON_COMMANDS_RU,
    "answer": LEXICON_ANSWER_RU,
    "keyboard": LEXICON_KEYBOARD_RU,
    "inlinebutton": LEXICON_INLINEBUTTON_RU,
    "admin": LEXICON_ADMIN,
}