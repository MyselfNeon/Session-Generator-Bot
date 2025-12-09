# ------------------------------------------------
# File Name: Set_Commands.py
# Author: https://t.me/myselfneon
# Description: Auto Add Commands via /ncommands (Owner Only)
# ------------------------------------------------

import asyncio
from config import OWNER_ID
from pyrogram import Client, filters
from pyrogram.types import BotCommand, Message

# --- Edit This List ---
SET_COMMANDS = [
    ("start", "𝘊𝘩𝘦𝘤𝘬 𝘈𝘭𝘪𝘷𝘦 𝘚𝘵𝘢𝘵𝘶𝘴"),
    ("help", "𝘏𝘰𝘸 𝘵𝘰 𝘜𝘴𝘦 𝘔𝘦"),
    ("login", "𝘓𝘰𝘨𝘪𝘯 𝘠𝘰𝘶𝘳 𝘛𝘦𝘭𝘦𝘨𝘳𝘢𝘮 𝘚𝘦𝘴𝘴𝘪𝘰𝘯"),
    ("logout", "𝘓𝘰𝘨𝘰𝘶𝘵 𝘠𝘰𝘶𝘳 𝘚𝘦𝘴𝘴𝘪𝘰𝘯"),
    ("cancel", "𝘊𝘢𝘯𝘤𝘦𝘭 𝘢𝘯𝘺 𝘖𝘯𝘨𝘰𝘪𝘯𝘨 𝘛𝘢𝘴𝘬"),
    ("users", "𝘊𝘩𝘦𝘤𝘬 𝘛𝘰𝘵𝘢𝘭 𝘜𝘴𝘦𝘳𝘴 (𝘈𝘥𝘮𝘪𝘯)"),
    ("broadcast", "𝘉𝘳𝘰𝘢𝘥𝘤𝘢𝘴𝘵 𝘔𝘴𝘨𝘴 𝘵𝘰 𝘜𝘴𝘦𝘳𝘴 (𝘈𝘥𝘮𝘪𝘯)")
]

# --- Internal Command Handler ---
@Client.on_message(filters.command("ncommands") & filters.user(OWNER_ID))
async def sync_bot_commands(client: Client, message: Message):

    msg = await message.reply_text("**⏱️ __Wait 3 Seconds while I load your Commands through plugin System.__**")
    
    for i in range(2, 0, -1):
        await asyncio.sleep(1)
        try:
            await msg.edit_text(f"**⏱️ __Wait {i} Seconds while I load your Commands through plugin System.__**")
        except:
            pass
            
    await asyncio.sleep(1)

    print("Checking Command Sync...")

    try:
  
        commands = [BotCommand(cmd, desc) for cmd, desc in SET_COMMANDS]

        await client.set_bot_commands(commands)
        
        print(f"✅ Commands Synced with Telegram: {SET_COMMANDS}")
        
        # --- Confirm Success ---
        await msg.edit_text("**✅ __Success !!\n🎉 Commands Updated Successfully.__**\n👀 **__Close Telegram and Return back to see Changes. - by @MyselfNeon 🆘__**")
        
    except Exception as e:
        print(f"✗ Failed to Sync Commands: {e}")
        await msg.edit_text(f"**🚫 __Error Updating Commands:__**\n`{e}`")

  
