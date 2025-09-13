from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from config import OWNER_ID, F_SUB
from Neon.db import db

# Replace with your actual custom links
MY_CUSTOM_LINKS = {
    "Neon": "https://myselfneon.github.io/about/"
}

START_TEXT = """<b><i>Hey {user}\n\n🔑 I Am {bot}\n🚀 Fast & Reliable Sessions\n🔒 Safe, Secure and Error-Free\n🧩 Your Ultimate STRING Generator !!\n\nCreated By @MyselfNeon 😎</i></b>"""

ABOUT_TEXT = """‣ 📝 𝐌𝐘 𝐃𝐄𝐓𝐀𝐈𝐋𝐒
• Mʏ Nᴀᴍᴇ : Auto Filter
• Mʏ Bᴇsᴛ Fʀɪᴇɴᴅ : Tʜɪs Sᴡᴇᴇᴛɪᴇ ❤️
• Dᴇᴠᴇʟᴏᴘᴇʀ : @MyselfNeon
• Lɪʙʀᴀʀʏ : Pʏʀᴏɢʀᴀᴍ
• Lᴀɴɢᴜᴀɢᴇ : Pʏᴛʜᴏɴ 𝟹
• DᴀᴛᴀBᴀsᴇ : Mᴏɴɢᴏ DB
• Bᴏᴛ Sᴇʀᴠᴇʀ : Hᴇʀᴏᴋᴜ
• Bᴜɪʟᴅ Sᴛᴀᴛᴜs : ᴠ𝟸.𝟽.𝟷 [Sᴛᴀʙʟᴇ]
"""

# Start Command
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
    await msg.reply_text(
        START_TEXT.format(user=msg.from_user.mention, bot=me),
        reply_markup=start_buttons()
    )

# Generate Page (Page 2 inside same message)
@Client.on_callback_query(filters.regex("generate"))
async def generate_page(bot: Client, cb: CallbackQuery):
    await cb.message.edit_text(
        "**__Cʜᴏᴏsᴇ Tʜᴇ Sᴛʀɪɴɢ Yᴏᴜ Wᴀɴᴛ Tᴏ Gᴇɴᴇʀᴀᴛᴇ 👇__**",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Tᴇʟᴇᴛʜᴏɴ", callback_data="telethon"),
                    InlineKeyboardButton("Pʏʀᴏɢʀᴀᴍ", callback_data="pyrogram")
                ],
                [
                    InlineKeyboardButton("Tᴇʟᴇᴛʜᴏɴ Bᴏᴛ", callback_data="telethon_bot"),
                    InlineKeyboardButton("Pʏʀᴏɢʀᴀᴍ Bᴏᴛ", callback_data="pyrogram_bot")
                ],
                [InlineKeyboardButton("🏠 Hᴏᴍᴇ", callback_data="home")]
            ]
        )
    )

# Try Again / Check Subscription
@Client.on_callback_query(filters.regex("chk"))
async def chk(bot: Client, cb: CallbackQuery):
    try:
        await bot.get_chat_member(int(F_SUB), cb.from_user.id)
    except:
        await cb.answer(
            "You Have Joined My Updates Channel. Please Join It And Then Click Try Again 🆘",
            show_alert=True
        )
        return

    me = (await bot.get_me()).mention
    await cb.message.edit_text(
        START_TEXT.format(user=cb.from_user.mention, bot=me),
        reply_markup=start_buttons()
    )
    await cb.answer("Access Granted ✅", show_alert=True)

# About Page Callback
@Client.on_callback_query(filters.regex("about"))
async def about_page(bot: Client, cb: CallbackQuery):
    about_buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Support Grp", url="https://t.me/+o1s-8MppL2syYTI9"),
                InlineKeyboardButton("Source Code", url="https://myselfneon.github.io/about/")
            ],
            [
                InlineKeyboardButton("Home", callback_data="home"),
                InlineKeyboardButton("Close", callback_data="close")
            ]
        ]
    )
    await cb.message.edit_text(ABOUT_TEXT, reply_markup=about_buttons)

# Home Callback
@Client.on_callback_query(filters.regex("home"))
async def go_home(bot: Client, cb: CallbackQuery):
    me = (await bot.get_me()).mention
    await cb.message.edit_text(
        START_TEXT.format(user=cb.from_user.mention, bot=me),
        reply_markup=start_buttons()
    )

# Close Callback
@Client.on_callback_query(filters.regex("close"))
async def close_message(bot: Client, cb: CallbackQuery):
    await cb.message.delete()
    await cb.answer("Closed ✅", show_alert=False)

# Utility: start buttons
def start_buttons():
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("⚡ Gᴇɴᴇʀᴀᴛᴇ Sᴛʀɪɴɢ Sᴇssɪᴏɴ ⚡", callback_data="generate")],
            [
                InlineKeyboardButton("📝 About", callback_data="about"),
                InlineKeyboardButton("Uᴘᴅᴀᴛᴇ Cʜᴀɴɴᴇʟ", url="https://t.me/NeonFiles")
            ]
        ]
    )
