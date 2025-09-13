import config
from telethon import TelegramClient
from pyrogram import Client, filters
from asyncio.exceptions import TimeoutError
from telethon.sessions import StringSession
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from Neon.db import db
from pyrogram.errors import (
    ApiIdInvalid,
    PhoneNumberInvalid,
    PhoneCodeInvalid,
    PhoneCodeExpired,
    SessionPasswordNeeded,
    PasswordHashInvalid
)
from telethon.errors import (
    ApiIdInvalidError,
    PhoneNumberInvalidError,
    PhoneCodeInvalidError,
    PhoneCodeExpiredError,
    SessionPasswordNeededError,
    PasswordHashInvalidError
)

# Main selection message
ask_ques = "**__Cʜᴏᴏsᴇ Tʜᴇ Sᴛʀɪɴɢ Wʜɪᴄʜ Yᴏᴜ Wᴀɴᴛ Tᴏ Gᴇɴᴇʀᴀᴛᴇ Fʀᴏᴍ Bᴇʟᴏᴡ 👇__**"

# Button layout
buttons_ques = [
    [
        InlineKeyboardButton("Tᴇʟᴇᴛʜᴏɴ", callback_data="telethon"),
        InlineKeyboardButton("Pʏʀᴏɢʀᴀᴍ", callback_data="pyrogram")
    ],[
        # Interchanged Pyrogram Bot and Telethon Bot buttons
        InlineKeyboardButton("Tᴇʟᴇᴛʜᴏɴ Bᴏᴛ", callback_data="telethon_bot"),
        InlineKeyboardButton("Pʏʀᴏɢʀᴀᴍ Bᴏᴛ", callback_data="pyrogram_bot")
    ],
    [
        # Added a big Home button
        InlineKeyboardButton("🏠 Hᴏᴍᴇ", callback_data="home")
    ]
]

gen_button = [[InlineKeyboardButton(text="⚡ Gᴇɴᴇʀᴀᴛᴇ Sᴛʀɪɴɢ Sᴇssɪᴏɴ ⚡", callback_data="generate")]]

# Trigger message
@Client.on_message(filters.private & ~filters.forwarded & filters.command(["generate", "gen", "string", "str"]))
async def main(_, msg):
    await msg.reply(ask_ques, reply_markup=InlineKeyboardMarkup(buttons_ques))


async def generate_session(bot: Client, msg: Message, telethon=False, is_bot: bool = False):
    if not await db.is_user_exist(msg.from_user.id):
        await db.add_user(msg.from_user.id, msg.from_user.first_name)

    # Force join check
    if config.F_SUB:
        try:
            await bot.get_chat_member(int(config.F_SUB), msg.from_user.id)
        except:
            try:
                invite_link = await bot.create_chat_invite_link(int(config.F_SUB))
            except:
                await msg.reply("**__Mᴀᴋᴇ Sᴜʀᴇ I Aᴍ Aᴅᴍɪɴ Iɴ Yᴏᴜʀ Cʜᴀɴɴᴇʟ Wɪᴛʜ Fᴜʟʟ Rɪɢʜᴛs Gɪᴠᴇɴ 🛐__**")
                return
            key = InlineKeyboardMarkup(
                [[
                    InlineKeyboardButton("Jᴏɪɴ Uᴘᴅᴀᴛᴇs", url=invite_link.invite_link),
                    InlineKeyboardButton("Tʀʏ Aɢᴀɪɴ", callback_data="generate")
                ]]
            ) 
            await msg.reply_text(
                "<i><b><blockquote>🚫 𝐀𝐂𝐂𝐄𝐒𝐒 𝐃𝐄𝐍𝐈𝐄𝐃</blockquote>\n\n"
                "Jᴏɪɴ Mʏ Uᴘᴅᴀᴛᴇ Cʜᴀɴɴᴇʟ Tᴏ Usᴇ Mᴇ Oɴᴄᴇ Yᴏᴜ’ᴠᴇ Jᴏɪɴᴇᴅ, "
                "Cʟɪᴄᴋ Tʜᴇ “Tʀʏ Aɢᴀɪɴ” Bᴜᴛᴛᴏɴ Tᴏ Cᴏɴғɪʀᴍ Yᴏᴜʀ Sᴜʙsᴄʀɪᴘᴛɪᴏɴ Aɴᴅ Gᴀɪɴ Aᴄᴄᴇss.\n\n"
                "Tʜᴀɴᴋ Yᴏᴜ Fᴏʀ Sᴛᴀʏɪɴɢ Uᴘᴅᴀᴛᴇᴅ !!</b></i>", 
                reply_markup=key
            )
            return

    # Determine type
    ty = "Tᴇʟᴇᴛʜᴏɴ" if telethon else "Pʏʀᴏɢʀᴀᴍ"
    if is_bot:
        ty += " Bᴏᴛ"

    await msg.reply(f"**__Tʀʏɪɴɢ Tᴏ Sᴛᴀʀᴛ {ty} Sᴇssɪᴏɴ Gᴇɴᴇʀᴀᴛᴏʀ__**...")

    user_id = msg.chat.id
    api_id_msg = await bot.ask(user_id, "**__Sᴇɴᴅ Yᴏᴜʀ --Aᴘɪ Iᴅ-- Tᴏ Pʀᴏᴄᴇᴇᴅ.\n\nCʟɪᴄᴋ Oɴ /skip Fᴏʀ Usɪɴɢ Bᴏᴛ Aᴘɪ.__**", filters=filters.text)
    if await cancelled(api_id_msg):
        return

    api_id = config.API_ID if api_id_msg.text == "/skip" else int(api_id_msg.text)
    api_hash = config.API_HASH if api_id_msg.text == "/skip" else (await bot.ask(user_id, "**__Nᴏᴡ Sᴇɴᴅ Yᴏᴜʀ --Aᴘɪ Hᴀsʜ-- Tᴏ Cᴏɴᴛɪɴᴜᴇ.__**", filters=filters.text)).text

    # Phone / Bot token
    if not is_bot:
        phone_text = "**__Sᴇɴᴅ Yᴏᴜʀ Pʜᴏɴᴇ Nᴜᴍʙᴇʀ Wɪᴛʜ Cᴏᴜɴᴛʀʏ Cᴏᴅᴇ__**\nEx: `+9100000000`"
    else:
        phone_text = "**__Sᴇɴᴅ Yᴏᴜʀ Bᴏᴛ Tᴏᴋᴇɴ__**\nEx: `123456789:neonisthebestonearound`"

    phone_number_msg = await bot.ask(user_id, phone_text, filters=filters.text)
    if await cancelled(phone_number_msg):
        return
    phone_number = phone_number_msg.text

    await msg.reply("**__Tʀʏɪɴɢ Tᴏ Lᴏɢɪɴ...__**" if is_bot else "**__Tʀʏɪɴɢ Tᴏ Sᴇɴᴅ OTP...__**")

    # Initialize client
    if telethon:
        client = TelegramClient(StringSession(), api_id, api_hash)
    else:
        client = Client(name="bot" if is_bot else "user", api_id=api_id, api_hash=api_hash, bot_token=phone_number if is_bot else None, in_memory=True)
    await client.connect()

    # OTP / login
    if not is_bot:
        code = await client.send_code(phone_number) if not telethon else await client.send_code_request(phone_number)

    # Sign in and generate session
    try:
        if not is_bot and not telethon:
            await client.sign_in(phone_number, code.phone_code_hash, phone_number_msg.text.replace(" ", ""))
        elif not is_bot and telethon:
            await client.sign_in(phone_number, phone_number_msg.text.replace(" ", ""), password=None)
        elif is_bot and telethon:
            await client.start(bot_token=phone_number)
        else:
            await client.sign_in_bot(phone_number)
    except Exception as e:
        await msg.reply(f"**__Error Occurred: {str(e)}__**", reply_markup=InlineKeyboardMarkup(gen_button))
        return

    string_session = client.session.save() if telethon else await client.export_session_string()
    await bot.send_message(msg.chat.id, f"**__Here is your {ty} string session:__**\n\n`{string_session}`")

    await client.disconnect()


async def cancelled(msg):
    text = msg.text
    if text.startswith("/cancel") or text.startswith("/"):
        await msg.reply("**__Cancelled the ongoing process__**", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
        return True
    elif text.startswith("/restart"):
        await msg.reply("**__Bot restarted__**", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
        return True
    elif text.startswith("/skip"):
        return False
    return False
