import aiosqlite

DB_PATH = "shop.db"


async def init_db() -> None:
    """Создаёт таблицы (если их нет) и наполняет каталог тестовыми товарами."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS products (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                name        TEXT NOT NULL,
                description TEXT,
                price       REAL NOT NULL
            )
            """
        )
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS orders (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id       INTEGER NOT NULL,
                username      TEXT,
                product_id    INTEGER,
                customer_name TEXT NOT NULL,
                phone         TEXT NOT NULL,
                created_at    TEXT DEFAULT (datetime('now'))
            )
            """
        )

        # Тестовые товары — добавляем только если таблица пуста
        cursor = await db.execute("SELECT COUNT(*) FROM products")
        (count,) = await cursor.fetchone()
        if count == 0:
            await db.executemany(
                "INSERT INTO products (name, description, price) VALUES (?, ?, ?)",
                [
                    ("Кружка «Dev»", "Керамика, 350 мл, чёрная", 590),
                    ("Худи «Python»", "Хлопок 80%, принт, размер M", 2490),
                    ("Набор наклеек", "10 стикеров про жизнь программиста", 290),
                ],
            )

        await db.commit()


async def get_all_products() -> list[dict]:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT id, name, description, price FROM products ORDER BY id"
        )
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]


async def get_product(product_id: int) -> dict | None:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("SELECT * FROM products WHERE id = ?", (product_id,))
        row = await cursor.fetchone()
        return dict(row) if row else None


async def save_order(user_id: int, username: str | None,
                     product_id: int, customer_name: str, phone: str) -> int:
    """Сохраняет заказ и возвращает его номер."""
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            """
            INSERT INTO orders (user_id, username, product_id, customer_name, phone)
            VALUES (?, ?, ?, ?, ?)
            """,
            (user_id, username, product_id, customer_name, phone),
        )
        await db.commit()
        return cursor.lastrowid
