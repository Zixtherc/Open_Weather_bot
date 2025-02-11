import aiosqlite as async_sql

class Database:
    '''### Класс базы данных ###'''
    def __init__(self, path_to_db: str):
        '''
        `Метод` конструктор, который принимает в себя `параметры`:
        -:mod:`path_to_db`: Путь где будет создана база данных
        '''
        self.db_path = path_to_db
    async def create_table(self):
        '''
        `Метод`, который создает таблицу в базе данных

        Пример использования:
        ```python 
        db.create_table()
        ```
        '''
        # Используем конструкцию `with`, которая автоматически откроет и закроет соединение, предотвращая утечки ресурсов и возможные ошибки
        async with async_sql.connect(self.db_path) as db:
            # Выполняем запрос
            await db.execute(
                '''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                chat_id INTEGER NOT NULL UNIQUE,
                task TEXT NOT NULL,
                send_time INTEGER NOT NULL)''')
            await db.commit()
    async def add_user(self, chat_id: int, task: str, send_time: int):
        '''
        `Метод`, который добавляет `нового` пользователя в базу данных
        
        Принимает в себя параметры:
        - :mod:`chat_id`: ID чата
        - :mod:`task`: Задача
        - :mod:`send_time`: Время отправки
        
        Пример использования:
        ```python
        db.add_user(chat_id = 123, tast = "Hello", send_time 11.02 22:31)
        ```
        '''
        async with async_sql.connect(self.db_path) as db:
            await db.execute(
                '''INSERT INTO users (chat_id, task, send_time) VALUES (?, ?, ?)'''), (chat_id, task, send_time)
            await db.commit()

    async def get_task(self, chat_id: int):
        '''
        `Метод`, который получает задачу пользователя из базы данных
        
        Принимает в себя параметры:
        - :mod:`chat_id`: ID чата
        
        Пример использования:
        ```python 
        db.get_task(chat_id = 123)
        ```'''
        async with async_sql.connect(self.db_path) as db:
            async with db.execute('''SELECT * FROM users WHERE chat_id = ?''', (chat_id,)) as cursor:
                # Возвращаем только одного ( и так вернётся лишь один, т.к у нас chat_id уникальный параметр)
                return await cursor.fetchone()
    async def add_note(self, chat_id: int, task: str, send_time: int):
        '''
        `Метод`, который добавляет заметку в базу данных
        
        Принимает в себя параметры:
        - :mod:`chat_id`: ID чата
        
        Пример использования:
        ```python
        db.add_note(chat_id = 123)
        '''
        async with async_sql.connect(self.db_path) as db:
            async with db.execute('''SELECT * FROM users WHERE chat_id = ?''', (chat_id,)) as cursor:
                user = cursor.fetchone()
                # Проверка что такой пользователь существует
                if user:
                    await db.execute('''UPDATE users SET task = ?, send_time = ? WHERE chat_id = ?''')
                    await db.commit()
                    # Возвращаем True, если пользователь был найден, и данные обновленны
                    return True
                # Если пользователь не найден,возвращаем False
                return False
            
# Объект от класса Database
db = Database(path_to_db = "bot_modules/db_function/database.db")