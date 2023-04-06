from aiogram.types import KeyboardButton

from tgbot.commands.admin import AdminCommands
from tgbot.commands.user import UserCommands

ADD_PRODUCT = KeyboardButton(AdminCommands.add_product.value)
ADD_PRODUCT_CAT = KeyboardButton(AdminCommands.add_cat.value)
DELETE_PRODUCT = KeyboardButton(AdminCommands.delete_product.value)
DELETE_PRODUCT_CAT = KeyboardButton(AdminCommands.delete_cat.value)
CATEGORY_LIST = KeyboardButton(AdminCommands.cat_list.value)
PRODUCT_LIST = KeyboardButton(AdminCommands.product_list.value)

ORDER = KeyboardButton(UserCommands.order.value)
CART = KeyboardButton(UserCommands.cart.value)