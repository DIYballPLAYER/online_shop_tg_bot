from enum import Enum


class AdminCommands(Enum):
    add_product = 'Добавить продукт😋'
    add_cat = 'Добавить категорию продуктов🍽️'
    delete_product = 'Удалить продукт🔪'
    delete_cat = 'Удалить категорию продуктов🥢'
    cat_list = 'Список категорий'
    product_list = 'Список подуктов'