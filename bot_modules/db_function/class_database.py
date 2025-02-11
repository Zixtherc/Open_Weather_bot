import sqlite3 as sql

class Database():
    '''
    `Класс` , который позволит нам :
    - :mod:`Cоздавать` базу данных по `указанному` пути 
    - :mod:`Добавлять` юзеров в базу данных
    - :mod:`Cоздавать` задачи в базе данных по `указанным` параметрам 
    - :mod:`Извлекать` задачи из базы данных по `указанному` chat_id

    Пример использования :
    ```python
    db = Database('users.db')
    db.create_table()
    db.add_user(chat_id = 123456789, task = "Привет мир!", send_time = 1644051200)
    db.get_task(chat_id = 123456789)
    ```
    '''
    def __init__(self, path_to_db : str):
        self.db_path = path_to_db
        self.connection = sql.connect(self.db_path)
        self.cursor = self.connection.cursor()
    
    def create_table(self):
        request = '''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY ,
        chat_id INTEGER NOT NULL UNIQUE,
        task TEXT NOT NULL,
        send_time INTEGER NOT NULL)'''
        self.cursor.execute(request)
        self.connection.commit()
    def add_user(self, chat_id : int, task: str, send_time: int):
        request = '''INSERT INTO users (chat_id, task, send_time) VALUES (?, ?, ?)'''
        self.cursor.execute(request, (chat_id, task, send_time))
        self.connection.commit()
    
    def get_task(self, chat_id : int):
        request = '''SELECT * FROM users WHERE chat_id = ?'''
        self.cursor.execute(request, (chat_id,))
        return self.cursor.fetchone()
    
    def create_task(self, chat_id : int, task : str, send_time : int):
        request = '''SELECT * FROM users WHERE chat_id = ?'''
        self.cursor.execute(request, (chat_id,))
        user = self.cursor.fetchone()
        if user:
            insert_request = '''UPDATE users SET task = ?, send_time = ? WHERE chat_id = ?'''
            self.cursor.execute(insert_request, (task, send_time, chat_id))
            self.connection.commit()
            return True
        else:
            return False
        
db = Database(path_to_db = "bot_modules/db_function/database.db")