from aiogram import Router
from aiogram.types import Message

from lexicon.lexicon import LEXICON_RU


router: Router = Router()

@router.message()
async def text_handler(message: Message):
    print(message.json(indent=4))
    await message.answer(text=(LEXICON_RU["answer"]["love"]))