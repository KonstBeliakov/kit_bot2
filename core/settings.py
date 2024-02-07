from environs import Env
from dataclasses import dataclass


@dataclass
class Bots:
    bot_token: str
    admin_id: int


@dataclass
class Settings:
    bots: Bots
    google_sheets_api_key: str
    spreadsheet_id: str


def get_settings(path: str):
    env = Env()
    env.read_env(path)

    return Settings(bots=Bots(bot_token=env.str('TOKEN'), admin_id=env.int('ADMIN_ID'), ),
                    google_sheets_api_key=env.str('GOOGLE_SHEETS_API_KEY'),
                    spreadsheet_id=env.str('SPREADSHEETS_ID'))


settings = get_settings('input')
