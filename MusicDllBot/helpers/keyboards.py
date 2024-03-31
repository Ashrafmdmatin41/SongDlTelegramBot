"""
Copyright (c) 2024 Minkxx

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

home_keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(text="Help", callback_data="help_data"),
            InlineKeyboardButton(text="About", callback_data="about_data"),
        ],
        [
            InlineKeyboardButton(
                text="Github Repo", url="https://github.com/minkxx/SongDlTelegramBot"
            )
        ],
        [InlineKeyboardButton(text="Close", callback_data="close_data")],
    ]
)

help_keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(text="Home", callback_data="home_data"),
            InlineKeyboardButton(text="About", callback_data="about_data"),
        ],
        [
            InlineKeyboardButton(
                text="Github Repo", url="https://github.com/minkxx/SongDlTelegramBot"
            )
        ],
        [InlineKeyboardButton(text="Close", callback_data="close_data")],
    ]
)

about_keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(text="Home", callback_data="home_data"),
            InlineKeyboardButton(text="Help", callback_data="help_data"),
        ],
        [
            InlineKeyboardButton(
                text="Github Repo", url="https://github.com/minkxx/SongDlTelegramBot"
            )
        ],
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
