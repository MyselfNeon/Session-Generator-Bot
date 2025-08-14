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

ask_ques = "**__Cʜᴏᴏsᴇ Tʜᴇ Sᴛʀɪɴɢ Wʜɪᴄʜ Yᴏᴜ Wᴀɴᴛ Tᴏ Gᴇɴᴇʀᴀᴛᴇ Fʀᴏᴍ Bᴇʟᴏᴡ 👇__**"
buttons_ques = [
    [
        InlineKeyboardButton("Tᴇʟᴇᴛʜᴏɴ", callback_data="telethon"),
        InlineKeyboardButton("Pʏʀᴏɢʀᴀᴍ", callback_data="pyrogram")
    ],[
        InlineKeyboardButton("Pʏʀᴏɢʀᴀᴍ Bᴏᴛ", callback_data="pyrogram_bot"),
        InlineKeyboardButton("Tᴇʟᴇᴛʜᴏɴ Bᴏᴛ", callback_data="telethon_bot")
    ]
]

gen_button = [[InlineKeyboardButton(text="⚡ Gᴇɴᴇʀᴀᴛᴇ Sᴛʀɪɴɢ Sᴇssɪᴏɴ ⚡", callback_data="generate")]]

@Client.on_message(filters.private & ~filters.forwarded & filters.command(["generate", "gen", "string", "str"]))
async def main(_, msg):
    await msg.reply(ask_ques, reply_markup=InlineKeyboardMarkup(buttons_ques))

async def generate_session(bot: Client, msg: Message, telethon=False, is_bot: bool = False):
    if not await db.is_user_exist(msg.from_user.id):
        await db.add_user(msg.from_user.id, msg.from_user.first_name)
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
                    InlineKeyboardButton("Tʀʏ Aɢᴀɪɴ", callback_data="chk")
                ]]
            ) 
            await msg.reply_text("<i><b><blockquote>🚫 𝐀𝐂𝐂𝐄𝐒𝐒 𝐃𝐄𝐍𝐈𝐄𝐃</blockquote>\n\nJᴏɪɴ Mʏ Uᴘᴅᴀᴛᴇ Cʜᴀɴɴᴇʟ Tᴏ Usᴇ Mᴇ Oɴᴄᴇ Yᴏᴜ’ᴠᴇ Jᴏɪɴᴇᴅ, Cʟɪᴄᴋ Tʜᴇ “Tʀʏ Aɢᴀɪɴ” Bᴜᴛᴛᴏɴ Tᴏ Cᴏɴғɪʀᴍ Yᴏᴜʀ Sᴜʙsᴄʀɪᴘᴛɪᴏɴ Aɴᴅ Gᴀɪɴ Aᴄᴄᴇss.\n\nTʜᴀɴᴋ Yᴏᴜ Fᴏʀ Sᴛᴀʏɪɴɢ Uᴘᴅᴀᴛᴇᴅ !!</b></i>", reply_markup=key)
            return 
    if telethon:
        ty = "Tᴇʟᴇᴛʜᴏɴ"
    else:
        ty = "Pʏʀᴏɢʀᴀᴍ"
    if is_bot:
        ty += " Bᴏᴛ"
    await msg.reply(f"**__Tʀʏɪɴɢ Tᴏ Sᴛᴀʀᴛ {ty} Sᴇssɪᴏɴ Gᴇɴᴇʀᴀᴛᴏʀ__**...")
    user_id = msg.chat.id
    api_id_msg = await bot.ask(user_id, "**__Sᴇɴᴅ Yᴏᴜʀ --Aᴘɪ Iᴅ-- Tᴏ Pʀᴏᴄᴇᴇᴅ.\n\nCʟɪᴄᴋ Oɴ /skip Fᴏʀ Usɪɴɢ Bᴏᴛ Aᴘɪ.__**", filters=filters.text)
    if await cancelled(api_id_msg):
        return
    if api_id_msg.text == "/skip":
        api_id = config.API_ID
        api_hash = config.API_HASH
    else:
        try:
            api_id = int(api_id_msg.text)
        except ValueError:
            await api_id_msg.reply("**__--Aᴘɪ Iᴅ-- Mᴜsᴛ Bᴇ Aɴ Iɴᴛᴇɢᴇʀ,\nSᴛᴀʀᴛ Gᴇɴᴇʀᴀᴛɪɴɢ Yᴏᴜʀ Sᴇssɪᴏɴ Aɢᴀɪɴ__**", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
            return
        api_hash_msg = await bot.ask(user_id, "**__Nᴏᴡ Sᴇɴᴅ Yᴏᴜʀ --Aᴘɪ Hᴀsʜ-- Tᴏ Cᴏɴᴛɪɴᴜᴇ.__**", filters=filters.text)
        if await cancelled(api_hash_msg):
            return
        api_hash = api_hash_msg.text
    if not is_bot:
        t = "**__Sᴇɴᴅ Yᴏᴜʀ Pʜᴏɴᴇ Nᴜᴍʙᴇʀ Wɪᴛʜ Cᴏᴜɴᴛʀʏ Cᴏᴅᴇ Fᴏʀ Wʜɪᴄʜ Yᴏᴜ Wᴀɴᴛ ᴛᴏ Gᴇɴᴇʀᴀᴛᴇ Sᴇssɪᴏɴ__** \n**__Exᴀᴍᴘʟᴇ__** : `+9100000000`'"
    else:
        t = "**__Pʟᴇᴀsᴇ Sᴇɴᴅ Yᴏᴜʀ --Bᴏᴛ Tᴏᴋᴇɴ-- Tᴏ Cᴏɴᴛɪɴᴜᴇ.\nExᴀᴍᴩʟᴇ__** : `123456789:neonisthebestonearound`'"
    phone_number_msg = await bot.ask(user_id, t, filters=filters.text)
    if await cancelled(phone_number_msg):
        return
    phone_number = phone_number_msg.text
    if not is_bot:
        await msg.reply("**__Tʀʏɪɴɢ Tᴏ Sᴇɴᴅ OTP Aᴛ Tʜᴇ Gɪᴠᴇɴ Nᴜᴍʙᴇʀ__**")
    else:
        await msg.reply("**__Tʀʏɪɴɢ Tᴏ Lᴏɢɪɴ Vɪᴀ Bᴏᴛ Tᴏᴋᴇɴ__**")
    if telethon and is_bot:
        client = TelegramClient(StringSession(), api_id, api_hash)
    elif telethon:
        client = TelegramClient(StringSession(), api_id, api_hash)
    elif is_bot:
        client = Client(name="bot", api_id=api_id, api_hash=api_hash, bot_token=phone_number, in_memory=True)
    else:
        client = Client(name="user", api_id=api_id, api_hash=api_hash, in_memory=True)
    await client.connect()
    try:
        code = None
        if not is_bot:
            if telethon:
                code = await client.send_code_request(phone_number)
            else:
                code = await client.send_code(phone_number)
    except (ApiIdInvalid, ApiIdInvalidError):
        await msg.reply("**__Yᴏᴜʀ --Aᴘɪ Iᴅ-- Aɴᴅ --Aᴘɪ Hᴀsʜ-- Cᴏᴍʙɪɴᴀᴛɪᴏɴ Dᴏᴇsɴ'ᴛ Mᴀᴛᴄʜ Wɪᴛʜ Tᴇʟᴇɢʀᴀᴍ Aᴩᴩs Sʏsᴛᴇᴍ. \n\nPʟᴇᴀsᴇ Sᴛᴀʀᴛ Gᴇɴᴇʀᴀᴛɪɴɢ Yᴏᴜʀ Sᴇssɪᴏɴ Aɢᴀɪɴ__**", reply_markup=InlineKeyboardMarkup(gen_button))
        return
    except (PhoneNumberInvalid, PhoneNumberInvalidError):
        await msg.reply("**__Tʜᴇ --Pʜᴏɴᴇ Nᴜᴍʙᴇʀ-- Yᴏᴜ'ᴠᴇ Sᴇɴᴛ Dᴏᴇsɴ'ᴛ Bᴇʟᴏɴɢ Tᴏ Aɴʏ Tᴇʟᴇɢʀᴀᴍ Aᴄᴄᴏᴜɴᴛ.\n\nPʟᴇᴀsᴇ Sᴛᴀʀᴛ Gᴇɴᴇʀᴀᴛɪɴɢ Yᴏᴜʀ Sᴇssɪᴏɴ Aɢᴀɪɴ__**", reply_markup=InlineKeyboardMarkup(gen_button))
        return
    try:
        phone_code_msg = None
        if not is_bot:
            phone_code_msg = await bot.ask(user_id, "**__Pʟᴇᴀsᴇ Sᴇɴᴅ Tʜᴇ OTP Tʜᴀᴛ Yᴏᴜ'ᴠᴇ Rᴇᴄᴇɪᴠᴇᴅ Fʀᴏᴍ Tᴇʟᴇɢʀᴀᴍ Oɴ Yᴏᴜʀ Aᴄᴄᴏᴜɴᴛ.\nSᴜᴘᴘᴏsᴇ OTP Rᴇᴄᴇɪᴠᴇᴅ Is**__ `12345`,\n**__Sᴇɴᴅ Iᴛ As__** `1 2 3 4 5`.", filters=filters.text, timeout=600)
            if await cancelled(phone_code_msg):
                return
    except TimeoutError:
        await msg.reply("**__Tɪᴍᴇ Lɪᴍɪᴛ Rᴇᴀᴄʜᴇᴅ Oғ 10 Mɪɴᴜᴛᴇs.\n\nPʟᴇᴀsᴇ Sᴛᴀʀᴛ Gᴇɴᴇʀᴀᴛɪɴɢ Yᴏᴜʀ Sᴇssɪᴏɴ Aɢᴀɪɴ__**", reply_markup=InlineKeyboardMarkup(gen_button))
        return
    if not is_bot:
        phone_code = phone_code_msg.text.replace(" ", "")
        try:
            if telethon:
                await client.sign_in(phone_number, phone_code, password=None)
            else:
                await client.sign_in(phone_number, code.phone_code_hash, phone_code)
        except (PhoneCodeInvalid, PhoneCodeInvalidError):
            await msg.reply("**__Tʜᴇ OTP Yᴏᴜ'ᴠᴇ Sᴇɴᴛ Is --Wʀᴏɴɢ--\n\nPʟᴇᴀsᴇ Sᴛᴀʀᴛ Gᴇɴᴇʀᴀᴛɪɴɢ Yᴏᴜʀ Sᴇssɪᴏɴ Aɢᴀɪɴ__**", reply_markup=InlineKeyboardMarkup(gen_button))
            return
        except (PhoneCodeExpired, PhoneCodeExpiredError):
            await msg.reply("**__Tʜᴇ OTP Yᴏᴜ'ᴠᴇ Sᴇɴᴛ Is --Exᴘɪʀᴇᴅ--\n\nᴩʟᴇᴀsᴇ Sᴛᴀʀᴛ Gᴇɴᴇʀᴀᴛɪɴɢ Yᴏᴜʀ Sᴇssɪᴏɴ Aɢᴀɪɴ__**", reply_markup=InlineKeyboardMarkup(gen_button))
            return
        except (SessionPasswordNeeded, SessionPasswordNeededError):
            try:
                two_step_msg = await bot.ask(user_id, "**__Pʟᴇᴀsᴇ Eɴᴛᴇʀ Yᴏᴜʀ --Tᴡᴏ Sᴛᴇᴘs Vᴇʀɪғɪᴄᴀᴛɪᴏɴ-- Pᴀssᴡᴏʀᴅ Tᴏ Cᴏɴᴛɪɴᴜᴇ__**", filters=filters.text, timeout=300)
            except TimeoutError:
                await msg.reply("**__Tɪᴍᴇ Lɪᴍɪᴛ Rᴇᴀᴄʜᴇᴅ Oғ 05 Mɪɴᴜᴛᴇs.\n\nPʟᴇᴀsᴇ Sᴛᴀʀᴛ Gᴇɴᴇʀᴀᴛɪɴɢ Yᴏᴜʀ Sᴇssɪᴏɴ Aɢᴀɪɴ__**", reply_markup=InlineKeyboardMarkup(gen_button))
                return
            try:
                password = two_step_msg.text
                if telethon:
                    await client.sign_in(password=password)
                else:
                    await client.check_password(password=password)
                if await cancelled(api_id_msg):
                    return
            except (PasswordHashInvalid, PasswordHashInvalidError):
                await two_step_msg.reply("**__Tʜᴇ Pᴀssᴡᴏʀᴅ Yᴏᴜ'ᴠᴇ Sᴇɴᴛ Is Wʀᴏɴɢ.\n\nPʟᴇᴀsᴇ Sᴛᴀʀᴛ Gᴇɴᴇʀᴀᴛɪɴɢ Yᴏᴜʀ Sᴇssɪᴏɴ Aɢᴀɪɴ__**", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
                return
    else:
        if telethon:
            await client.start(bot_token=phone_number)
        else:
            await client.sign_in_bot(phone_number)
    if telethon:
        string_session = client.session.save()
    else:
        string_session = await client.export_session_string()
    text = f"**__Tʜɪs Is Yᴏᴜʀ {ty} Sᴛʀɪɴɢ Sᴇssɪᴏɴ__** \n\n`{string_session}` \n\n**__⚡ Gᴇɴᴇʀᴀᴛᴇᴅ Bʏ @NeonFiles ⚡__**\n\n<blockquote>‣ **𝐍𝐎𝐓𝐄**</blockquote>\n**__Dᴏ Nᴏᴛ Sʜᴀʀᴇ Tʜɪs Iɴғᴏʀᴍᴀᴛɪᴏɴ Wɪᴛʜ Aɴʏᴏɴᴇ. Iᴛ Cᴏᴜʟᴅ Pᴏᴛᴇɴᴛɪᴀʟʟʏ Cᴏᴍᴘʀᴏᴍɪsᴇ Aʟʟ Oғ Yᴏᴜʀ Dᴀᴛᴀ !!__**"
    try:
        if not is_bot:
            await client.send_message("me", text)
        else:
            await bot.send_message(msg.chat.id, text)
    except KeyError:
        pass
    await client.disconnect()
    await bot.send_message(msg.chat.id, "**__Sᴜᴄᴄᴇssғᴜʟʟʏ Gᴇɴᴇʀᴀᴛᴇᴅ Yᴏᴜʀ__** {} **__Sᴛʀɪɴɢ Sᴇssɪᴏɴ\n\nPʟᴇᴀsᴇ Cʜᴇᴄᴋ Yᴏᴜʀ Sᴀᴠᴇᴅ Mᴇssᴀɢᴇs Cʜᴀᴛ Tᴏ Vɪᴇᴡ Iᴛ\n\nA Pᴏᴡᴇʀғᴜʟ Sᴛʀɪɴɢ Sᴇssɪᴏɴ Gᴇɴᴇʀᴀᴛᴏʀ Bᴏᴛ Dᴇᴠᴇʟᴏᴘᴇᴅ Bʏ @MyselfNeon__**".format("ᴛᴇʟᴇᴛʜᴏɴ" if telethon else "ᴩʏʀᴏɢʀᴀᴍ"))


async def cancelled(msg):
    if "/cancel" in msg.text:
        await msg.reply("**__Cᴀɴᴄᴇʟʟᴇᴅ Tʜᴇ Oɴɢᴏɪɴɢ Sᴛʀɪɴɢ Gᴇɴᴇʀᴀᴛɪᴏɴ Pʀᴏᴄᴇss__**", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
        return True
    elif "/restart" in msg.text:
        await msg.reply("**__Sᴜᴄᴄᴇssғᴜʟʟʏ Rᴇsᴛᴀʀᴛᴇᴅ Tʜɪs Bᴏᴛ Fᴏʀ Yᴏᴜ__**", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
        return True
    elif "/skip" in msg.text:
        return False
    elif msg.text.startswith("/"):  # Bot Commands
        await msg.reply("**__Cᴀɴᴄᴇʟʟᴇᴅ Tʜᴇ Oɴɢᴏɪɴɢ Sᴛʀɪɴɢ Sᴇssɪᴏɴ Gᴇɴᴇʀᴀᴛɪɴɢ Pʀᴏᴄᴇss__**", quote=True)
        return True
    else:
        return False
