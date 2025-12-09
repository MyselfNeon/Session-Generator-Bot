# ---------------------------------------------------
# File Name: Broadcast.py
# Author: NeonAnurag
# GitHub: https://github.com/MyselfNeon/
# Telegram: https://t.me/MyelfNeon
# Created: 2025-11-21
# Last Modified: 2025-11-22
# Version: Latest
# License: MIT License
# ---------------------------------------------------

from pyrogram.errors import InputUserDeactivated, UserNotParticipant, FloodWait, UserIsBlocked, PeerIdInvalid
from pyrogram.types import BotCommand, Message
from MyselfNeon.db import db
from pyrogram import Client, filters
from config import OWNER_ID
import asyncio
import datetime
import time

async def broadcast_messages(user_id, message):
    try:
        await message.copy(chat_id=user_id)
        return True, "Success"
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return await broadcast_messages(user_id, message)
    except InputUserDeactivated:
        await db.delete_user(int(user_id))
        return False, "Deleted"
    except UserIsBlocked:
        await db.delete_user(int(user_id))
        return False, "Blocked"
    except PeerIdInvalid:
        await db.delete_user(int(user_id))
        return False, "Error"
    except Exception as e:
        return False, "Error"


@Client.on_message(filters.command("broadcast") & filters.user(OWNER_ID))
async def verupikkals(bot, message):
    b_msg = message.reply_to_message
    if not b_msg:
        return await message.reply_text("**__Reply This Command To Your Msg you Needed to Broadcast__ ✅**",quote=True)

    users = await db.get_all_users()
    sts = await message.reply_text("**📢 __Bʀᴏᴀᴅᴄᴀsᴛɪɴɢ Yᴏᴜʀ Mᴇssᴀɢᴇs__**")
    start_time = time.time()
    total_users = await db.total_users_count()

    done = 0
    success = 0
    blocked = 0
    deleted = 0
    failed = 0

    async for user in users:
        if 'id' in user:
            pti, sh = await broadcast_messages(int(user['id']), b_msg)
            if pti:
                success += 1
            else:
                if sh == "Blocked":
                    blocked += 1
                elif sh == "Deleted":
                    deleted += 1
                elif sh == "Error":
                    failed += 1
            done += 1
        else:
            done += 1
            failed += 1

        # Update progress every 10 users for smoother feedback
        if done % 10 == 0 or done == total_users:
            await sts.edit(
                f"**📢 --__Broadcast In Progress__--**\n\n"
                f"**👥 __Total Users: {total_users}__**\n"
                f"**✅ __Completed: {done}/{total_users}__**\n"
                f"**💖 __Success: {success}__**\n"
                f"**🚫 __Blocked: {blocked}__**\n"
                f"**🗑️ __Deleted: {deleted}__**\n"
                f"**❌ __Failed: {failed}__**"
            )

    time_taken = datetime.timedelta(seconds=int(time.time() - start_time))
    await sts.edit(
        f"**📢 --__Broadcast Completed__--**\n\n"
        f"**⏰ __Completed in {time_taken}__**\n\n"
        f"**👥 __Total Users: {total_users}__**\n"
        f"**✅ __Completed: {done}/{total_users}__**\n"
        f"**💖 __Success: {success}__**\n"
        f"**❌ __Blocked: {blocked}__**\n"
        f"**🗑️ __Deleted: {deleted}__**\n"
        f"**⚠️ __Failed: {failed}__**"
        )

# -------------------------------------
# --- Edit This List ---
SET_COMMANDS = [
    ("start", "𝘊𝘩𝘦𝘤𝘬 𝘈𝘭𝘪𝘷𝘦 𝘚𝘵𝘢𝘵𝘶𝘴"),
    ("generate", "𝘎𝘦𝘯𝘦𝘳𝘢𝘵𝘦 𝘚𝘦𝘴𝘴𝘪𝘰𝘯 𝘚𝘵𝘳𝘪𝘯𝘨𝘴"),
    ("broadcast", "𝘉𝘳𝘰𝘢𝘥𝘤𝘢𝘴𝘵 𝘔𝘴𝘨𝘴 𝘵𝘰 𝘜𝘴𝘦𝘳𝘴")
]

# --- Internal Command Handler ---
@Client.on_message(filters.command("neoncmd"))
async def sync_bot_commands(client: Client, message: Message):
    msg = await message.reply_text("**⏱️ __Wait 3 Seconds while I load your Commands through plugin System.__**")
    
    # 01. Real-time Countdown Loop
    for i in range(2, 0, -1):
        await asyncio.sleep(1)
        try:
            await msg.edit_text(f"**⏱️ __Wait {i} Seconds while I load your Commands through plugin System.__**")
        except:
            pass
            
    await asyncio.sleep(1)

    print("Checking Command Sync...")

    try:
        # 02. --- Format the Commands ---
        commands = [BotCommand(cmd, desc) for cmd, desc in SET_COMMANDS]

        # 03. --- Push to Telegram ---
        await client.set_bot_commands(commands)
        
        print(f"✅ Commands Synced with Telegram: {SET_COMMANDS}")
        
        # 05. --- Confirm Success ---
        await msg.edit_text("**✅ __Success !!\n🎉 Commands Updated Successfully.__**\n👀 **__Close Telegram and Return back to see Changes. - by @MyselfNeon 🆘__**")
        
    except Exception as e:
        print(f"❌ Failed to Sync Commands: {e}")
        await msg.edit_text(f"**🚫 __Error Updating Commands:__**\n`{e}`")


# Dont remove Credits
# Developer Telegram @MyselfNeon
# Update channel - @NeonFiles
