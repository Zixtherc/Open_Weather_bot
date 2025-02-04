import asyncio
from googletrans import Translator

async def my_translate(text: str, lang: str = 'ru'):
    translator = Translator()
    translation = await translator.translate(text, dest=lang)
    print(translation.text)

asyncio.run(my_translate(text = "hello world"))