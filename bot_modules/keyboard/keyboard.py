from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


inline_buttons_s = [
    [InlineKeyboardButton(text="Get weather", callback_data = "weather"), InlineKeyboardButton(text="Get news", callback_data="news")],
    [InlineKeyboardButton(text="Calendar", callback_data = "calendar"), InlineKeyboardButton(text="Button4", callback_data="button4")],
    [InlineKeyboardButton(text="Diary", callback_data = "diary")]
]


inline_buttons_forecast = [
    [InlineKeyboardButton(text = "Next", callback_data = "next")],
    [InlineKeyboardButton(text = "Back", callback_data = "back")]
]
inline_buttons_news =[
    [InlineKeyboardButton(text = "Next", callback_data = "next_news")],
    [InlineKeyboardButton(text = "Back", callback_data = "back_news")]
]

# Создаем клавиатуры
inline_keyboard = InlineKeyboardMarkup(inline_keyboard = inline_buttons_s)
forecast_keyboard = InlineKeyboardMarkup(inline_keyboard = inline_buttons_forecast)
news_keyboard = InlineKeyboardMarkup(inline_keyboard = inline_buttons_news)