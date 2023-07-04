from aiogram.filters.state import State, StatesGroup


class FSMUsersAnEyebrow(StatesGroup):
    name = State()
    service = State()
    date = State()
    time = State()
    payments = State()
    sucsess = State()