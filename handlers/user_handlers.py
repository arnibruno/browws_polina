import datetime
from aiogram import types, Bot
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import Router, F
from aiogram.filters import Text, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ContentType
from aiogram.fsm.state import default_state
from datetime import datetime
from bot import main
from aiogram.types import ContentType

from keyboards.keyboard_utils import start_geoex
from keyboards.keyboard_inline import keyboard_url_contact
from config_data.config import load_config
from keyboards import keyboard_inline
from lexicon.lexicon import LEXICON_RU
from database import sqlite, models
from FSM.users import FSMUsersAnEyebrow

config = load_config(".env")
bot = Bot(token=config.tg_bot.token)

router: Router = Router()


@router.message(Command(commands=["start"]))
async def process_start_handler(message: Message) -> None:
    models.add_user(message.from_user.username, message.from_user.id)
    
    try:
        await message.answer(
            text=(LEXICON_RU["commands"]["/start"].format(first_name=message.from_user.first_name)),
            reply_markup=start_geoex
        )    
    except Exception:
        await message.answer(
            text=(LEXICON_RU["commands"]["/start"].format(first_name="Красотка")),
            reply_markup=start_geoex
        )     

@router.message(Command(commands=["/help"]))
async def text_handler(message: Message) -> None:
    await message.answer(
        text=(LEXICON_RU["commands"]["/help"]),
        reply_markup=start_geoex
    )   

@router.message(Text(text=LEXICON_RU["keyboard"]["geomap"]))
async def process_geomap(message: Message):
    await message.answer(
        text=(LEXICON_RU["answer"]["geoanswer"])
    )
    await message.answer_location(45.055902, 39.042300)

@router.message(Text(text=LEXICON_RU["keyboard"]["exwork"]))
async def process_exwork(message: Message):
    await message.answer(text="Свои работы я выкладываю в инстаграмм, также там вы можете найти много интересного 🥰",
    reply_markup=keyboard_inline.start_keyboard_url_inst.as_markup())

@router.message(Text(text=LEXICON_RU["keyboard"]["contact"]))
async def process_contact(message: Message):
    await message.answer(
        text=LEXICON_RU["inlinebutton"]["contact_text"],
        reply_markup=keyboard_url_contact
    )

@router.message(Text(text=LEXICON_RU["keyboard"]["price"]))
async def process_price(message: Message):
    prices = models.get_prices()
    if not prices:
        await message.answer(text="нет услуг")
    else:
        text = f"{LEXICON_RU['inlinebutton']['price_text']}"
        for row in prices:
            text += f"✨{row.service} - {row.price} рублей\n\n"

        keyboard_price_enwork = keyboard_inline.keyboard_price_enwork()

        await message.answer(
            text=text,
            reply_markup=keyboard_price_enwork.as_markup()
        )

@router.message(Text(text=LEXICON_RU["keyboard"]["sale"]))
async def process_sale(message: Message):
    sale = models.get_sale()
    
    if not sale:
        await message.answer(text="На данный момент скидок нет 😟")
    text = ""
    for row in sale:
        text += f"{row.text}"

    await message.answer(
        text=text
    )    

@router.message(Text(text="Произошла ошибка☹️"))
async def process_error(message: Message):  
    await message.answer(
        text=LEXICON_RU["keyboard"]["error"]
    ) 

# Этот хэндлер будет срабатывать на команду "/cancel" в любых состояниях,
# кроме состояния по умолчанию, и отключать машину состояний
@router.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(text='Вы прервали запись на брови\n\n'
                              'Чтобы снова перейти к записи - '
                              'нажмите на кнопку "записаться на бровки"')
    # Сбрасываем состояние
    await state.clear()


# Этот хэндлер будет срабатывать на команду "/cancel" в состоянии
# по умолчанию и сообщать, что эта команда доступна в машине состояний
@router.message(Command(commands='cancel'), StateFilter(default_state))
async def process_cancel_command(message: Message):
    await message.answer(text='Отменять нечего. Вы не записываетесь на брови\n\n'
                              'Чтобы перейти начать запись - '
                              'нажмите на кнопку "записаться на бровки"')


# Хэндлер обработки инлайн кнопки "Записаться на бровки". Запускает FSM
@router.callback_query(Text(text='enwork_brows'), StateFilter(default_state))
async def process_enroll_name_bytton(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer(text="Пожалуйста введите ваше имя\n\n\n<i>Если передумали, введите команду</i>\n/cancel")
    await state.set_state(FSMUsersAnEyebrow.name)                                  

# Хэндлер обработки обычной кнопки "Записаться на бровки". Запускает FSM
@router.message(Text(text=LEXICON_RU["keyboard"]["enroll"]), StateFilter(default_state))
async def process_enroll_command(message: Message, state: FSMContext):
    await message.answer(text="🤍Пожалуйста введите ваше имя🤍\n\n\n<i>Если передумали, введите команду</i>\n/cancel")
    await state.set_state(FSMUsersAnEyebrow.name)

# Хэндлер срабатывает после ввода имени, и просит выбрать услугу
@router.message(StateFilter(FSMUsersAnEyebrow.name), F.text.isalpha())
async def process_enroll_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)

    user_id = message.from_user.id
    await state.update_data(user_id=user_id)

    await state.set_state(FSMUsersAnEyebrow.service)

    keyboard_user_price = keyboard_inline.keyboard_user_price()

    await message.answer(
        text="🤍Спасибо, а теперь выберите услугу на которую хотите записаться\n\n\n<i>Если передумали, введите команду\n</i>/cancel",
        reply_markup=keyboard_user_price.as_markup()
    )

# Хэндлер срабатывает на ввод имени в котором есть что-то крому букв
@router.message(StateFilter(FSMUsersAnEyebrow.name))
async def warning_not_name(message: Message):
    await message.answer(text='🤍То, что вы отправили не похоже на имя\n\n'
                              'Пожалуйста, введите ваше имя\n\n'
                              '<i>Если вы хотите прервать заполнение анкеты - '
                              'отправьте команду</i>/cancel')

# Хэндлер срабатывает после выбора услуги и просит выбрать дату записи
@router.callback_query(StateFilter(FSMUsersAnEyebrow.service))
async def process_service_date(callback: CallbackQuery, state: FSMContext):
    try:
        _, service, price = callback.data.split(':')
        await state.update_data(service=service)
        await state.update_data(price=price)
        data = await state.get_data()
        await state.set_state(FSMUsersAnEyebrow.date)
        
        date_keyboard = keyboard_inline.date_keyboard()

        await callback.message.edit_text(f'🟢Вы выбрали услугу:\n✨{data.get("service")}\n\n🤍Выберите дату для записи:\n\n\n<i>Если передумали, введите команду\n</i>/cancel', reply_markup=date_keyboard.as_markup())
    except Exception as error:
        print(f"Ошибка ---- {error}")
        await callback.message.edit_text(text="К сожалению свободных дат на запись нет.")
        await state.clear()                                 

# Хэндлер срабатывает после выбора даты и просит выбрать время записи
@router.callback_query(StateFilter(FSMUsersAnEyebrow.date))
async def process_date_time(callback: CallbackQuery, state: FSMContext):
    if callback.data == f"back:{FSMUsersAnEyebrow.service}":
        keyboard_user_price = keyboard_inline.keyboard_user_price()    
        await state.set_state(FSMUsersAnEyebrow.service)
        await callback.message.edit_text(text="🤍Спасибо, а теперь выберите услугу на которую хотите записаться\n\n\n<i>Если передумали, введите команду\n</i>/cancel",
                                        reply_markup=keyboard_user_price.as_markup())
        return                  
    date_ = callback.data

    await state.update_data(date=date_)
    data = await state.get_data()
    await state.set_state(FSMUsersAnEyebrow.time)
    db_time = models.date_to_time(date_)

    time_keyboard = keyboard_inline.time_keyboard(db_time, data.get("date"))   

    await callback.message.edit_text(
        text=f'🟢Вы выбрали услугу:\n✨{data.get("service")}\n\n🟢На дату:\n✨{data.get("date")}\n\n🤍Выберите на какое время вас записать:\n\n\n<i>Если передумали, введите команду\n</i>/cancel',
        reply_markup=time_keyboard.as_markup()
    )
        

# Хэндлер срабатывает после имени, услуги, даты, времени, просит подтвердить запись
@router.callback_query(StateFilter(FSMUsersAnEyebrow.time))
async def process_enroll_sucsess(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    if callback.data == f"back:{FSMUsersAnEyebrow.date}":
        date_keyboard = keyboard_inline.date_keyboard()    
        await state.set_state(FSMUsersAnEyebrow.date)
        await callback.message.edit_text(f'🟢Вы выбрали услугу:\n✨{data.get("service")}.\n\n🤍Выберите дату для записи:\n\n\n<i>Если передумали, введите команду\n</i>/cancel',
                                        reply_markup=date_keyboard.as_markup())
        return

    _, time_ = callback.data.split(',')
    await state.update_data(time=time_)
    data = await state.get_data()
    await state.set_state(FSMUsersAnEyebrow.payments)

    sucsess_keyboard = keyboard_inline.sucsess_keyboard() 

    await callback.message.edit_text(
        text=f'✨Имя:\n<b>{data.get("name")}</b>\n\n✨Услуга:\n<b>{data.get("service")}</b>\n\n✨Дата:\n<b>{data.get("date")}</b>\n\n✨Время:\n<b>{data.get("time")}</b>\n\n✨Цена услуг:\n<b>{data.get("price")} рублей</b>\n\n',
        reply_markup=sucsess_keyboard.as_markup()
    )

# Хэндлер срабатывает на подтверждение или отказ от оплаты 
@router.callback_query(StateFilter(FSMUsersAnEyebrow.payments))
async def process_enroll_sucsess_pay(callback: CallbackQuery, state: FSMContext):
    pay_keyboard = keyboard_inline.pay_keyboard()

    if callback.data == "suc_yes":
        await callback.message.edit_text(text=f'🤍Чтобы подтвердить вашу запись и обеспечить вам гарантированное время, нужно внести предоплату <b>в размере 200 рублей</b>\n\n\n🏦<i>Сбербанк</i>🏦\n\n💎<b>Телефон</b> +7(938)409-97-27\n💎<b>Номер карты</b>  5469980420521334', reply_markup=pay_keyboard.as_markup())
        await state.set_state(FSMUsersAnEyebrow.sucsess)
    else:
        await callback.message.edit_text(text="Очень жаль, но если вы хотите записаться снова, то я всегда буду вам рада🥰")
        await state.clear()

# Хэндлер срабатывает на подтверждение или отказ от записи  
@router.callback_query(StateFilter(FSMUsersAnEyebrow.sucsess))
async def process_enroll_sucsess_yes(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    if callback.data == "pay_yes":
        models.enwork_client_add(name=data.get('name'), service=data.get('service'), client_user_id=data.get('user_id'), price=data.get('price'), date=data.get('date'), time=data.get('time'))
        await bot.send_message(chat_id=-1001544172966, text=f'Клиент перед оплатой:\n\nИмя:\n{data.get("name")}\n\nУслуга:\n{data.get("service")}\n\nДата:\n{data.get("date")}\n\nВремя:\n{data.get("time")}\n\nЦена услуг:\n{data.get("price")} рублей\n\n\ntg://user?id={data.get("user_id")}')
        await state.set_state(FSMUsersAnEyebrow.payments)
        await callback.message.edit_text(text=f'Отлично, тогда я вас жду\nВот информация:\n\n✨Имя:\n<b>{data.get("name")}</b>\n\n✨Услуга:\n<b>{data.get("service")}</b>\n\n✨Дата:\n<b>{data.get("date")}</b>\n\n✨Время:\n<b>{data.get("time")}</b>\n\n✨Цена услуг:\n<b>{data.get("price")} рублей</b>\n\n✨Адрес:\n<b>ул. Генерала Трошего 17</b>\n\n\nP.S.\n<i>Если остались вопросы, пишите - </i>@liin_ampolina')
        await state.clear()
    else:
        await state.clear()
        await callback.message.edit_text(text="Очень жаль, но если вы хотите записаться снова, то я всегда буду вам рада🥰")