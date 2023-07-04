from aiogram.filters.state import State, StatesGroup


class FSMAdminPriceSave(StatesGroup):
    service = State()
    price = State()


class FSMAdminPriceDel(StatesGroup):
    delete = State()

class FSMAdminDateTime(StatesGroup):
    date = State()
    start_time = State()
    end_time = State()


class FSMAdminMove(StatesGroup):
    price_save = State()
    price_del = State()
    time_save = State()
    time_del = State()
    sale_save = State()
    sale_del = State()


class FSMAdminPrice(StatesGroup):
    service = State()
    price = State()


class FSMAdminTimeDel(StatesGroup):
    delete = State()


class FSMAdminSale(StatesGroup):
    save = State()
    delete = State()


class FSMAdminClientSucsess(StatesGroup):
    all_client = State()
    client = State()