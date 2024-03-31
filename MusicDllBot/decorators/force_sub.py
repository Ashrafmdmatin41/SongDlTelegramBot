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

from functools import wraps

from pyrogram.types import Message

from MusicDllBot import FORCE_SUB_CHANNEL


async def you_must_join(client, m):
    chat_info = await client.get_chat(FORCE_SUB_CHANNEL)
    JOIN_TEXT = ""
    if chat_info.username:
        JOIN_TEXT = f"Must join @{chat_info.username} to use this bot.\nJoin and start bot again."
    else:
        CHAT_NAME = chat_info.title
        JOIN_TEXT = f"Must join [{CHAT_NAME}]({chat_info.invite_link}) to use this bot.\nJoin and start bot again."
    await client.send_message(
        chat_id=m.chat.id,
        text=JOIN_TEXT,
        reply_to_message_id=m.id,
    )


def force_sub(func):
    @wraps(func)
    async def wrapper(client, message: Message, *args, **kwargs):
        members = [
            mem.user.id async for mem in client.get_chat_members(FORCE_SUB_CHANNEL)
        ]
        if message.from_user.id in members:
            return await func(client, message, *args, **kwargs)
        else:
            return await you_must_join(client, message, *args, **kwargs)

    return wrapper
