from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import FSInputFile
from aiogram import Bot

from crud_functions import is_included, add_user

admin = Router()


class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = State()


@admin.message(F.text == 'Регистрация')
async def sing_up(message: Message, state: FSMContext):
    await state.set_state(RegistrationState.username)
    await message.answer("Введите имя пользователя (только латинский алфавит):")


@admin.message(RegistrationState.username)
async def sing_up(message: Message, state: FSMContext):
    username = message.text
    if not is_included(username):
        await state.update_data(username=message.text)
        await message.answer("Введите email:")
        await state.set_state(RegistrationState.email)
    else:
        await message.answer("Такой пользователь уже существует")
        await state.set_state(RegistrationState.username)


@admin.message(RegistrationState.email)
async def set_email(message: Message, state: FSMContext):
    await state.update_data(email=message.text)
    await message.answer("Введите возраст:")
    await state.set_state(RegistrationState.age)


@admin.message(RegistrationState.age)
async def set_age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    data = await state.get_data()
    await add_user(data['username'], data['email'], int(data['age']))
    await message.answer("Вы успешно зарегистрировались")
    await state.clear()
