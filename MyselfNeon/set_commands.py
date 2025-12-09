# ------------------------------------------------
# File Name: Set_Commands.py
# Author: https://t.me/myselfneon
# Description: Auto Add Commands via /ncommands
# ------------------------------------------------

import asyncio
from pyrogram import Client, filters
from pyrogram.types import BotCommand, Message

# --- Edit This List ---
SET_COMMANDS = [
    ("start", "𝘊𝘩𝘦𝘤𝘬 𝘈𝘭𝘪𝘷𝘦 𝘚𝘵𝘢𝘵𝘶𝘴"),
    ("generate", "𝘎𝘦𝘯𝘦𝘳𝘢𝘵𝘦 𝘚𝘦𝘴𝘴𝘪𝘰𝘯 𝘚𝘵𝘳𝘪𝘯𝘨𝘴"),
    ("broadcast", "𝘉𝘳𝘰𝘢𝘥𝘤𝘢𝘴𝘵 𝘔𝘴𝘨𝘴 𝘵𝘰 𝘜𝘴𝘦𝘳𝘴")
]

# --- Internal Command Handler ---
@Client.on_message(filters.command("ncommands"))
async def sync_bot_commands(client: Client, message: Message):
    # 01. Notify User and Start Delay
    msg = await message.reply_text("***Initializing Command Refresh... Waiting 3 Seconds...***")
    
    # 02. Wait 3 Seconds as requested
    await asyncio.sleep(3)

    print("Checking Command Sync...")

    try:
        # 03. --- Format the Commands ---
        commands = [BotCommand(cmd, desc) for cmd, desc in SET_COMMANDS]

        # 04. --- Push to Telegram ---
        await client.set_bot_commands(commands)
        
        print(f"✅ Commands Synced with Telegram: {SET_COMMANDS}")
        
        # 05. --- Confirm Success ---
        await msg.edit_text("**✅ __Success !!\n🎉 Commands Updated Successfully.**\n👀 Close Telegram and Return back to see Changes. - by <a href="t.me/myselfneon">**@MyselfNeon**</a>__")
        
    except Exception as e:
        print(f"✗ Failed to Sync Commands: {e}")
        await msg.edit_text(f"**🚫 __Error Updating Commands:***\n{e}__")

