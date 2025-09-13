from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from config import OWNER_ID, F_SUB
from Neon.db import db

# Replace with your actual custom links
MY_CUSTOM_LINKS = {
    "Neon": "https://myselfneon.github.io/about/"
}

@Client.on_message(filters.private & filters.incoming & filters.command("start"))
async def start(bot: Client, msg: Message):
    args = msg.text.split(maxsplit=1)

    # Handle deep-link parameter
    if len(args) > 1:
        key = args[1]
        if key in MY_CUSTOM_LINKS:
            await msg.reply_text(f"**__Here's Your Link__ 🖇️**\n\n**__{MY_CUSTOM_LINKS[key]}__**")
            return
        else:
            await msg.reply_text(f"**__You Started me with: {key}__**")
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
                await msg.reply("**__Make Sure I'm Admin in Your Channel__**")
                return 
            key = InlineKeyboardMarkup(
                [[
                    InlineKeyboardButton("📢 Uᴘᴅᴀᴛᴇs", url=invite_link.invite_link),
                    InlineKeyboardButton("♻️ Tʀʏ Aɢᴀɪɴ", callback_data="chk")
                ]]
            ) 
            await msg.reply_text(
                "<i><b><blockquote>🚫 𝐀𝐂𝐂𝐄𝐒𝐒 𝐃𝐄𝐍𝐈𝐄𝐃</blockquote>\n\nJoin My Update Channel To Use Me Once You’ve Joined, Click The Try Again Button To Confirm Your Subscription And Gain Access.\n\nThank You For Staying Updated !!</b></i>",
                reply_markup=key
            )
            return 

    me = (await bot.get_me()).mention
    await bot.send_message(
        chat_id=msg.chat.id,
        text=f"""<b><i>Hᴇʏ {msg.from_user.mention}\n\nI Aᴍ {me}\nYᴏᴜʀ Uʟᴛɪᴍᴀᴛᴇ STRING GENERATOR !\n🔒 Sᴀғᴇ, Sᴇᴄᴜʀᴇ & Eʀʀᴏʀ-Fʀᴇᴇ\n🚀 Fᴀsᴛ, Rᴇʟɪᴀʙʟᴇ, ᴀɴᴅ Rᴇᴀᴅʏ ᴛᴏ Pᴏᴡᴇʀ Uᴘ Yᴏᴜʀ Sᴇssɪᴏɴs !\n\nCʀᴇᴀᴛᴇᴅ Wɪᴛʜ 💖 Bʏ [@MʏsᴇʟғNᴇᴏɴ](https://t.me/myselfneon) !</i></b>""",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text="⚡ Gᴇɴᴇʀᴀᴛᴇ Sᴛʀɪɴɢ Sᴇssɪᴏɴ ⚡", callback_data="generate")],
                [
                    InlineKeyboardButton("Sᴜᴘᴘᴏʀᴛ Gʀᴏᴜᴘ", url="https://t.me/+o1s-8MppL2syYTI9"),
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
            "You Have Joined My Updates Channel. Please Join It And Then Click Try Again 🆘",
            show_alert=True
        )
        return 
    me = (await bot.get_me()).mention
    await bot.send_message(
        chat_id=cb.from_user.id,
        text=f"""<b><i>Hᴇʏ {msg.from_user.mention}\n\nI Aᴍ {me}\nYᴏᴜʀ Uʟᴛɪᴍᴀᴛᴇ STRING GENERATOR !\n🔒 Sᴀғᴇ, Sᴇᴄᴜʀᴇ & Eʀʀᴏʀ-Fʀᴇᴇ\n🚀 Fᴀsᴛ, Rᴇʟɪᴀʙʟᴇ, ᴀɴᴅ Rᴇᴀᴅʏ ᴛᴏ Pᴏᴡᴇʀ Uᴘ Yᴏᴜʀ Sᴇssɪᴏɴs !\n\nCreated By @MyselfNeon 😎</i></b>""",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text="⚡ Gᴇɴᴇʀᴀᴛᴇ Sᴛʀɪɴɢ Sᴇssɪᴏɴ ⚡", callback_data="generate")],
                [
                    InlineKeyboardButton("Sᴜᴘᴘᴏʀᴛ Gʀᴏᴜᴘ", url="https://t.me/+o1s-8MppL2syYTI9"),
                    InlineKeyboardButton("Uᴘᴅᴀᴛᴇ Cʜᴀɴɴᴇʟ", url="https://t.me/NeonFiles")
                ]
            ]
        )
                )
