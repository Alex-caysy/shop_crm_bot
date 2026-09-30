from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def main_menu() -> ReplyKeyboardMarkup:
    """Главное меню бота."""
    kb = ReplyKeyboardBuilder()
    kb.button(text="🛍 Каталог")
    kb.button(text="🛒 Заказать")
    kb.button(text="ℹ️ О нас")
    kb.adjust(2, 1)  # 2 кнопки в первом ряду, 1 во втором
    return kb.as_markup(resize_keyboard=True)


def cancel_kb() -> ReplyKeyboardMarkup:
    """Клавиатура во время диалога (только кнопка отмены)."""
    kb = ReplyKeyboardBuilder()
    kb.button(text="❌ Отмена")
    return kb.as_markup(resize_keyboard=True)