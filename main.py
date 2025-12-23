# ---------------------------------------------------
# File Name: Main.py
# Author: NeonAnurag
# GitHub: https://github.com/MyselfNeon/
# Telegram: https://t.me/MyelfNeon
# Created: 2025-11-21
# Last Modified: 2025-11-22
# Version: Latest
# License: MIT License
# ---------------------------------------------------

from pyrogram import Client, filters
from config import API_ID, API_HASH, BOT_TOKEN, LOG_CHANNEL, KEEP_ALIVE_URL
import datetime
from datetime import timezone, timedelta  # ✅ Added for IST
import asyncio
import aiohttp
import logging

# ✅ Indian Standard Time
IST = timezone(timedelta(hours=5, minutes=30))

class Bot(Client):
    def __init__(self):
        super().__init__(
            "Neon String Session Bot",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            plugins=dict(root="MyselfNeon"),
            workers=150,
            sleep_threshold=10
        )
        self.username = None  # will be set on start

    async def start(self):
        await super().start()
        me = await self.get_me()
        self.username = '@' + me.username
        print('Bot Started Powered By @NeonFiles')

        # ✅ Start keep-alive task
        asyncio.create_task(keep_alive())

        # Send restart log
        await self.send_restart_log()

    async def stop(self, *args):
        await super().stop()
        print('Bot Stopped Bye')

    async def send_restart_log(self):
        now = datetime.datetime.now(IST)  # ✅ Using IST
        date = now.strftime("%d/%m/%y")   # ✅ Adjusted to match your format
        time = now.strftime("%I:%M:%S %p") # ✅ Adjusted to match your format
        text = (
            f"⌬ Restarted Successfully!\n"
            f"┟ Date: {date}\n"
            f"┠ Time: {time}\n"
            f"┠ TimeZone: Asia/Kolkata\n"
            f"┖ Version: v3.0.8-x"
        )
        try:
            await self.send_message(LOG_CHANNEL, text)
        except Exception as e:
            print(f"Restart log failed: {e}")

# ✅ Keep Alive Function
async def keep_alive():
    """Send a request every 100 seconds to keep the bot alive (if required)."""
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                await session.get(KEEP_ALIVE_URL)
                logging.info("Sent keep-alive request.")
            except Exception as e:
                logging.error(f"Keep-alive request failed: {e}")
            await asyncio.sleep(100)

# --- HANDLERS ---
# Handle /start and new user logging (no DB dependency)
@Bot.on_message(filters.private & filters.command("start"))
async def start_cmd(client, message):
    user_id = message.from_user.id
    user_name = message.from_user.mention

    # Send new user log
    now = datetime.datetime.now(IST)  # ✅ Using IST
    text = (
        "<b>#NewUser</b>\n"
        f"<b><i>@NeonSessionBot</i></b>\n\n"
        f"<b>🆔 <i>Usᴇʀ ID :</i></b> <code>{user_id}</code>\n"
        f"<b>👤 <i>Usᴇʀ : {user_name}</i></b>\n"
        f"<b>📆 <i>Dᴀᴛᴇ :</b> {now.strftime('%d-%b-%Y')}</i>\n"
        f"<b>⏰ <i>Tɪᴍᴇ :</b> {now.strftime('%I:%M %p')}</i>"
    )
    try:
        await client.send_message(LOG_CHANNEL, text)
    except Exception as e:
        print(f"New user log failed: {e}")

    await message.reply("Hey! You started me 🎉")

# Run the bot
Bot().run()


# MyselfNeon
# Don't Remove Credit 🥺
# Telegram Channel @NeonFiles
