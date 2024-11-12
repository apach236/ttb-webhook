
import asyncpg
from config.config import Config, load_config

config: Config = load_config()
db_uri = config.db.db_uri


async def create_table():
    conn = await asyncpg.connect(dsn=db_uri)
    await conn.execute('''CREATE TABLE IF NOT EXISTS training 
                         (training_id int generated always as identity primary key, 
                         user_id int not null, 
                         date timestamp default current_date, 
                         category text not null)''')
    print("Table created")
    await conn.close()


async def save_to_db(user_id: int, category: str):
    conn = await asyncpg.connect(dsn=db_uri)
    await conn.execute('INSERT INTO training(user_id, category) VALUES ($1, $2)',
                       user_id, category)
    await conn.close()


async def check_training_today(user_id: int) -> bool:
    conn = await asyncpg.connect(dsn=db_uri)
    last_date = await conn.fetchval('''select date from training
                            where user_id = $1 
                            and date = current_date''',
                                    user_id)
    await conn.close()
    if last_date is None:
        return False
    else:
        return True


async def get_all_users() -> list:
    users: list = []
    conn = await asyncpg.connect(dsn=db_uri)
    all_users = await conn.fetch('select distinct user_id from training')
    for user in all_users:
        users.append(user['user_id'])
    await conn.close()
    return users


async def get_trainings(user_id: int, period: int) -> int:
    conn = await asyncpg.connect(dsn=db_uri)
    training_count = await conn.fetchval('''SELECT count(*)
                                            FROM training
                                            WHERE user_id = $1
                                            AND date > 
                                            (current_date - $2*interval '1 day') ''',
                                         user_id, period)
    await conn.close()
    return training_count
