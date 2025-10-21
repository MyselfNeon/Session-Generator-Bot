# broadcast.py
from pyrogram.errors import InputUserDeactivated, UserNotParticipant, FloodWait, UserIsBlocked, PeerIdInvalid
from Neon.db import db
from pyrogram import Client, filters
from config import OWNER_ID
import asyncio
import datetime
import time
from pyrogram.types import Message
import json
import tempfile
import os

# ─────────────────────────────
# Broadcast helper function
# ─────────────────────────────
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
    except Exception:
        return False, "Error"

# ─────────────────────────────
# /broadcast command
# ─────────────────────────────
@Client.on_message(filters.command("broadcast") & filters.user(OWNER_ID))
async def verupikkals(bot, message):
    b_msg = message.reply_to_message
    if not b_msg:
        return await message.reply_text(
            "**__Reply This Command To Your Msg you Needed to Broadcast__ ✅**",
            quote=True
        )

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


# ─────────────────────────────
# /users Command (Standalone + JSON export)
# ─────────────────────────────
@Client.on_message(filters.command("users") & filters.user(OWNER_ID))
async def users_count(client: Client, message: Message):
    """Shows total registered users and sends a JSON file of all users."""
    msg = await message.reply_text("⏳ Gathering user data...", quote=True)

    try:
        # 1) Count total users
        total = await db.total_users_count()
        await msg.edit_text(f"👥 Total Registered Users: {total}\n⏳ Generating JSON file...")

        # 2) Fetch all users
        users_cursor = await db.get_all_users()
        users_list = []
        async for user in users_cursor:
            users_list.append({
                "id": user.get("id"),
                "name": user.get("name", "None")
            })

        # 3) Write users to a temporary JSON file
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        tmp_path = tmp.name
        try:
            with open(tmp_path, "w", encoding="utf-8") as f:
                json.dump(users_list, f, indent=2, ensure_ascii=False)
        finally:
            tmp.close()

        # 4) Send JSON file to the admin
        await message.reply_document(
            document=tmp_path,
            caption=f"📄 Recorded {len(users_list)} Users",
            quote=True
        )

        # 5) Clean up temp file
        try:
            os.remove(tmp_path)
        except Exception as e:
            print(f"[!] Failed to delete temp file {tmp_path}: {e}")

        # 6) Update original message
        await msg.edit_text(f"✅ Successfully fetched {total} users and sent the JSON file.")

    except Exception as e:
        await msg.edit_text(f"⚠️ Error fetching user data:\n<code>{e}</code>")
        print(f"[!] /users error: {e}")


# Dont remove Credits
# Developer Telegram @MyselfNeon
# Update channel - @NeonFiles
