from os.path import join, abspath

# Функция, которая позволяет нам возвращать абсолютный путь
def search_path(file_name : str): 
    '''
    :mod:`Функция`, которая позволяет нам возвращать абсолютный путь к указанному файлу.
    
    Вмещает в себя параметры:
    - :mod:`file_name`: имя файла, который нужно найти. Пример: "bot_modules/api_requests/request_news.py"

    Пример использования:
    ```python 
    path = search_path(file_name = "bot_modules/api_requests/request_news.py")
    ```
    >>> TERMINAL: C:\PROJECT VISUAL STUDIO CODE\Weather Tg Bot\bot_modules\keyboard
    '''
    # Создаёт абсолютный путь, начиная с текущей директории, звёдочка означает "распокавать данные", т.к метод split вовзарщает список
    # Мы распоковываем данные, и при помощи метода join, присоединяем 
    path = abspath(join(".", *file_name.split("/"))) 
    return path
