from aiogram.types import InlineKeyboardButton

from tgbot.commands.user import UserCommands

ADD_CART = InlineKeyboardButton(UserCommands.cart.value, callback_data='add_cart')
NEXT = InlineKeyboardButton(UserCommands.next.value, callback_data='next')
PREVIOUS = InlineKeyboardButton(UserCommands.previous.value, callback_data='prev')
