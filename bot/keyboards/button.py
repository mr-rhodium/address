from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

button_yes_no=ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Yes"),
            KeyboardButton(text="No"),
        ]
    ],
    resize_keyboard=True,
)
