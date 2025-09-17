from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram import types
from quiz_data import quiz_data

def generate_options_keyboard(answer_options, right_answer):
    builder = InlineKeyboardBuilder()
    
    for option in answer_options:
        builder.add(types.InlineKeyboardButton(
            text=option,
            callback_data="right_answer" if option == right_answer else "wrong_answer")
        )
    
    builder.adjust(1)
    return builder.as_markup()

def generate_start_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Начать игру"))
    return builder.as_markup(resize_keyboard=True)

def generate_stats_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Статистика"))
    return builder.as_markup(resize_keyboard=True)