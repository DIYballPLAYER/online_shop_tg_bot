from aiogram.dispatcher.filters.state import StatesGroup, State


class CreateCategoryState(StatesGroup):
    name = State()


class CreateProductState(StatesGroup):
    name = State()
    category = State()
    price = State()
    description = State()
    photo_url = State()


class DeleteCategory(StatesGroup):
    callback_query = State()


class DeleteProduct(StatesGroup):
    callback_query = State()


class OrderProduct(StatesGroup):
    category = State()
    cart_id = State()
    products_id = State()


