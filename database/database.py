
import aiosqlite

from datetime import date


async def create_table():
    async with aiosqlite.connect('data/training.db') as db:
        await db.execute('''CREATE TABLE IF NOT EXISTS training 
                         (training_id integer primary key autoincrement, 
                         user_id integer not null, 
                         date text not null, 
                         category text not null)''')
        await db.commit()


async def save_to_db(user_id: int, category: str):
    async with aiosqlite.connect('data/training.db') as db:
        await db.execute('INSERT INTO training(user_id, date, category) VALUES (?, ?, ?)',
                         (user_id, str(date.today()), category))
        await db.commit()


async def check_training_today(user_id: int) -> bool:
    async with aiosqlite.connect('data/training.db') as db:
        async with db.execute('''select date from training
                            where user_id = ?
                            order by date desc limit 1''',
                              (user_id,)) as cursor:
            last_date = await cursor.fetchone()
    if last_date is None:
        return False
    else:
        return last_date[0] == str(date.today())


async def get_all_users() -> tuple:
    users: tuple = tuple()
    async with aiosqlite.connect('data/training.db') as db:
        async with db.execute('select distinct user_id from training') as cursor:
            async for user in cursor:
                users += user
    return users


async def get_tarinings(user_id: int, period: int) -> list:
    trainings: list = []
    async with aiosqlite.connect('data/training.db') as db:
        async with db.execute('''select date from training
                                where user_id = ?
                                order by date limit ?''',
                              (user_id, period)) as cursor:
            async for training in cursor:
                trainings.append(training[0])
    return trainings
