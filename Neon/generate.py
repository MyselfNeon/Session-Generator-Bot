#Generate.py
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

ask_ques = "**__Choose The String Which You Want to Generate from Below__  ⬇️**"
buttons_ques = [
    [
        InlineKeyboardButton("Tᴇʟᴇᴛʜᴏɴ 🤖", callback_data="telethon"),
        InlineKeyboardButton("Pʏʀᴏɢʀᴀᴍ 🐍", callback_data="pyrogram")
    ],[
        InlineKeyboardButton("Tᴇʟᴇᴛʜᴏɴ Bᴏᴛ", callback_data="telethon_bot"),
        InlineKeyboardButton("Pʏʀᴏɢʀᴀᴍ Bᴏᴛ", callback_data="pyrogram_bot")
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
                await msg.reply("**__Make Sure I Am Admin In Your Channel With Full Rights Given 🛐__**")
                return
            key = InlineKeyboardMarkup(
                [[
                    InlineKeyboardButton("Jᴏɪɴ Uᴘᴅᴀᴛᴇs", url=invite_link.invite_link),
                    InlineKeyboardButton("Tʀʏ Aɢᴀɪɴ", callback_data="chk")
                ]]
            ) 
            await msg.reply_text("<b><blockquote>🚫 𝐀𝐂𝐂𝐄𝐒𝐒 𝐃𝐄𝐍𝐈𝐄𝐃</blockquote>\n\n<i><blockquote>Join My Update Channel To Use Me Once You've Joined, Click The Try Again Button To Confirm Your Subscription And Gain Access.\n\n🍀 Thank You For Staying Updated !!</b></i></blockquote>", reply_markup=key)
            return 
    if telethon:
        ty = "Tᴇʟᴇᴛʜᴏɴ"
    else:
        ty = "Pʏʀᴏɢʀᴀᴍ"
    if is_bot:
        ty += " Bᴏᴛ"
    await msg.reply(f"**__Trying To Start {ty} Session Generator__**...")
    user_id = msg.chat.id
    api_id_msg = await bot.ask(user_id, "**__Send Your --API ID-- Tᴏ Pʀᴏᴄᴇᴇᴅ.\n\nClick On /skip For Using Bot Api.__**", filters=filters.text)
    if await cancelled(api_id_msg):
        return
    if api_id_msg.text == "/skip":
        api_id = config.API_ID
        api_hash = config.API_HASH
    else:
        try:
            api_id = int(api_id_msg.text)
        except ValueError:
            await api_id_msg.reply("**__--API ID-- Must Be An Integer,\nStart Generating Your Seasion Again__**", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
            return
        api_hash_msg = await bot.ask(user_id, "**__Now Send You --API HASH-- To Continue.__**", filters=filters.text)
        if await cancelled(api_hash_msg):
            return
        api_hash = api_hash_msg.text
    if not is_bot:
        t = "**__Send Your Phone Number With Country Code For Which You Want To Generate Session__** \n**__Example__** : `+9100000000`'"
    else:
        t = "**__Please Send Your --BOT TOKEN-- To Continue.\nExample__** : `123456789:NeonIsTheBestOneAround`'"
    phone_number_msg = await bot.ask(user_id, t, filters=filters.text)
    if await cancelled(phone_number_msg):
        return
    phone_number = phone_number_msg.text
    if not is_bot:
        await msg.reply("**__Trying To Send OTP At The Given Nember__**")
    else:
        await msg.reply("**__Trying To Login Via Bot Token__**")
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
        await msg.reply("**__Your --API ID-- And --API HASH-- Combination Doesn't Match With Telegram Apps System. \n\nPlease Start Generating Your Session Again.__**", reply_markup=InlineKeyboardMarkup(gen_button))
        return
    except (PhoneNumberInvalid, PhoneNumberInvalidError):
        await msg.reply("**__The --Phone Number-- You'he Sent Doesn't Belong To Any Telegram Account.\n\nPlease Start Generating Your Session Again__**", reply_markup=InlineKeyboardMarkup(gen_button))
        return
    try:
        phone_code_msg = None
        if not is_bot:
            phone_code_msg = await bot.ask(user_id, "**__Please Send The OTP That You've Received From Telegram On Your Account.\nSuppose OTP Received Is**__ `12345`,\n**__Send It As__** `1 2 3 4 5`.", filters=filters.text, timeout=600)
            if await cancelled(phone_code_msg):
                return
    except TimeoutError:
        await msg.reply("**__Time Limit Reached Of 10 Minutes.\n\nPlease Start Generating Your Session Again__**", reply_markup=InlineKeyboardMarkup(gen_button))
        return
    if not is_bot:
        phone_code = phone_code_msg.text.replace(" ", "")
        try:
            if telethon:
                await client.sign_in(phone_number, phone_code, password=None)
            else:
                await client.sign_in(phone_number, code.phone_code_hash, phone_code)
        except (PhoneCodeInvalid, PhoneCodeInvalidError):
            await msg.reply("**__Tʜᴇ OTP Yᴏᴜ'ᴠᴇ Sᴇɴᴛ Is --Wʀᴏɴɢ--\n\nPlease Start Generating Your Session Again__**", reply_markup=InlineKeyboardMarkup(gen_button))
            return
        except (PhoneCodeExpired, PhoneCodeExpiredError):
            await msg.reply("**__The OTP You've Sent Is Expired.\n\nPlease Start Generating Your Session Again__**", reply_markup=InlineKeyboardMarkup(gen_button))
            return
        except (SessionPasswordNeeded, SessionPasswordNeededError):
            try:
                two_step_msg = await bot.ask(user_id, "**__Please Enter Your --Two Steps Verification-- Password To Continue__**", filters=filters.text, timeout=300)
            except TimeoutError:
                await msg.reply("**__Time Limit Reached Of 05 Minutes.\n\nPlease Start Generating Your Session Again__**", reply_markup=InlineKeyboardMarkup(gen_button))
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
                await two_step_msg.reply("**__The Password You've Sent Is Wrong.\n\nPlease Start Generating Your Session Again__**", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
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
    text = f"**__This Is Your {ty} String Session__**\n\n`{string_session}` \n\n**__Generated By @NeonFiles__**\n\n**__Do Not Share This Information With Anyone. It Could Potentially Compromise All Of Your Data !!__**"
    try:
        if not is_bot:
            await client.send_message("me", text)
        else:
            await bot.send_message(msg.chat.id, text)
    except KeyError:
        pass
    await client.disconnect()
    await bot.send_message(msg.chat.id, "**__--Successfully Generated Your String Session For--__** {} ✅\n\n**__Please Check Your Saved Messages Chat To View It 🗒\n\nA String Session Generator Bot Developed By @MyselfNeon__ 🛐**".format("ᴛᴇʟᴇᴛʜᴏɴ" if telethon else "ᴩʏʀᴏɢʀᴀᴍ"))


async def cancelled(msg):
    if "/cancel" in msg.text:
        await msg.reply("**__Cancelled The Ongoing String Generation 🥲__**", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
        return True
    elif "/restart" in msg.text:
        await msg.reply("**__Successfully Restarted the Bot__**", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
        return True
    elif "/skip" in msg.text:
        return False
    elif msg.text.startswith("/"):  # Bot Commands
        await msg.reply("**__Cancelled The Ongoing String Session Generating Process__ ❌**", quote=True)
        return True
    else:
        return False


# Dont remove Credits
# Developer Telegram @MyselfNeon
# Update channel - @NeonFiles
