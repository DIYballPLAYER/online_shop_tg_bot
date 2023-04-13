from aiogram.types import ReplyKeyboardMarkup

from tgbot.buttons.reply import ADD_PRODUCT, ADD_PRODUCT_CAT, DELETE_PRODUCT, DELETE_PRODUCT_CAT, ORDER, CATEGORY_LIST, \
    PRODUCT_LIST, MY_CART

ADMIN_KEYBOARD = ReplyKeyboardMarkup([
    [ADD_PRODUCT, ADD_PRODUCT_CAT], [DELETE_PRODUCT, DELETE_PRODUCT_CAT], [CATEGORY_LIST, PRODUCT_LIST]
], resize_keyboard=True)


USER_KEYBOARD = ReplyKeyboardMarkup([
    [ORDER], [MY_CART]
], resize_keyboard=True)
