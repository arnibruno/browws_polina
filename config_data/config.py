from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str
    #pay_token: str


@dataclass
class Config:
    tg_bot: TgBot
    #pay_bot: TgBot


def load_config(path: str) -> Config:
    env = Env()
    env.read_env(path)
    return Config(
        tg_bot=TgBot(token=env("BOT_TOKEN"))#, #pay_token=env("PAYMENTS_TOKEN")),
        #pay_bot=TgBot(token=env("BOT_TOKEN"), pay_token=env("PAYMENTS_TOKEN"))
    )