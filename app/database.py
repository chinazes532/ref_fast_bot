import aiosqlite as sq

from config import DB_NAME


async def create_db():
    async with sq.connect(DB_NAME) as db:
        print("Database created!")

        await db.execute("""CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            ref_link TEXT,
            invited_by INTEGER,
            ref_count INTEGER,
            balance INTEGER,
            register_date TEXT
        )""")

        await db.commit()


async def add_user(user_id, ref_link, invited_by, ref_count, register_date, balance):
    async with sq.connect(DB_NAME) as db:
        async with db.execute('SELECT user_id, invited_by, ref_count FROM users WHERE user_id = ?',
                              (user_id,)) as cursor:
            result = await cursor.fetchone()

        if result:
            # Пользователь уже зарегистрирован
            if result[2] == 0 and not result[1]:
                # Проверяем, что пользователь не перешел по своей собственной реферальной ссылке
                if invited_by and invited_by != user_id:
                    await db.execute('UPDATE users SET invited_by = ? WHERE user_id = ?', (invited_by, user_id))
                    await db.commit()
                    return True
                else:
                    return False
            else:
                # Пользователь уже перешел по реферальной ссылке или уже пригласил других
                return False
        else:
            await db.execute(
                'INSERT INTO users (user_id, ref_link, invited_by, ref_count, register_date, balance) VALUES (?, ?, ?, ?, ?, ?)',
                (user_id, ref_link, invited_by, ref_count, register_date, balance))
            await db.commit()
            return True


async def check_referral(ref_link):
    async with sq.connect(DB_NAME) as db:  # Укажите путь к вашей базе данных
        async with db.execute('SELECT user_id FROM users WHERE user_id = ?', (int(ref_link),)) as cursor:
            result = await cursor.fetchone()
            if result:
                return int(ref_link)
    return None


async def increment_referral_count(user_id):
    async with sq.connect(DB_NAME) as db:
        # Проверка на существование user_id
        async with db.execute('SELECT COUNT(*) FROM users WHERE user_id = ?', (user_id,)) as cursor:
            count = await cursor.fetchone()
            if count[0] == 0:
                print("User not found")
                return

        # Выполнение обновления: увеличение ref_count и balance
        async with db.execute('''
            UPDATE users 
            SET ref_count = ref_count + 1, balance = balance + 1 
            WHERE user_id = ?
        ''', (user_id,)) as cursor:
            await db.commit()
