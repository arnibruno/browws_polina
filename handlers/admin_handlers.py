from aiogram import Router, F
from aiogram.filters import Text, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import default_state
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from datetime import timedelta, datetime

from FSM.admin import FSMAdminPriceSave, FSMAdminPriceDel, FSMAdminDateTime, FSMAdminTimeDel, FSMAdminSale, FSMAdminClientSucsess
from database import sqlite, models
from keyboards import keyboard_inline

router: Router = Router()

ID = [742757669, 1698315327]

# Что вы хотетите сделать после действие инлайн клавиатура
async def show_admin_menu(message_or_callback):
    admin_send_move = keyboard_inline.admin_send_move()
    if isinstance(message_or_callback, Message):
        await message_or_callback.answer(
            text="Что вы хотите сделать?\n\nЕсли ничего, введите команду --\n\n/cancel",
            reply_markup=admin_send_move.as_markup()
        )
    elif isinstance(message_or_callback, CallbackQuery):
        await message_or_callback.message.answer(
            text="Что вы хотите сделать?\n\nЕсли ничего, введите команду --\n\n/cancel",
            reply_markup=admin_send_move.as_markup()
        )   


@router.message(Command(commands='admin'), StateFilter(default_state))
async def admin_start(message: Message, state: FSMContext):
    if message.from_user.id in ID:
        await show_admin_menu(message)


# Add price
@router.callback_query(Text(text=['price_save']), StateFilter(default_state))
async def admin_service_input(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id in ID:
        await callback.message.edit_text(text="Введите наименование услуги.\n\nНапример: Коррекция воск/пинцет")
        await callback.answer()
        await state.set_state(FSMAdminPriceSave.service)

# Cancel
@router.message(Command(commands='cancel'), ~StateFilter(default_state))
async def admin_command_canselfsm(message: Message, state: FSMContext):
    if message.from_user.id in ID:    
        await message.answer(text='Вы вышли из настроек бота, чтобы вернуться введите команду\n\n/admin')    
        await state.clear()

# Cancel
@router.message(Command(commands='cancel'), StateFilter(default_state))
async def admin_command_cansel(message: Message):
    if message.from_user.id in ID:    
        await message.answer(text='Сейчас вы не настраиваете бота')

@router.message(StateFilter(FSMAdminPriceSave.service))
async def admin_service_load(message: Message, state: FSMContext):
    if message.from_user.id in ID:    
        await state.update_data(service=message.text)
        await state.set_state(FSMAdminPriceSave.price)
        await message.reply(text='Введите цену на услугу, только числом. Например - 500')

@router.message(StateFilter(FSMAdminPriceSave.price))
async def admin_price_input(message: Message, state: FSMContext):
    if message.from_user.id in ID:    
        await state.update_data(price=message.text)
        data = await state.get_data()
        models.add_price(service=data.get("service"), price=data.get("price"))
        
        await message.answer(text=f"отлично, услуга - {data.get('service')}. C ценой - {data.get('price')} добавлена")

        admin_send_move = keyboard_inline.admin_send_move()

        await show_admin_menu(message)

        await state.clear()



# Del price 
@router.callback_query(Text(text='price_del'), StateFilter(default_state))
async def admin_del_prices(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    price_del_keyboard = keyboard_inline.price_del_keyboard()

    await state.set_state(FSMAdminPriceDel.delete)
    await callback.message.edit_text(
        text="Выберите услугу, которую хотите удалить:",
        reply_markup=price_del_keyboard.as_markup()
    )

@router.callback_query(StateFilter(FSMAdminPriceDel.delete))
async def admin_del_price(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    service = callback.data

    models.delete_price(service)
    await callback.message.edit_text(text=f"Услуга - {service}. Удалена")
    await state.clear()

    admin_send_move = keyboard_inline.admin_send_move()
    
    await show_admin_menu(callback)

    await state.clear()


# Add Time
@router.callback_query(Text(text="time_save"), StateFilter(default_state))
async def admin_start_date_time(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id in ID:
        await callback.message.edit_text(text="Введите дату в формате ДД-ММ-ГГ:")
        await state.set_state(FSMAdminDateTime.date)

@router.message(StateFilter(FSMAdminDateTime.date))
async def admin_date(message: Message, state: FSMContext):
    try:
        date = datetime.strptime(message.text, '%d-%m-%Y').date()
        if date < date.today():
            await message.answer(text="Вы ввели прошедшую дату")
            return
        await state.update_data(date=date.strftime('%d-%m-%Y'))
        await message.answer(text="Введите время начала работы в формате ЧЧ:ММ")
        await state.set_state(FSMAdminDateTime.start_time)
    except ValueError:
        print("Не тот формат даты")

@router.message(StateFilter(FSMAdminDateTime.start_time))
async def admin_start_time(message: Message, state: FSMContext):
    try:
        time_start = datetime.strptime(message.text, '%H:%M').time()
        await state.update_data(start_time=time_start.strftime('%H:%M'))
        await message.answer(text="Введите время окончания работы в формате ЧЧ:ММ")
        await state.set_state(FSMAdminDateTime.end_time)
    except ValueError:
        print("Не тот формат времени")

@router.message(StateFilter(FSMAdminDateTime.end_time))
async def admin_end_time(message: Message, state: FSMContext):
    try:
        time_end = datetime.strptime(message.text, '%H:%M').time()
        await state.update_data(end_time=time_end.strftime('%H:%M'))
        await message.answer(text="День и время успешно добавлены")
        data = await state.get_data()
        models.add_date_time(date=data.get("date"), start_time=data.get("start_time"), end_time=data.get("end_time"))

        admin_send_move = keyboard_inline.admin_send_move()

        await show_admin_menu(message)

        await state.clear()        
    except ValueError:
        print("Не тот формат времени")


# Del Time
@router.callback_query(Text(text="time_del"), StateFilter(default_state))
async def admin_date_times_del(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    if callback.from_user.id in ID:
        date_del_keyboard = keyboard_inline.date_del_keyboard()
        await callback.message.edit_text(text="Выберите дату для удаления", reply_markup=date_del_keyboard.as_markup())
        await state.set_state(FSMAdminTimeDel.delete)        

@router.callback_query(StateFilter(FSMAdminTimeDel.delete))
async def process_date_time_del_ok(callback: CallbackQuery, state: FSMContext):
    # Получаем выбранную дату из callback_data кнопки
    await callback.answer()

    date = callback.data
    if date == None:
        models.date_time_del_none()
        await callback.message.edit_text(text=f"Дата работы {date} удалена")
    else:
        models.date_time_del(date)
        await callback.message.edit_text(text=f"Дата работы {date} удалена")

        admin_send_move = keyboard_inline.admin_send_move()

        await show_admin_menu(callback)


    await state.clear()


# Add sale
@router.callback_query(Text(text="sale_save"), StateFilter(default_state))
async def process_add_sale(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    if callback.from_user.id in ID:
        await state.set_state(FSMAdminSale.save)
        await callback.message.edit_text(text="Введите любой текст, который вы хотите видеть в разделе 'Скидки'")

@router.message(StateFilter(FSMAdminSale.save))
async def process_add_sale_ok(message: Message, state: FSMContext):
    sale = message.text
    models.add_sale(sale)
    await message.answer(text=f"Текст \n\n--- {sale} ---\n\n Успешно добавлен в раздел 'Скидки'")

    admin_send_move = keyboard_inline.admin_send_move()
    await show_admin_menu(message)

    await state.clear()    

# all client
@router.message(Command(commands="client"), StateFilter(default_state))
async def process_all_client(message: Message, state: FSMContext):
    if message.from_user.id in ID:
        all_client = models.get_enwork_client()
        client_sucsess = keyboard_inline.client_sucsess()

        if client_sucsess:
            await state.set_state(FSMAdminClientSucsess.client)
            await message.answer(
                text=f"Все клиенты:\n\n\n/cancel",
                reply_markup=client_sucsess.as_markup()
            )
        else:
            await message.answer(
                text=f"Клиентов нет")

@router.callback_query(Text(text="client_unsuc"), StateFilter(FSMAdminClientSucsess.client))
async def process_client_del(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    models.client_del(data.get("client_user_id"))
    await callback.message.delete()
    await state.clear()
    await callback.answer(text="Клиент Удален")
    await callback.answer()

@router.callback_query(StateFilter(FSMAdminClientSucsess.client))
async def process_client(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id in ID:
        await callback.answer()
        client_user_id = callback.data
        await state.update_data(client_user_id=client_user_id)
        data = await state.get_data()
        await callback.message.delete()

        client = models.client_user_id(data.get("client_user_id"))
        for row in client:
            client_del_or_pay = keyboard_inline.client_del_or_pay(row.client_user_id)
            await callback.message.answer(text=f'Клиент\n\nИмя:\n{row.client_name}\n\nУслуга:\n{row.client_service}\n\nДата:\n{row.appointment_date}\n\nВремя:\n{row.appointment_time}\n\nЦена услуг:\n{row.client_price} рублей\n\n\n/cancel', reply_markup=client_del_or_pay.as_markup())


# Del sale
@router.callback_query(Text(text="sale_del"), StateFilter(default_state))
async def process_del_sale(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    models.del_sale()
    await callback.message.edit_text(text="Все скидки успешно удалены")
    
    admin_send_move = keyboard_inline.admin_send_move()
    await show_admin_menu(callback)

    await state.clear()