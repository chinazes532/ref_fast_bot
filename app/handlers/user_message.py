from datetime import datetime

from aiogram import F, Router, Bot
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

import app.keyboards.reply as rkb
import app.keyboards.builder as bkb
import app.keyboards.inline as ikb

from app.filters.admin_filter import AdminProtect

from app.database import add_user, check_referral, increment_referral_count

from config import BOT_USERNAME

user = Router()


@user.message(CommandStart())
async def start_command(message: Message, bot: Bot, command: CommandObject):
    admin = AdminProtect()
    user_id = message.from_user.id
    ref_link = command.args
    current_time = datetime.now()

    # Проверяем, является ли пользователь администратором
    if await admin(message):
        await message.answer(f"Привет, {message.from_user.full_name}!\nВы успешно авторизовались как администратор!",
                             reply_markup=rkb.admin_menu)
        return

    # Добавляем пользователя в базу данных
    user_registered = await add_user(user_id=user_id,
                                     ref_link=f'https://t.me/{BOT_USERNAME}?start={user_id}',
                                     invited_by=None,
                                     ref_count=0,
                                     register_date=current_time,
                                     balance=0)

    if user_registered:
        # Проверяем реферальную ссылку
        if ref_link:
            invited_by = await check_referral(ref_link)
            if invited_by:
                await add_user(user_id=user_id,
                               ref_link=f'https://t.me/{BOT_USERNAME}?start={user_id}',
                               invited_by=invited_by,
                               ref_count=0,
                               register_date=current_time,
                               balance=0)

                await bot.send_message(chat_id=user_id,
                                       text=f"Вы зарегистрировались на сайте. Приглашенный вами пользователь: @{invited_by}")
                await bot.send_message(invited_by,
                                       f"Пользователь @{message.from_user.username} с ID {user_id} зарегистрировался по вашей реферальной ссылке.")
                await increment_referral_count(invited_by)
            else:
                await bot.send_message(chat_id=user_id,
                                       text=f" 1 Вы зарегистрировались на сайте. Ваша реферальная ссылка: https://t.me/{BOT_USERNAME}?start={user_id}")
        else:
            await bot.send_message(chat_id=user_id,
                                   text=f" 2 Вы зарегистрировались на сайте. Ваша реферальная ссылка: https://t.me/{BOT_USERNAME}?start={user_id}")
    else:
        await bot.send_message(chat_id=user_id, text="Вы уже зарегистрированы!")

