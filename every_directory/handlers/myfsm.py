import sqlite3

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, StateFilter


from every_directory.keyboards.keyboard import make_keyboard, callback_keyboard, callback_keyboard1233

fsm_router = Router()

categoriii = ['Продукты', 'Транспорт', 'Развлечения']

class AddExp(StatesGroup):
    nachalnaya_trati = State()
    categoria = State()
    promezzutok_opisanie = State()
    add_or_noadd_opisanie = State()
    opisanie = State()



@fsm_router.message(StateFilter(None), Command('addexpence'))
async def cmd_addexp(message: Message, state: FSMContext):
    await message.answer('Введите сумму траты')
    await state.set_state(AddExp.nachalnaya_trati)


@fsm_router.message(AddExp.nachalnaya_trati)
async def handle_amount(message: Message, state: FSMContext):
        try:
            amount = float(message.text)
            await state.update_data(amount=amount)
            await message.answer('Выберете категорию', reply_markup=make_keyboard(categoriii))
            await message.answer('Хотите отменить действие?', reply_markup=callback_keyboard)
            await state.set_state(AddExp.categoria)

        except ValueError:
            await message.answer('Введите число')

@fsm_router.callback_query(F.data == 'yes_action')
async def handle_yes(callback: CallbackQuery, state: FSMContext):
    await callback.answer("Удалено")
    await state.clear()
    

@fsm_router.message(AddExp.categoria, F.text.in_(categoriii))
async def cmd_opisanie(message: Message, state: FSMContext):
    await state.update_data(category=message.text)
    await message.answer('Хотите добавить описание?',reply_markup=callback_keyboard1233)
    await state.set_state(AddExp.promezzutok_opisanie)


@fsm_router.message(AddExp.categoria)
async def cmd_opisanie(message: Message):
    await message.answer('Я не знаю такой категории',reply_markup=callback_keyboard1233)


@fsm_router.message(AddExp.promezzutok_opisanie, F.data == 'yes')
async def cmd_add_opisanie(callback: CallbackQuery, state: FSMContext):
     await callback.answer()
     await callback.message.edit_text("Введите описание:")
     await state.set_state(AddExp.opisanie)


@fsm_router.callback_query(AddExp.promezzutok_opisanie, F.data == 'no')
async def desc_no(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    with sqlite3.connect('mydatabase.db') as conn:
        conn.execute("""
            INSERT INTO noone (user_id, sum, category, description) VALUES (?, ?, ?, ?)
        """, (callback.from_user.id, float(data['amount']), data['category'], ""))
    
    await state.clear()


@fsm_router.message(AddExp.opisanie)
async def handle_description_input(message: Message, state: FSMContext):
     data = await state.get_data()
     with sqlite3.connect('mydatabase.db') as conn:
         conn.execute("""
            INSERT INTO noone (user_id, sum, category, description) VALUES (?, ?, ?, ?)
           """, (message.from_user.id, float(data['amount']), data['category'], message.text)
        )
     await message.answer('Успешно!')
     await state.clear()