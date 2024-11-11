
from aiogram import Router
from aiogram.types import Message

from lexicon.lexicon import LEXICON

router = Router()


@router.message()
async def process_other_messages(message: Message):
    await message.answer(LEXICON['other_message'])
