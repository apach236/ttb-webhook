import asyncio
import logging


from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config.config import Config, load_config
from handlers import other_handlers, user_handlers
from keyboards.main_menu import set_main_menu
from services.services import send_morning_ask
from database.database import create_table

logger = logging.getLogger(__name__)


async def main():

    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s'
    )
    logger.info('Starting bot')

    config: Config = load_config()
    bot = Bot(
        token=config.tg_bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    await create_table()
    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)

    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_morning_ask, 'cron', hour=17, args=(bot,))
    scheduler.start()

    await set_main_menu(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


asyncio.run(main())
