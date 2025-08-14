from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from config import OWNER_ID, F_SUB
from Neon.db import db

# Replace with your actual custom links
MY_CUSTOM_LINKS = {
    "BotRepoLink": "https://github.com/MyselfNeon/YourBotRepo"
}

@Client.on_message(filters.private & filters.incoming & filters.command("start"))
async def start(bot: Client, msg: Message):
    args = msg.text.split(maxsplit=1)

    # Handle deep-link parameter
    if len(args) > 1:
        key = args[1]
        if key in MY_CUSTOM_LINKS:
            await msg.reply_text(f"**__Hᴇʀᴇ's Yᴏᴜʀ Lɪɴᴋ__**:\n {MY_CUSTOM_LINKS[key]}")
            return
        else:
            await msg.reply_text(f"You started me with: {key}")
            return

    if not await db.is_user_exist(msg.from_user.id):
        await db.add_user(msg.from_user.id, msg.from_user.first_name)

    if F_SUB:
        try:
            await bot.get_chat_member(int(F_SUB), msg.from_user.id)
        except:
            try:
                invite_link = await bot.create_chat_invite_link(int(F_SUB))
            except:
                await msg.reply("**__Mᴀᴋᴇ Sᴜʀᴇ I Aᴍ Aᴅᴍɪɴ Iɴ Yᴏᴜʀ Cʜᴀɴɴᴇʟ__**")
                return 
            key = InlineKeyboardMarkup(
                [[
                    InlineKeyboardButton("📢 Uᴘᴅᴀᴛᴇ Cʜᴀɴɴᴇʟ", url=invite_link.invite_link),
                    InlineKeyboardButton("♻️ Tʀʏ Aɢᴀɪɴ", callback_data="chk")
                ]]
            ) 
            await msg.reply_text(
                "**⚠️Access Denied!⚠️\n\nPlease Join My Update Channel To Use Me."
                "If You Joined The Channel Then Click On Check Again Button To Confirm.**",
                reply_markup=key
            )
            return 

    me = (await bot.get_me()).mention
    await bot.send_message(
        chat_id=msg.chat.id,
        text=f"""<b><i>Hᴇʏ {msg.from_user.mention}\n\nI Aᴍ {me}\nYᴏᴜʀ Uʟᴛɪᴍᴀᴛᴇ STRING GENERATOR !\n🔒 𝟷𝟶𝟶% Sᴀғᴇ, Sᴇᴄᴜʀᴇ & Eʀʀᴏʀ-Fʀᴇᴇ\n🚀 Fᴀsᴛ, Rᴇʟɪᴀʙʟᴇ, ᴀɴᴅ Rᴇᴀᴅʏ ᴛᴏ Pᴏᴡᴇʀ Uᴘ Yᴏᴜʀ Sᴇssɪᴏɴs !\n\nCʀᴇᴀᴛᴇᴅ Wɪᴛʜ 💖 Bʏ [@MʏsᴇʟғNᴇᴏɴ](https://t.me/myselfneon) !</i></b>""",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text="⚡ Gᴇɴᴇʀᴀᴛᴇ Sᴛʀɪɴɢ Sᴇssɪᴏɴ", callback_data="generate")],
                [
                    InlineKeyboardButton("Sᴜᴘᴘᴏʀᴛ Gʀᴏᴜᴘ", url="https://t.me/VJ_Bot_Disscussion"),
                    InlineKeyboardButton("Uᴘᴅᴀᴛᴇ Cʜᴀɴɴᴇʟ", url="https://t.me/NeonFiles")
                ]
            ]
        )
    )

@Client.on_callback_query(filters.regex("chk"))
async def chk(bot : Client, cb : CallbackQuery):
    try:
        await bot.get_chat_member(int(F_SUB), cb.from_user.id)
    except:
        await cb.answer(
            "**__Yᴏᴜ Hᴀᴠᴇ Jᴏɪɴᴇᴅ Mʏ Uᴘᴅᴀᴛᴇ Cʜᴀɴɴᴇʟ. Pʟᴇᴀsᴇ Jᴏɪɴ Iᴛ Aɴᴅ Tʜᴇɴ Cʟɪᴄᴋ Tʀʏ Aɢᴀɪɴ__**",
            show_alert=True
        )
        return 
    me = (await bot.get_me()).mention
    await bot.send_message(
        chat_id=cb.from_user.id,
        text=f"""<b><i>Hᴇʏ {msg.from_user.mention}\n\nI Aᴍ {me}\nYᴏᴜʀ Uʟᴛɪᴍᴀᴛᴇ STRING GENERATOR !\n🔒 𝟷𝟶𝟶% Sᴀғᴇ, Sᴇᴄᴜʀᴇ & Eʀʀᴏʀ-Fʀᴇᴇ\n🚀 Fᴀsᴛ, Rᴇʟɪᴀʙʟᴇ, ᴀɴᴅ Rᴇᴀᴅʏ ᴛᴏ Pᴏᴡᴇʀ Uᴘ Yᴏᴜʀ Sᴇssɪᴏɴs !\n\nCʀᴇᴀᴛᴇᴅ Wɪᴛʜ 💖 Bʏ [@MʏsᴇʟғNᴇᴏɴ](https://t.me/myselfneon) !</i></b>""",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text="⚡ Gᴇɴᴇʀᴀᴛᴇ Sᴛʀɪɴɢ Sᴇssɪᴏɴ", callback_data="generate")],
                [
                    InlineKeyboardButton("Sᴜᴘᴘᴏʀᴛ Gʀᴏᴜᴘ", url="https://t.me/VJ_Bot_Disscussion"),
                    InlineKeyboardButton("Uᴘᴅᴀᴛᴇ Cʜᴀɴɴᴇʟ", url="https://t.me/NeonFiles")
                ]
            ]
        )
                )
