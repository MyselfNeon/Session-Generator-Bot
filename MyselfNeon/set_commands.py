# ------------------------------------------------
# File Name: Set_Commands.py
# Description: Auto Add Commands via /ncommands
# ------------------------------------------------

import asyncio
from pyrogram import Client, filters
from pyrogram.types import BotCommand, Message

# --- Edit This List ---
SET_COMMANDS = [
    ("start", "Check Alive Status"),
    ("generate", "Generate Session Strings"),
    ("broadcast", "Broadcast Msgs to Users")
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
        
        print(f"✓ Commands Synced with Telegram: {SET_COMMANDS}")
        
        # 05. --- Confirm Success ---
        await msg.edit_text("***✓ Success! Bot Commands Updated via Plugin.***")
        
    except Exception as e:
        print(f"✗ Failed to Sync Commands: {e}")
        await msg.edit_text(f"***✗ Error Updating Commands:***\n`{e}`")
