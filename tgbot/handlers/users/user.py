from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InputFile

from tgbot.buttons.inline import PREVIOUS, ADD_CART, NEXT
from tgbot.commands.user import UserCommands
from tgbot.keyboards.reply import USER_KEYBOARD
from tgbot.misc.states import CreateProductState, OrderProduct
from tgbot.models.models import Users, Category, Products, Cart, CartProducts


async def user_start(message: Message):
    user = await Users.query.where(Users.tg_id == message.from_user.id).gino.first()
    if not user:
        await Users.create(tg_id=message.from_user.id)
    await message.reply('Привет пользователь! \nЗдесь ты можешь заказать себе продукты'
                        ' для хозяйства не выходя из дома:)',
                        reply_markup=USER_KEYBOARD)
    await OrderProduct.cart_id.set()


async def order_product(message: Message, state: FSMContext):
    cart: Cart = await Cart.query.where(
        Cart.user_id == message.from_user.id
    ).gino.first()
    if not cart:
        await Cart.create(user_id=message.from_user.id)
    await state.update_data(cart_id=cart.Id)
    keyboard = InlineKeyboardMarkup()
    cat_list = await Category.query.gino.all()
    if not cat_list:
        await message.answer('Категорий нет')
        return
    for cat in cat_list:
        keyboard.add(InlineKeyboardButton(cat.name, callback_data=cat.Id))
    await message.answer('Выберите категорию:', reply_markup=keyboard)
    await OrderProduct.choose.set()
    await state.update_data(choose=2)


async def order_product_(callback: CallbackQuery, state: FSMContext):
    await callback.bot.delete_message(
        callback.from_user.id,
        callback.message.message_id
    )
    products = await Products.query.where(
        Products.category == int(callback.data)
    ).gino.first()
    if not products:
        await callback.bot.send_message(callback.from_user.id, 'Продуктов в этой категории ещё нет...')
    keyboard = InlineKeyboardMarkup()
    keyboard.add(PREVIOUS,
                 ADD_CART,
                 NEXT)
    await callback.bot.send_photo(callback.from_user.id, photo=InputFile(products.photo_url),
                                caption=f'Имя:{products.name}\n\n'
                                              f'Категория:{products.category}\n\n'
                                              f'Описание:{products.description}\n\n'
                                              f'Цена:{products.price}', reply_markup=keyboard)
    await OrderProduct.products_id.set()


async def order_product_callback(callback: CallbackQuery, state: FSMContext):
    if callback.data in ['next', 'prev']:
        async with state.proxy() as data:
            count = data['choose']
        if callback.data == 'next':
            product = await Products.query.gino.limit(count)[-1]
            await state.update_data(choose=count+1)
        else:
            if count <= 0:
                count = 1
            if count == 1:
                category = await Category.query.gino.first()
            else:
                category = await Category.gino.limit(count - 1)[-1]
            await state.update_data(choose=count - 1)
        product = await Products.query.where(
            Products.category == Category.Id
        ).gino.first()
        keyboard = InlineKeyboardMarkup()
        keyboard.add(PREVIOUS,
                     ADD_CART,
                     NEXT)
        await callback.bot.delete_message(
            callback.from_user.id,
            callback.message.message_id
        )
        await callback.bot.send_photo(callback.from_user.id, photo=InputFile(product.photo_url),
                                      caption=f'Имя:{product.name}\n\n'
                                              f'Категория:{product.category}\n\n'
                                              f'Описание:{product.description}\n\n'
                                              f'Цена:{product.price}', reply_markup=keyboard)


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=['start'], state='*')
    dp.register_message_handler(
        order_product, text=UserCommands.order.value, state=OrderProduct.cart_id
    )
    dp.register_callback_query_handler(
        order_product_, state=OrderProduct.choose
    )
    dp.register_callback_query_handler(
        order_product_callback, state=OrderProduct.products_id
    )
