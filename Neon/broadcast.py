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


@Client.on_message(filters.command("broadcast") & filters.user(OWNER_ID) & filters.reply)
async def verupikkals(bot, message):
    users = await db.get_all_users()
    b_msg = message.reply_to_message
    if not b_msg:
        return await message.reply_text("**__Rᴇᴘʟʏ Tʜɪs Cᴏᴍᴍᴀɴᴅ Tᴏ Yᴏᴜʀ Bʀᴏᴀᴅᴄᴀsᴛ Mᴇssᴀɢᴇ__**")
    sts = await message.reply_text(
        text='**📢 __Bʀᴏᴀᴅᴄᴀsᴛɪɴɢ Yᴏᴜʀ Mᴇssᴀɢᴇs__**'
    )
    start_time = time.time()
    total_users = await db.total_users_count()
    done = 0
    blocked = 0
    deleted = 0
    failed =0

    success = 0
    async for user in users:
        if 'id' in user:
            pti, sh = await broadcast_messages(int(user['id']), b_msg)
            if pti:
                success += 1
            elif pti == False:
                if sh == "Blocked":
                    blocked += 1
                elif sh == "Deleted":
                    deleted += 1
                elif sh == "Error":
                    failed += 1
            done += 1
            if not done % 20:
                await sts.edit(f"**📢 __Bʀᴏᴀᴅᴄᴀsᴛ Iɴ Pʀᴏɢʀᴇss__**:\n\n**👥 __Tᴏᴛᴀʟ Usᴇʀs__**: {total_users}\n**✅ __Cᴏᴍᴘʟᴇᴛᴇᴅ__**: {done} / {total_users}\n**💖 __Sᴜᴄᴄᴇss__**: {success}\n**❌ __Bʟᴏᴄᴋᴇᴅ__**: {blocked}\n**🗑️ __Dᴇʟᴇᴛᴇᴅ__**: {deleted}")    
        else:
            # Handle the case where 'id' key is missing in the user dictionary
            done += 1
            failed += 1
            if not done % 20:
                await sts.edit(f"**📢 __Bʀᴏᴀᴅᴄᴀsᴛ Iɴ Pʀᴏɢʀᴇss__**:\n\n**👥 __Tᴏᴛᴀʟ Usᴇʀs__**: {total_users}\n**✅ __Cᴏᴍᴘʟᴇᴛᴇᴅ__**: {done} / {total_users}\n**💖__Sᴜᴄᴄᴇss__**: {success}\n**❌ __Bʟᴏᴄᴋᴇᴅ__**: {blocked}\n**🗑️ __Dᴇʟᴇᴛᴇᴅ__**: {deleted}")
    
    time_taken = datetime.timedelta(seconds=int(time.time()-start_time))
    await sts.edit(f"**📢 __Bʀᴏᴀᴅᴄᴀsᴛ Cᴏᴍᴘʟᴇᴛᴇᴅ__**:\n\n**⏰ __Cᴏᴍᴘʟᴇᴛᴇᴅ Iɴ {time_taken} Sᴇᴄᴏɴᴅs__**.\n\n**👥 __Tᴏᴛᴀʟ Usᴇʀs__**: {total_users}\n**✅ __Cᴏᴍᴘʟᴇᴛᴇᴅ__**: {done} / {total_users}\n**💖 __Sᴜᴄᴄᴇss__**: {success}\n**❌ __Bʟᴏᴄᴋᴇᴅ__**: {blocked}\n**🗑️ __Dᴇʟᴇᴛᴇᴅ__**: {deleted}")
