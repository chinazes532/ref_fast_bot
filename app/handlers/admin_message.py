from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

import app.keyboards.reply as rkb
import app.keyboards.builder as bkb
import app.keyboards.inline as ikb

from app.filters.admin_filter import AdminProtect


admin = Router()


@admin.message(AdminProtect(), Command("admin"))
@admin.message(AdminProtect(), F.text == "Админ-панель")
async def admin_panel(message: Message):
    await message.answer(f"Вы вошли в админ-панель!\n"
                         f"Выберите действие",
                         reply_markup=ikb.admin_panel)