#Main.py
from pyrogram import Client, filters
from config import API_ID, API_HASH, BOT_TOKEN, LOG_CHANNEL
import datetime

class Bot(Client):
    def __init__(self):
        super().__init__(
            "Neon String Session Bot",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            plugins=dict(root="Neon"),
            workers=150,
            sleep_threshold=10
        )

    async def start(self):
        await super().start()
        me = await self.get_me()
        self.username = '@' + me.username
        print('Bot Started Powered By @NeonFiles')

        # Send restart log
        await self.send_restart_log(me.first_name)

    async def stop(self, *args):
        await super().stop()
        print('Bot Stopped Bye')

    async def send_restart_log(self, me_name):
        now = datetime.datetime.now()
        date = now.strftime("%d-%m-%Y")
        time = now.strftime("%H:%M:%S")
        text = (
            f"<b><i>{me_name} is Up ✅</b></i>\n"
            f"<b>📅 <i>Dᴀᴛᴇ: {date}</b></i>\n"
            f"<b>⏰ <i>Tɪᴍᴇ: {time}</b></i>"
        )
        try:
            await self.send_message(LOG_CHANNEL, text)
        except Exception as e:
            print(f"Restart log failed: {e}")

# Handle /start and new user logging (no DB dependency)
@Bot.on_message(filters.private & filters.command("start"))
async def start_cmd(client, message):
    user_id = message.from_user.id
    user_name = message.from_user.mention

    # Send new user log
    now = datetime.datetime.now()
    text = (
        "<b>#NewUser</b>\n"
        f"<b><i>@NeonSessionBot</i></b>\n\n"
        f"<b>🆔 <i>Usᴇʀ ID:</i></b> <code>{user_id}</code>\n"
        f"<b>👤 <i>Usᴇʀ: {user_name}</i></b>\n"
        f"<b>📆 <i>Dᴀᴛᴇ: {now.strftime('%d-%m-%Y')}</i></b>\n"
        f"<b>⏰ <i>Tɪᴍᴇ: {now.strftime('%H:%M:%S')}</b></i>"
    )
    try:
        await client.send_message(LOG_CHANNEL, text)
    except Exception as e:
        print(f"New user log failed: {e}")

    await message.reply("Hey! You started me 🎉")

# Run the bot
Bot().run()
