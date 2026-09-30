from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

import database.db as db
from keyboards.inline import catalog_kb, product_kb
from keyboards.reply import main_menu

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        f"Привет, {message.from_user.full_name}! 👋\n\n"
        "Это магазин-бот. Выберите действие:",
        reply_markup=main_menu(),
    )


@router.message(F.text == "🛍 Каталог")
async def show_catalog(message: Message):
    products = await db.get_all_products()
    await message.answer("📖 Наш каталог:", reply_markup=catalog_kb(products))


@router.message(F.text == "🛒 Заказать")
async def order_from_menu(message: Message):
    # Заказ всегда начинается с выбора товара
    products = await db.get_all_products()
    await message.answer("🛒 Выберите товар:", reply_markup=catalog_kb(products))


@router.message(F.text == "ℹ️ О нас")
async def show_about(message: Message):
    await message.answer(
        "ℹ️ Мы — магазин полезных штук.\nРаботаем с 9:00 до 21:00."
    )


# ---------- Обработка нажатий inline-кнопок ----------

@router.callback_query(F.data == "prod_list")
async def cb_back_to_catalog(callback: CallbackQuery):
    products = await db.get_all_products()
    await callback.message.edit_text(
        "📖 Наш каталог:", reply_markup=catalog_kb(products)
    )
    await callback.answer()


@router.callback_query(F.data.startswith("prod:"))
async def cb_show_product(callback: CallbackQuery):
    product_id = int(callback.data.split(":")[1])
    product = await db.get_product(product_id)
    if product is None:
        await callback.answer("Товар не найден 😕", show_alert=True)
        return

    await callback.message.edit_text(
        f"🏷 {product['name']}\n\n"
        f"{product['description']}\n\n"
        f"💰 Цена: {product['price']:.0f} ₽",
        reply_markup=product_kb(product["id"]),
    )
    await callback.answer()
