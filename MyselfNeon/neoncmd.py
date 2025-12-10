# ------------------------------------------------
# File Name: NeonCommands.py
# Author: https://t.me/myselfneon
# Description: Auto Add Commands via /neoncmd (Owner Only)
# ------------------------------------------------

import asyncio
from config import OWNER_ID
from pyrogram import Client, filters
from pyrogram.types import BotCommand, Message

# --- Edit This List (Text Format) ---
COMMAND_BLOCK = """
[
start - 𝘊𝘩𝘦𝘤𝘬 𝘈𝘭𝘪𝘷𝘦 𝘚𝘵𝘢𝘵𝘶𝘴
generate - 𝘎𝘦𝘯𝘦𝘳𝘢𝘵𝘦 𝘚𝘦𝘴𝘴𝘪𝘰𝘯 𝘚𝘵𝘳𝘪𝘯𝘨𝘴
broadcast - 𝘉𝘳𝘰𝘢𝘥𝘤𝘢𝘴𝘵 𝘔𝘴𝘨𝘴 𝘵𝘰 𝘜𝘴𝘦𝘳𝘴
]
"""

# --- Internal Command Handler ---
@Client.on_message(filters.command("neoncmd") & filters.user(OWNER_ID))
async def sync_bot_commands(client: Client, message: Message):

    msg = await message.reply_text("**⏱️ __Wait 3 Seconds while I load your Commands through plugin System.__**")
    
    # Countdown
    for i in range(2, 0, -1):
        await asyncio.sleep(1)
        try:
            await msg.edit_text(f"**⏱️ __Wait {i} Seconds while I load your Commands through plugin System.__**")
        except:
            pass
            
    await asyncio.sleep(1)

    print("Checking Command Sync...")

    try:
        # --- Parse The Text Block ---
        commands = []
        for line in COMMAND_BLOCK.strip().split("\n"):
            # Clean Up Line
            line = line.strip()
            
            if line in ["[", "]"] or not line:
                continue
                
            if "-" in line:
                cmd, desc = line.split("-", 1)
                commands.append(BotCommand(cmd.strip(), desc.strip()))

        # --- Push to Telegram ---
        await client.set_bot_commands(commands)
        
        print(f"✅ Commands Synced with Telegram: {len(commands)} commands set.")
        
        # --- Confirm Success ---
        await msg.edit_text("**✅ __Success !!\n🎉 Commands Updated Successfully.__**\n👀 **__Close Telegram and Return back to see Changes. - by @MyselfNeon 🆘__**")
        
    except Exception as e:
        print(f"✗ Failed to Sync Commands: {e}")
        await msg.edit_text(f"**🚫 __Error Updating Commands:__**\n`{e}`")
        
