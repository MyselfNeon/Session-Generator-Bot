#Broadcast.py
from pyrogram.errors import InputUserDeactivated, UserNotParticipant, FloodWait, UserIsBlocked, PeerIdInvalid
from Neon.db import db
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
        return await message.reply_text("**📢 Reply This Command To Your Broadcast Msg**")

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
                f"**📢 --Bʀᴏᴀᴅᴄᴀsᴛ Iɴ Pʀᴏɢʀᴇss--**\n\n"
                f"👥 Total Users: {total_users}\n"
                f"✅ Completed: {done}/{total_users}\n"
                f"💖 Success: {success}\n"
                f"🚫 Blocked: {blocked}\n"
                f"🗑️ Deleted: {deleted}\n"
                f"❌ Failed: {failed}"
            )

    time_taken = datetime.timedelta(seconds=int(time.time() - start_time))
    await sts.edit(
        f"**📢 --Bʀᴏᴀᴅᴄᴀsᴛ Cᴏᴍᴘʟᴇᴛᴇᴅ--**\n\n"
        f"⏰ Completed in {time_taken}\n\n"
        f"👥 Total Users: {total_users}\n"
        f"✅ Completed: {done}/{total_users}\n"
        f"💖 Success: {success}\n"
        f"❌ Blocked: {blocked}\n"
        f"🗑️ Deleted: {deleted}\n"
        f"⚠️ Failed: {failed}"
        )


# Dont remove Credits
# Developer Telegram @MyselfNeon
# Update channel - @NeonFiles
