
import logging

from aiogram import Bot
from datetime import date, timedelta
from lexicon.lexicon import LEXICON, LEXICON_TRAININGS
from keyboards.training_kb import create_asking_keyboard
from database.database import check_training_today, get_all_users, get_tarinings, save_to_db
from keyboards.training_kb import create_asking_keyboard

logger = logging.getLogger(__name__)


async def send_morning_ask(bot: Bot):
    users = await get_all_users()
    for user in users:
        try:
            await bot.send_message(user,
                                   LEXICON['ask_training_new_day'],
                                   reply_markup=create_asking_keyboard())
        except TypeError:
            logger.warning('User or Chat not found')


async def save_training(category: str, user_id):
    if await check_training_today(user_id):
        answer = LEXICON['already_exist']
        logger.warning(type(check_training_today(user_id)))
    else:
        await save_to_db(user_id, category)
        answer = f'{LEXICON["saved"]} {LEXICON_TRAININGS[category]} - {date.today()}'
    return answer


async def send_statistics(user_id: int) -> str:
    period = 14
    trainings: list = await get_tarinings(user_id, period)
    first_date = str(date.today()-timedelta(days=period))
    for day in trainings:
        if day >= first_date:
            number_of_trainings = len(trainings[trainings.index(day):])
            break
    return (f'{LEXICON["stat"]} {number_of_trainings}')
