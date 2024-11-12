from dataclasses import dataclass
from environs import Env


@dataclass
class DatabaseConfig:
    db_uri: str


@dataclass
class WebhookConfig:
    host: str
    path: str


@dataclass
class WebappConfig:
    host: str
    port: int


@dataclass
class TgBot:
    token: str            # Токен для доступа к телеграм-боту


@dataclass
class Config:
    tg_bot: TgBot
    db: DatabaseConfig
    webhook: WebhookConfig
    webapp: WebappConfig


def load_config(path: str | None = None) -> Config:

    env: Env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env('BOT_TOKEN')
        ),
        db=DatabaseConfig(
            db_uri=env('DB_URI')
        ),
        webhook=WebhookConfig(
            host=env('WEBHOOK_HOST'),
            path=env('WEBHOOK_PATH')
        ),
        webapp=WebappConfig(
            host=env('WEBAPP_HOST'),
            port=env('WEBAPP_PORT')
        )
    )
