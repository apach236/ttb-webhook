import asyncio
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiohttp import web
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from config.config import Config, load_config
from handlers import other_handlers, user_handlers
from keyboards.main_menu import set_main_menu
from services.services import send_morning_ask
from database.database import create_table


logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s:%(lineno)d #%(levelname)-8s '
           '[%(asctime)s] - %(name)s - %(message)s'
)

logger = logging.getLogger(__name__)

config: Config = load_config()

WEBHOOK_HOST = config.webhook.host
WEBHOOK_PATH = config.webhook.path
WEBHOOK_URL = WEBHOOK_HOST + WEBHOOK_PATH

WEBAPP_HOST = config.webapp.host
WEBAPP_PORT = config.webapp.port


async def on_startup(bot: Bot) -> None:
    await bot.set_webhook(WEBHOOK_URL)


async def main():

    bot = Bot(
        token=config.tg_bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    app = web.Application()

    dp.startup.register(on_startup)
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
    )

    await create_table()
    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)

    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_morning_ask, 'cron', hour=17, args=(bot,))
    scheduler.start()

    await set_main_menu(bot)

    webhook_requests_handler.register(app, path=WEBHOOK_PATH)

    setup_application(app, dp, bot=bot)
    web.run_app(app, host=WEBAPP_HOST, port=WEBAPP_PORT)


if __name__ == '__main__':
    asyncio.run(main())
