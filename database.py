import aiosqlite
from config import DB_NAME

async def create_table():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''CREATE TABLE IF NOT EXISTS quiz_state 
                          (user_id INTEGER PRIMARY KEY, question_index INTEGER, right_answer INTEGER, wrong_answer INTEGER)''')
        await db.commit()

async def get_quiz_index(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT question_index FROM quiz_state WHERE user_id = (?)', (user_id,)) as cursor:
            results = await cursor.fetchone()
            return results[0] if results is not None else 0

async def get_quiz_right_answer(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT right_answer FROM quiz_state WHERE user_id = (?)', (user_id,)) as cursor:
            results = await cursor.fetchone()
            return results[0] if results is not None else 0

async def get_quiz_wrong_answer(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT wrong_answer FROM quiz_state WHERE user_id = (?)', (user_id,)) as cursor:
            results = await cursor.fetchone()
            return results[0] if results is not None else 0

async def update_quiz_index(user_id, index, right_answer, wrong_answer):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('INSERT OR REPLACE INTO quiz_state (user_id, question_index, right_answer, wrong_answer) VALUES (?, ?, ?, ?)', 
                        (user_id, index, right_answer, wrong_answer))
        await db.commit()