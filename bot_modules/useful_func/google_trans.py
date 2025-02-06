r'''
:mod:`Модуль` который вмещает в себя `функцию` перевода текста
'''
# Необходимый импорт Класса 
from deep_translator import GoogleTranslator

def my_translate(text: str, lang: str = 'ru'):
    '''
    :mod:`Функция`, которая вмещает в себя параметры:
    - :mod:`text`: для текста который мы будем переводить
    - :mod:`lang`: язык на который мы хотим перевести текст (по умолчанию 'ru')

    Пример использования : 
    ```python 
    translation = my_translate(text = "Hello, world!", lang = "ru")
    print(translation)
    ```
    TERMINAL > Привет, мир!
    '''
    translation = GoogleTranslator(source = "auto", target = lang).translate(text = text)
    return translation