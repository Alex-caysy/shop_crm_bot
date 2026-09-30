from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def catalog_kb(products: list[dict]) -> InlineKeyboardMarkup:
    """Список товаров: каждая кнопка — товар."""
    kb = InlineKeyboardBuilder()
    for p in products:
        kb.button(text=f"{p['name']} — {p['price']:.0f} ₽",
                  callback_data=f"prod:{p['id']}")
    kb.adjust(1)
    return kb.as_markup()


def product_kb(product_id: int) -> InlineKeyboardMarkup:
    """Кнопки под карточкой товара."""
    kb = InlineKeyboardBuilder()
    kb.button(text="🛒 Заказать", callback_data=f"buy:{product_id}")
    kb.button(text="⬅️ К каталогу", callback_data="prod_list")
    kb.adjust(1)
    return kb.as_markup()