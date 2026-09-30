from aiogram.fsm.state import State, StatesGroup


class OrderStates(StatesGroup):
    """Состояния оформления заказа."""

    name = State()     # ждём имя
    phone = State()    # ждём телефон
    confirm = State()  # ждём подтверждение