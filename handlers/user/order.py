from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

import database.db as db
from keyboards.reply import cancel_kb, main_menu
from states.user_states import OrderStates

router = Router()


@router.message(F.text == "❌ Отмена")
async def cancel_handler(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Действие отменено.", reply_markup=main_menu())


@router.callback_query(F.data.startswith("buy:"))
async def start_order(callback: CallbackQuery, state: FSMContext):
    product_id = int(callback.data.split(":")[1])
    product = await db.get_product(product_id)
    if product is None:
        await callback.answer("Товар не найден 😕", show_alert=True)
        return

    # Сохраняем товар в данных состояния и запускаем FSM
    await state.update_data(product_id=product_id)
    await state.set_state(OrderStates.name)

    await callback.message.answer(
        f"Вы выбрали: {product['name']} ({product['price']:.0f} ₽)\n\n"
        "Как вас зовут?",
        reply_markup=cancel_kb(),
    )
    await callback.answer()


@router.message(OrderStates.name, F.text)
async def process_name(message: Message, state: FSMContext):
    if len(message.text) < 2:
        await message.answer("Имя слишком короткое. Введите ещё раз:")
        return

    await state.update_data(name=message.text)
    await state.set_state(OrderStates.phone)
    await message.answer(
        f"Приятно познакомиться, {message.text}!\nТеперь введите номер телефона:"
    )


@router.message(OrderStates.phone, F.text)
async def process_phone(message: Message, state: FSMContext):
    digits = "".join(ch for ch in message.text if ch.isdigit())
    if len(digits) < 10:
        await message.answer("Похоже, это не телефон. Введите ещё раз:")
        return

    await state.update_data(phone=message.text)
    await state.set_state(OrderStates.confirm)

    data = await state.get_data()
    product = await db.get_product(data["product_id"])
    await message.answer(
        "📋 Проверьте заказ:\n\n"
        f"🛍 Товар: {product['name']}\n"
        f"💰 Цена: {product['price']:.0f} ₽\n"
        f"👤 Имя: {data['name']}\n"
        f"📞 Телефон: {data['phone']}\n\n"
        "Всё верно? (да / нет)",
        reply_markup=cancel_kb(),
    )


@router.message(OrderStates.confirm, F.text)
async def process_confirm(message: Message, state: FSMContext):
    if message.text.lower() not in ("да", "yes", "👍"):
        await state.clear()
        await message.answer("Заказ отменён.", reply_markup=main_menu())
        return

    data = await state.get_data()
    order_id = await db.save_order(
        user_id=message.from_user.id,
        username=message.from_user.username,
        product_id=data["product_id"],
        customer_name=data["name"],
        phone=data["phone"],
    )

    await state.clear()
    await message.answer(
        f"✅ Спасибо, {data['name']}! Заказ №{order_id} принят.\n"
        f"Мы свяжемся с вами по номеру {data['phone']}",
        reply_markup=main_menu(),
    )
