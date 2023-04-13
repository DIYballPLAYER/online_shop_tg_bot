from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InputFile
from sqlalchemy import and_

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


async def order_product(message: Message):
    keyboard = InlineKeyboardMarkup()
    cat_list = await Category.query.gino.all()
    if not cat_list:
        await message.answer('Категорий нет')
        return
    for cat in cat_list:
        keyboard.add(InlineKeyboardButton(cat.name, callback_data=cat.Id))
    await message.answer('Выберите категорию:', reply_markup=keyboard)
    await OrderProduct.category.set()


async def order_product_(callback: CallbackQuery, state: FSMContext):
    cart: Cart = await Cart.query.where(
        Cart.user_id == callback.from_user.id
    ).gino.first()
    if not cart:
        await Cart.create(user_id=callback.from_user.id)
    await state.update_data(cart_id=cart.Id)
    await callback.bot.delete_message(
        callback.from_user.id,
        callback.message.message_id
    )
    products = await Products.query.where(
        Products.category == int(callback.data)
    ).gino.first()
    await state.update_data(category=int(callback.data))
    if not products:
        await callback.bot.send_message(callback.from_user.id, 'Продуктов в этой категории ещё нет...')
        await state.finish()
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
    await state.update_data(products_id=products.Id)


async def order_product_callback(callback: CallbackQuery, state: FSMContext):
    if callback.data in ['next', 'prev']:
        async with state.proxy() as data:
            if callback.data == 'next':
                product = await Products.query.where(and_(Products.category == data['category'],
                                                     Products.Id > data['products_id'])).gino.first()
                if product is None:
                    await callback.answer( 'Больше продуктов нет :(')
                    product = await Products.query.where(and_(Products.category == data['category'],
                                                              Products.Id == data['products_id'])).gino.first()
                else:
                    await state.update_data(products_id=product.Id)
            elif callback.data == 'prev':
                product = await Products.query.where(and_(Products.category == data['category'],
                                                     Products.Id < data['products_id'])).gino.first()
                if product is None:
                    await callback.answer( 'Больше продуктов нет :(')
                    product = await Products.query.where(and_(Products.category == data['category'],
                                                              Products.Id == data['products_id'])).gino.first()
                else:
                    await state.update_data(products_id=product.Id)
            await callback.bot.delete_message(
                callback.from_user.id,
                callback.message.message_id
            )
            keyboard = InlineKeyboardMarkup()
            keyboard.add(PREVIOUS,
                         ADD_CART,
                         NEXT)
            await callback.bot.send_photo(callback.from_user.id, photo=InputFile(product.photo_url),
                                          caption=f'Имя:{product.name}\n\n'
                                                  f'Категория:{product.category}\n\n'
                                                  f'Описание:{product.description}\n\n'
                                                  f'Цена:{product.price}', reply_markup=keyboard)
    elif callback.data == 'add_cart':
        async with state.proxy() as data:
            product = await Products.query.where(Products.Id == data['products_id']).gino.first()
            await state.update_data(amount=int(product.price))
        async with state.proxy() as data:
            order_data = data.as_dict()
            order_data.pop('category')
            await CartProducts.create(**order_data)
            await state.finish()
            await callback.bot.delete_message(
                callback.from_user.id,
                callback.message.message_id
            )
            await callback.bot.send_message(
                callback.from_user.id,
                'Успешно добавил в корзину'
            )


async def my_cart(message: Message):
    cart = await Cart.query.where(
        Cart.user_id == message.from_user.id
    ).gino.first()
    cart_products = await CartProducts.query.where(
        CartProducts.cart_id == cart.Id
    ).gino.first()
    print(cart_products)
    products_list = []
    amount = 0
    for products in cart_products:
        print(products.products_id)
        products = await Products.query.where(
            Products.Id == cart_products.products_id
        ).gino.first()
        products_list.append(products.name)
        amount += int(products.price)
        print(products_list)
        print(amount)
    await message.answer(
        f'У вас в корзине:{products_list}'
        f'Cумма заказа: {amount} сум'
    )


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=['start'], state='*')
    dp.register_message_handler(
        my_cart, text=UserCommands.my_cart.value
    )
    dp.register_message_handler(
        order_product, text=UserCommands.order.value
    )
    dp.register_callback_query_handler(
        order_product_, state=OrderProduct.category
    )
    dp.register_callback_query_handler(
        order_product_callback, state=OrderProduct.products_id
    )

