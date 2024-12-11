from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

admin_panel = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Текст 1", callback_data="text_1")],
    ]
)