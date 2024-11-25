from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


inline_buttons_s = [
    [InlineKeyboardButton(text="Get weather", callback_data = "weather"), InlineKeyboardButton(text="Button2", callback_data="button2")],
    [InlineKeyboardButton(text="Button3", callback_data = "button3"), InlineKeyboardButton(text="Button4", callback_data="button4")],
    [InlineKeyboardButton(text="Button5", callback_data = "button5")]
]


inline_buttons_forecast = [
    [InlineKeyboardButton(text = "Next", callback_data = "next")],
    [InlineKeyboardButton(text = "Back", callback_data = "back")]
]

# Создаем клавиатуры
inline_keyboard = InlineKeyboardMarkup(inline_keyboard = inline_buttons_s)
forecast_keyboard = InlineKeyboardMarkup(inline_keyboard = inline_buttons_forecast)
