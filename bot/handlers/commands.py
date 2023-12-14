from aiogram import F, Router, types
from aiogram.filters import Command, CommandObject, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import KeyboardButton, Message, ReplyKeyboardRemove

from bot.keyboards.button import button_yes_no
from bot.service.logic import GeneralLogic

router = Router()


class Form(StatesGroup):
    address = State()
    ask = State()


@router.message(CommandStart())
async def start(message: Message, state: FSMContext, session):
    await state.set_state(Form.address)

    await GeneralLogic(session).add_user(message)
    await message.answer(
        "Hi ! Please add your address, for example: London, England, zipcode: 123456"
    )


@router.message(Form.address)
async def process_address(message: Message, state: FSMContext, session):
    await state.update_data(name=message.text)
    await GeneralLogic(session).add_address(message)
    await state.set_state(Form.ask)
    await message.answer(
        "Do you wont listen othar commands ?",
        reply_markup=button_yes_no,
    )


@router.message(Form.ask, F.text.casefold() == "yes")
async def process_yes(message: Message, state: FSMContext):
    await state.clear()

    await message.reply(
        f"<b>/start</b> - Start bot\n <b>/info  id</b> - User info\n and remember your user id is {message.from_user.id}",
        parse_mode="HTML",
        reply_markup=ReplyKeyboardRemove(),
    )


@router.message(Form.ask, F.text.casefold() == "no")
async def process_no(message: Message, state: FSMContext):
    # data = await state.get_data()
    await state.clear()
    await message.reply(
        "It's sad. Goodbay!",
        reply_markup=types.ReplyKeyboardRemove(),
    )



@router.message(Command("info"))
async def info(message: Message, command: CommandObject, session):
    data  = await GeneralLogic(session).info(command.args)
    await message.answer(
        data,
        reply_markup=ReplyKeyboardRemove(),
    )