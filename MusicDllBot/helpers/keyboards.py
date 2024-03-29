from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

home_keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(text="Help", callback_data="help_data"),
            InlineKeyboardButton(text="About", callback_data="about_data"),
        ],
        [InlineKeyboardButton(text="Github Repo", url="https://github.com/minkxx/SongDlTelegramBot")],
        [InlineKeyboardButton(text="Close", callback_data="close_data")],
    ]
)

help_keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(text="Home", callback_data="home_data"),
            InlineKeyboardButton(text="About", callback_data="about_data"),
        ],
        [InlineKeyboardButton(text="Github Repo", url="https://github.com/minkxx/SongDlTelegramBot")],
        [InlineKeyboardButton(text="Close", callback_data="close_data")],
    ]
)

about_keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(text="Home", callback_data="home_data"),
            InlineKeyboardButton(text="Help", callback_data="help_data"),
        ],
        [InlineKeyboardButton(text="Github Repo", url="https://github.com/minkxx/SongDlTelegramBot")],
        [InlineKeyboardButton(text="Close", callback_data="close_data")],
    ]
)

cancel_keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(text=f"❌ Cancel", callback_data=f"cancel_data"),
        ],
    ]
)
