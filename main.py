# main.py
from pyrogram import Client, filters
from config import API_ID, API_HASH, BOT_TOKEN, LOG_CHANNEL, KEEP_ALIVE_URL
from MyselfNeon.keep_alive_plugin import init_keep_alive  # ✅ Import plugin
import datetime
from datetime import timezone, timedelta
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
        self.username = None

    async def start(self):
        await super().start()
        me = await self.get_me()
        self.username = '@' + me.username

        # ✅ Load monitor plugin before doing anything else
        await init_keep_alive(self)

        print('Bot Started Powered By @NeonFiles')

        # ✅ Start the internal keep-alive pinger
        asyncio.create_task(keep_alive())

        # Log restart event
        await self.send_restart_log()

    async def stop(self, *args):
        await super().stop()
        print('Bot Stopped Bye')

    async def send_restart_log(self):
        now = datetime.datetime.now(IST)
        date = now.strftime("%d-%b-%Y")
        time = now.strftime("%I:%M %p")
        text = (
            f"<b>🤖 <i>Bot Deployed / Restarted ♻️</b></i>\n"
            f"<i><b>- {self.username}</i></b>\n\n"
            f"<b>- <i>Dᴀᴛᴇ :</b> {date}</i>\n"
            f"<b>- <i>Tɪᴍᴇ :</b> {time}</i>\n"
            f"**- __@neonfiles__**"
        )
        try:
            await self.send_message(LOG_CHANNEL, text)
        except Exception as e:
            print(f"Restart log failed: {e}")

# ✅ Keep Alive Function
async def keep_alive():
    """Send a request every 300 seconds to keep the bot alive (if required)."""
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                await session.get(KEEP_ALIVE_URL)
                logging.info("Sent keep-alive request.")
            except Exception as e:
                logging.error(f"Keep-alive request failed: {e}")
            await asyncio.sleep(300)

# Handle /start and new user logging (no DB dependency)
@Bot.on_message(filters.private & filters.command("start"))
async def start_cmd(client, message):
    user_id = message.from_user.id
    user_name = message.from_user.mention
    now = datetime.datetime.now(IST)
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
