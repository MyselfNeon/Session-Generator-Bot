#Start.py
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from config import OWNER_ID, F_SUB
from Neon.db import db
import random

# Replace with your actual custom links
MY_CUSTOM_LINKS = {
    "Neon": "Contact Owner & Details 🍀\n\nhttps://myselfneon.github.io/neon/"
}

REACTIONS = [
    "🤝", "😇", "🤗", "😍", "👍", "🎅", "😐", "🥰", "🤩",
    "😱", "🤣", "😘", "👏", "😛", "😈", "🎉", "⚡️", "🫡",
    "🤓", "😎", "🏆", "🔥", "🤭", "🌚", "🆒", "👻", "😁"]
# Don't add unsupported emojis because Telegram reactions have limits

@Client.on_message(filters.private & filters.incoming & filters.command("start"))
async def start(bot: Client, msg: Message):
    # --- Reaction feature ---
    try:
        await msg.react(emoji=random.choice(REACTIONS), big=True)
    except Exception as e:
        print(f"Reaction failed: {e}")
    # ------------------------

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

    # --- Add user to DB with username ---
    if not await db.is_user_exist(msg.from_user.id):
        await db.add_user(
            msg.from_user.id,
            msg.from_user.first_name,
            msg.from_user.username or "N/A"  # store username or "N/A"
        )

    # --- Force subscription check ---
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
                    InlineKeyboardButton("Uᴘᴅᴀᴛᴇs 🔥", url=invite_link.invite_link),
                    InlineKeyboardButton("Tʀʏ Aɢᴀɪɴ ♻️", callback_data="chk")
                ]]
            ) 
            await msg.reply_text(
                "<b><blockquote>🚫 𝐀𝐂𝐂𝐄𝐒𝐒 𝐃𝐄𝐍𝐈𝐄𝐃 🚫</blockquote>\n<blockquote><i>Join My Update Channel To Use Me Once You’ve Joined, Click The Try Again Button To Confirm Your Subscription And Gain Access.\n\n⏰ Thank You For Staying Updated !!</blockquote></b></i>",
                reply_markup=key
            )
            return 

    # --- Send welcome message ---
    me = (await bot.get_me()).mention
    await bot.send_message(
        chat_id=msg.chat.id,
        text=f"""<b><i><blockquote>Yoo !! {msg.from_user.mention}</blockquote>\n<blockquote>🔑 I Am {me}\n🚀 Fast & Reliable Sessions\n🔒 Safe, Secure and Error-Free\n🧩 Your Ultimate STRING Generator !!\n\nCreated By @MyselfNeon 😎</i></b></blockquote>""",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text="⚡ Gᴇɴᴇʀᴀᴛᴇ Sᴛʀɪɴɢ Sᴇssɪᴏɴ ⚡", callback_data="generate")],
                [
                    InlineKeyboardButton("Uᴘᴅᴀᴛᴇ 🔥", url="https://t.me/NeonFiles"),
                    InlineKeyboardButton("Aʙᴏᴜᴛ 😎", callback_data="about_btn")
                ]
            ]
        )
    )

@Client.on_callback_query(filters.regex("chk"))
async def chk(bot: Client, cb: CallbackQuery):
    try:
        await bot.get_chat_member(int(F_SUB), cb.from_user.id)
    except:
        await cb.answer(
            "You Have Not Joined My Updates Channel. Please Join It And Then Click Try Again 🆘",
            show_alert=True
        )
        return 

    me = (await bot.get_me()).mention
    await cb.message.edit_text(
        f"""<b><i><blockquote>Yoo !! {cb.from_user.mention}</blockquote>\n<blockquote>🔑 I Am {me}\n🚀 Fast & Reliable Sessions\n🔒 Safe, Secure and Error-Free\n🧩 Your Ultimate STRING Generator !!\n\nCreated By @MyselfNeon 😎</i></b></blockquote>""",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text="⚡ Gᴇɴᴇʀᴀᴛᴇ Sᴛʀɪɴɢ Sᴇssɪᴏɴ ⚡", callback_data="generate")],
                [
                    InlineKeyboardButton("Uᴘᴅᴀᴛᴇ 🔥", url="https://t.me/NeonFiles"),
                    InlineKeyboardButton("Aʙᴏᴜᴛ 😎", callback_data="about_btn")
                ]
            ]
        )
    )
    await cb.answer()

# --- About page callback ---
@Client.on_callback_query(filters.regex("about_btn"))
async def about_page(bot: Client, cb: CallbackQuery):
    me = (await bot.get_me()).mention  # <-- added dynamic mention

    about_text = f"""<b><blockquote>‣ 📝 𝐌𝐘 𝐃𝐄𝐓𝐀𝐈𝐋𝐒</blockquote>
<blockquote><i>• Mʏ Nᴀᴍᴇ : {me}
• Mʏ Bᴇsᴛ Fʀɪᴇɴᴅ : <a href='tg://settings'>Tʜɪs Sᴡᴇᴇᴛɪᴇ ❤️</a> 
• Dᴇᴠᴇʟᴏᴘᴇʀ : <a href='https://t.me/MyselfNeon'>@MʏsᴇʟғNᴇᴏɴ</a> 
• Lɪʙʀᴀʀʏ : <a href='https://docs.pyrogram.org/'>Pʏʀᴏɢʀᴀᴍ</a> 
• Lᴀɴɢᴜᴀɢᴇ : <a href='https://www.python.org/download/releases/3.0/'>Pʏᴛʜᴏɴ 𝟹</a> 
• DᴀᴛᴀBᴀsᴇ : <a href='https://www.mongodb.com/'>Mᴏɴɢᴏ DB</a> 
• Bᴏᴛ Sᴇʀᴠᴇʀ : <a href='https://heroku.com'>Hᴇʀᴏᴋᴜ</a> 
• Bᴜɪʟᴅ Sᴛᴀᴛᴜs : ᴠ𝟸.𝟽.𝟷 [Sᴛᴀʙʟᴇ]</i></b></blockquote>"""

    about_buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Sᴜᴘᴘᴏʀᴛ 🔊", url="https://t.me/+o1s-8MppL2syYTI9"),
                InlineKeyboardButton("Sᴏᴜʀᴄᴇ Cᴏᴅᴇ 🚀", url="https://t.me/NeonSessionBot?start=Neon")
            ],
            [
                InlineKeyboardButton("Cʟᴏsᴇ ❌", callback_data="close"),
                InlineKeyboardButton("⬅️ Bᴀᴄᴋ", callback_data="back_to_start")
            ]
        ]
    )

    await cb.message.edit_text(
        about_text,
        reply_markup=about_buttons,
        disable_web_page_preview=True  # <-- web preview disabled
    )
    await cb.answer()

@Client.on_callback_query(filters.regex("back_to_start"))
async def back_to_start(bot: Client, cb: CallbackQuery):
    me = (await bot.get_me()).mention
    await cb.message.edit_text(
        f"""<b><i><blockquote>Yoo !! {cb.from_user.mention}</blockquote>\n<blockquote>🔑 I Am {me}\n🚀 Fast & Reliable Sessions\n🔒 Safe, Secure and Error-Free\n🧩 Your Ultimate STRING Generator !!\n\nCreated By @MyselfNeon 😎</i></b></blockquote>""",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text="⚡ Gᴇɴᴇʀᴀᴛᴇ Sᴛʀɪɴɢ Sᴇssɪᴏɴ ⚡", callback_data="generate")],
                [
                    InlineKeyboardButton("Uᴘᴅᴀᴛᴇ 🔥", url="https://t.me/NeonFiles"),
                    InlineKeyboardButton("Aʙᴏᴜᴛ 😎", callback_data="about_btn")
                ]
            ]
        )
    )
    await cb.answer()

@Client.on_callback_query(filters.regex("close"))
async def close_page(bot: Client, cb: CallbackQuery):
    await cb.message.delete()
    await cb.answer()
    
