from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from tgbot.commands.admin import AdminCommands
from tgbot.keyboards.reply import ADMIN_KEYBOARD
from tgbot.misc.states import CreateCategoryState
from tgbot.models.models import Category


async def admin_start(message: Message):
    await message.reply("Hello, admin!\nWanna add/delete smthing?",
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
