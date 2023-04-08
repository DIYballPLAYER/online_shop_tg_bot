from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery, ContentType, InlineKeyboardMarkup

from tgbot.commands.admin import AdminCommands
from tgbot.config import MEDIA_DIR
from tgbot.keyboards.reply import ADMIN_KEYBOARD
from tgbot.misc.states import CreateCategoryState, CreateProductState, DeleteCategory, DeleteProduct
from tgbot.models.models import Category, Products


async def admin_start(message: Message):
    await message.reply("Привет админ!\nЧто будем делать?",
                        reply_markup=ADMIN_KEYBOARD)


async def add_product_category(message: Message):
    await message.answer('Напишите категорию продуктов которую хоитите добавить')
    await CreateCategoryState.name.set()


async def add_category(message: Message, state: FSMContext):
    await state.finish()
    check_category: Category = await Category.query.where(
        Category.name == message.text
    ).gino.first()
    if check_category:
        await message.answer('Такая категория уже существует!')
        return
    check_category: Category = await Category.create(name=f"{message.text}")
    await message.answer('Успешно создал')


async def category_list(message: Message):
    cat_list: Category = await Category.query.gino.all()
    if not category_list:
        await message.answer('Категорий нет')
        return
    await message.answer("\n\n".join(map(
        lambda cat: f"🆔: {cat.Id}\n🥫: {cat.name}\n",
        cat_list
    )))


async def create_product(message: Message):
    await CreateProductState.name.set()
    await message.answer('Напишите имя продукта которую хотите добавить')


async def create_product_name(message: Message, state: FSMContext):
    product = await Products.query.where(
        Products.name == message.text
    ).gino.first()
    if product:
        await message.answer('Продукт уже существует')
        return
    await state.update_data(name=message.text)
    keyboard = InlineKeyboardMarkup()
    cat_list = await Category.query.gino.all()
    if not cat_list:
        await message.answer('Категорий нет')
        return
    for cat in cat_list:
        keyboard.add(InlineKeyboardButton(cat.name, callback_data=cat.Id))
    await CreateProductState.category.set()
    await message.answer('Выберите категорию:', reply_markup=keyboard)


async def create_product_category(callback: CallbackQuery, state=CreateProductState.category):
    await state.update_data(category=int(callback.data))
    await callback.bot.delete_message(
        callback.from_user.id,
        callback.message.message_id
    )
    await CreateProductState.price.set()
    await callback.bot.send_message(
        callback.from_user.id,
        "Отлично! Отправьте цену на продукт!"
    )


async def create_product_price(message: Message, state: FSMContext):
    await state.update_data(price=int(message.text))
    await message.answer('Хорошо, а теперь отправьте описание продукта')
    await CreateProductState.description.set()


async def create_product_description(message: Message, state=FSMContext):
    await state.update_data(description=message.text)
    await CreateProductState.photo_url.set()
    await message.answer('А теперь отправь фото продукта')


async def create_product_photo(message: Message, state: FSMContext, content_types=ContentType.PHOTO):
    photo = await message.photo[0].download(destination_dir=MEDIA_DIR)
    await state.update_data(photo_url=photo.name)
    await message.answer('Отлично, продукт создан!!!')
    async with state.proxy() as data:
        products_data = data.as_dict()
    await Products.create(
        **products_data
    )
    await state.finish()


async def delete_product(message: Message):
    keyboard = InlineKeyboardMarkup()
    products_list = await Products.query.gino.all()
    if not products_list:
        await message.answer('Продуктов нет...')
        return
    for product in products_list:
        keyboard.add(InlineKeyboardButton(product.name, callback_data=product.Id))
    await DeleteProduct.callback_query.set()
    await message.answer('Выберите что хотите удалить...', reply_markup=keyboard)


async def product_list(message: Message):
    products_list: Products = await Products.query.gino.all()
    if not products_list:
        await message.answer('Категорий нет')
        return
    await message.answer("\n\n".join(map(
        lambda product: f"🆔: {product.Id}\n🥫: {product.name}\n",
        products_list
    )))


async def delete_product_callback_query(callback: CallbackQuery, state=FSMContext):
    product: Products = await Products.query.where(
        Products.Id == int(callback.data)
    ).gino.first()
    await product.delete()
    await callback.bot.send_message(
        callback.from_user.id,
        "Успешно удалил!"
    )
    await callback.bot.delete_message(
        callback.from_user.id,
        callback.message.message_id)
    await state.finish()


async def delete_category(message: Message):
    keyboard = InlineKeyboardMarkup()
    cat_list = await Category.query.gino.all()
    if not category_list:
        await message.answer('Категорий нет')
        return
    for cat in cat_list:
        keyboard.add(InlineKeyboardButton(cat.name, callback_data=cat.Id))
    await DeleteCategory.callback_query.set()
    await message.answer('Выберите категорию которую хотите удалить:', reply_markup=keyboard)


async def delete_category_callback_query(callback: CallbackQuery, state: FSMContext):
    category: Category = await Category.query.where(
        Category.Id == int(callback.data)
    ).gino.first()
    await category.delete()
    await callback.bot.send_message(
        callback.from_user.id,
        "Успешно удалил!"
    )
    await callback.bot.delete_message(
        callback.from_user.id,
        callback.message.message_id)
    await state.finish()


def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start, commands=["start"], state="*", is_admin=True)
    dp.register_message_handler(
        add_product_category, text=AdminCommands.add_cat.value
    )
    dp.register_message_handler(
        add_category, state=CreateCategoryState.name
    )
    dp.register_message_handler(
        category_list, text=AdminCommands.cat_list.value
    )
    dp.register_message_handler(
        product_list, text=AdminCommands.product_list.value
    )
    dp.register_message_handler(
        create_product, text=AdminCommands.add_product.value
    )
    dp.register_message_handler(
        create_product_name, state=CreateProductState.name
    )
    dp.register_callback_query_handler(
        create_product_category, state=CreateProductState.category
    )
    dp.register_message_handler(
        create_product_price, state=CreateProductState.price
    )
    dp.register_message_handler(
        create_product_description, state=CreateProductState.description
    )
    dp.register_message_handler(
        create_product_photo, state=CreateProductState.photo_url, content_types=ContentType.PHOTO
    )
    dp.register_message_handler(
        delete_category, text=AdminCommands.delete_cat.value
    )
    dp.register_callback_query_handler(
        delete_category_callback_query, state=DeleteCategory.callback_query
    )
    dp.register_message_handler(
        delete_product, text=AdminCommands.delete_product.value
    )
    dp.register_callback_query_handler(
        delete_product_callback_query, state=DeleteProduct.callback_query
    )
