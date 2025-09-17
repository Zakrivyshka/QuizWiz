from aiogram import types, F
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from database import get_quiz_index, update_quiz_index, get_quiz_right_answer, get_quiz_wrong_answer
from keyboards import generate_options_keyboard, generate_start_keyboard, generate_stats_keyboard
from quiz_data import quiz_data

async def cmd_start(message: types.Message):
    await message.answer("Добро пожаловать в квиз!", reply_markup=generate_start_keyboard())

async def cmd_start(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Начать игру"))
    builder.add(types.KeyboardButton(text="Статистика"))
    builder.adjust(2)
    await message.answer("Добро пожаловать в квиз!", reply_markup=builder.as_markup(resize_keyboard=True))

async def cmd_quiz(message: types.Message):
    await message.answer("Давайте начнем квиз!")
    await new_quiz(message)

async def cmd_stats(message: types.Message):
    user_id = message.from_user.id
    right = await get_quiz_right_answer(user_id)
    wrong = await get_quiz_wrong_answer(user_id)

    total = right + wrong
    
    table = (
        "Статистика Ваших ответов:\n\n"
        f"Правильные: {right:2d}\n"
        f"Неправильные: {wrong:2d}\n"
        f"Всего: {total:2d}\n"
    )
    
    await message.answer(table)
    
async def new_quiz(message):
    user_id = message.from_user.id
    await update_quiz_index(user_id, 0, 0, 0)
    await get_question(message, user_id)

async def get_question(message, user_id):
    current_question_index = await get_quiz_index(user_id)
    correct_index = quiz_data[current_question_index]['correct_option']
    opts = quiz_data[current_question_index]['options']
    kb = generate_options_keyboard(opts, opts[correct_index])
    await message.answer(f"{quiz_data[current_question_index]['question']}", reply_markup=kb)

async def right_answer(callback: types.CallbackQuery):
    selected_option = callback.message.reply_markup.inline_keyboard[0][0].text
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )

    await callback.message.answer(f"Ваш ответ: {selected_option}✅")
    current_question_index = await get_quiz_index(callback.from_user.id)
    current_right_answer = await get_quiz_right_answer(callback.from_user.id)
    current_wrong_answer = await get_quiz_wrong_answer(callback.from_user.id)
    current_question_index += 1
    current_right_answer += 1
    await update_quiz_index(callback.from_user.id, current_question_index, current_right_answer, current_wrong_answer)

    if current_question_index < len(quiz_data):
        await get_question(callback.message, callback.from_user.id)
    else:
        await callback.message.answer("Это был последний вопрос. Квиз завершен!🎉")

async def wrong_answer(callback: types.CallbackQuery):
    selected_option = callback.message.reply_markup.inline_keyboard[0][0].text
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )

    current_question_index = await get_quiz_index(callback.from_user.id)
    correct_option = quiz_data[current_question_index]['correct_option']

    await callback.message.answer(
        f"Вы выбрали: {selected_option}❌\n"
        f"Правильный ответ: {quiz_data[current_question_index]['options'][correct_option]}")

    current_right_answer = await get_quiz_right_answer(callback.from_user.id)
    current_wrong_answer = await get_quiz_wrong_answer(callback.from_user.id)
    current_question_index += 1
    current_wrong_answer += 1
    await update_quiz_index(callback.from_user.id, current_question_index, current_right_answer, current_wrong_answer)

    if current_question_index < len(quiz_data):
        await get_question(callback.message, callback.from_user.id)
    else:
        await callback.message.answer("Это был последний вопрос. Квиз завершен!🎉")