from aiogram.types import CallbackQuery
from lexicon.lexicon import LEXICON_TRAININGS


def category_filter(callback: CallbackQuery) -> bool:
    return (callback.data in (LEXICON_TRAININGS) and callback.data != 'cancel')
