import aiosqlite

DB_NAME = 'quiz_bot.db'

async def create_table():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''CREATE TABLE IF NOT EXISTS quiz_state (
                                user_id INTEGER PRIMARY KEY, 
                                question_index INTEGER
                            )''')
        await db.execute('''CREATE TABLE IF NOT EXISTS quiz_results (
                                user_id INTEGER PRIMARY KEY, 
                                correct_answers INTEGER
                            )''')
        await db.commit()

async def get_quiz_index(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT question_index FROM quiz_state WHERE user_id = ?', (user_id,)) as cursor:
            results = await cursor.fetchone()
            if results is not None:
                return results[0]
            else:
                return 0

async def update_quiz_index(user_id, index):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('INSERT OR REPLACE INTO quiz_state (user_id, question_index) VALUES (?, ?)', (user_id, index))
        await db.commit()

async def get_user_stats(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT correct_answers FROM quiz_results WHERE user_id = ?', (user_id,)) as cursor:
            result = await cursor.fetchone()
            if result:
                return result[0]
            else:
                return None

async def save_quiz_result(user_id, correct_answers):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('INSERT OR REPLACE INTO quiz_results (user_id, correct_answers) VALUES (?, ?)', 
                         (user_id, correct_answers))
        await db.commit()
