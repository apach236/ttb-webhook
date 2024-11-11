
from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message
from random import choice
from database.database import check_training_today
from filters.filters import category_filter
from keyboards.training_kb import create_asking_keyboard, create_trainings_keyboard, create_insure_keyboard
from lexicon.lexicon import LEXICON, LEXICON_YELLS
from services.services import send_statistics, save_training

router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(LEXICON[message.text])
    if await check_training_today(message.from_user.id):
        await message.answer(text=LEXICON['already_exist'])
    else:
        await message.answer(text=LEXICON['ask_training'],
                             reply_markup=create_asking_keyboard())


@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(LEXICON[message.text])
    if await check_training_today(message.from_user.id):
        await message.answer(text=LEXICON['already_exist'])
    else:
        await message.answer(text=LEXICON['ask_training'],
                             reply_markup=create_asking_keyboard())


@router.message(Command(commands='statistics'))
async def process_statistics_command(message: Message):
    await message.answer(
        text=f'{LEXICON[message.text]} {await send_statistics(message.from_user.id)}'
    )


@router.callback_query(F.data == 'yes')
async def send_trainings_keyboard(callback: CallbackQuery):
    await callback.message.edit_text(
        text=LEXICON['which_training'],
        reply_markup=create_trainings_keyboard()
    )


@router.callback_query(F.data == 'no')
async def insure_no_trainings(callback: CallbackQuery):
    await callback.message.edit_text(
        text=LEXICON['insure_no_training'],
        reply_markup=create_insure_keyboard()
    )


@router.callback_query(F.data == 'sure')
async def answer_no_trainings(callback: CallbackQuery):
    await callback.message.edit_text(text=LEXICON['no_training_today'])
    await callback.answer(choice(LEXICON_YELLS['shame']))


@router.callback_query(F.data == 'cancel')
async def process_cancel_button(callback: CallbackQuery):
    await callback.message.edit_text(
        text=LEXICON['ask_training'],
        reply_markup=create_asking_keyboard()
    )


@router.callback_query(category_filter)
async def process_training_category(callback: CallbackQuery):
    await callback.message.edit_text(
        await save_training(callback.data, callback.from_user.id)
    )
    await callback.answer(choice(LEXICON_YELLS['motivation']))
