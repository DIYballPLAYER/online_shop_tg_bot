from aiogram.dispatcher.filters.state import StatesGroup, State


class CreateCategoryState(StatesGroup):
    name = State()


class CreateProductState(StatesGroup):
    name = State()
    description = State()
    category = State()
    price = State()
    image = State()
    confirm = State()








