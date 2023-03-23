from aiogram import Dispatcher
from aiogram.types import Message

from tgbot.commands.user import UserCommands
from tgbot.keyboards.reply import USER_KEYBOARD
from tgbot.models.models import Users


async def user_start(message: Message):
    user = await Users.query.where(Users.tg_id == message.from_user.id
    ).gino.first()
    if not user:
        await Users.create(tg_id=message.from_user.id)
    await message.reply('Привет пользователь! \nЗдесь ты можешь заказать себе продукты'
                        ' для хозяйства не выходя из дома:)',
                        reply_markup=USER_KEYBOARD)


async def order_product(message: Message):
    pass


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=['start'], state='*')
    dp.register_message_handler(
        order_product, text=UserCommands.order.value
    )
