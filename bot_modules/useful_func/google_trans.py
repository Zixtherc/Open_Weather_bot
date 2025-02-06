r'''
:mod:`Модуль` который вмещает в себя `функцию` перевода текста
'''
# Необходимый импорт Класса 
from googletrans import Translator

async def my_translate(text: str, lang: str = 'ru'):
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
    # Создаём объект класса от Translator
    translator = Translator()
    # Выполняем перевод текста с одного языка на другой
    translation = await translator.translate(text, dest=lang)
    # Выводим переведенный текст
    print(translation.text)
    # Возвращаем переведенный текст для дальнейшего использования
    return translation