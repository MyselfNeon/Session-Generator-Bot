import os
import re
import time
import logging
import requests
from telegraph import Telegraph
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

# Logger setup
logger = logging.getLogger(__name__)

# --- Configuration ---
DOMAIN = "graph.org"
CATBOX_API_URL = "https://catbox.moe/user/api.php"
IMGBB_API_URL = "https://api.imgbb.com/1/upload"

# Regex Patterns
EMOJI_PATTERN = re.compile(r'<emoji id="\d+">')
TITLE_PATTERN = re.compile(r"title:? (.*)", re.IGNORECASE)

# --- Session Management ---
user_sessions = set()
last_update_time = {}

# --- Custom Filter ---
async def check_session_func(_, __, message):
    return message.from_user and message.from_user.id in user_sessions

has_active_session = filters.create(check_session_func)

# --- Simple Progress Function ---
async def simple_progress(current, total, message):
    percentage = current * 100 / total
    now = time.time()
    last_time = last_update_time.get(message.id, 0)

    if now - last_time > 3 or current == total:
        last_update_time[message.id] = now
        try:
            await message.edit(f"**Downloading... {int(percentage)}%**")
        except Exception:
            pass

# --- Core Logic: Upload Function ---
def upload_file(file_path):
    """
    Priority: ImgBB (fetched from OS)
    Fallback: Catbox.moe
    """
    # Fetching API Key directly from OS
    imgbb_key = os.getenv("IMGBB_API_KEY")
    
    # 1. Attempt ImgBB
    if imgbb_key:
        try:
            logger.info("Attempting upload to ImgBB...")
            with open(file_path, "rb") as f:
                response = requests.post(
                    IMGBB_API_URL,
                    params={"key": imgbb_key},
                    files={"image": f},
                    timeout=60,
                )
            
            if response.ok:
                data = response.json()["data"]
                return {
                    "provider": "ImgBB",
                    "url": data["url"],
                    "delete_url": data.get("delete_url")
                }
        except Exception as e:
            logger.error(f"ImgBB Error: {e}")

    # 2. Fallback to Catbox.moe
    try:
        logger.info("Falling back to Catbox.moe...")
        with open(file_path, "rb") as f:
            response = requests.post(
                CATBOX_API_URL,
                data={"reqtype": "fileupload", "userhash": ""},
                files={"fileToUpload": f},
                timeout=60
            )
            
        if response.ok:
            return {
                "provider": "Catbox",
                "url": response.text.strip(),
                "delete_url": None
            }
    except Exception as e:
        logger.error(f"Catbox Error: {e}")
        
    return None

# --- Handlers ---

@Client.on_message(filters.command("tel") & filters.private)
async def ask_content_handler(client: Client, message: Message):
    user_sessions.add(message.from_user.id)
    await message.reply_text(
        "**✅ Mode Activated!**\n\n"
        "Please send the **Photo** or **Text** now.\n"
        "__I will process the very next message you send.__",
        quote=True
    )

@Client.on_message(filters.photo & filters.private & has_active_session)
async def photo_handler(client: Client, message: Message):
    user_sessions.discard(message.from_user.id)
    msg = await message.reply_text("**Processing Photo... 0%**", quote=True)
    
    file = None
    location = f"./downloads/{message.from_user.id}_{int(time.time())}/"

    try:
        file = await message.download(location, progress=simple_progress, progress_args=(msg,))
        await msg.edit("**__☁️ Uploading...__**")
        
        media_data = upload_file(file)
        if not media_data:
            await msg.edit("**⚠️ Upload Failed.**")
            return

        buttons = [[InlineKeyboardButton("🌐 Vɪᴇᴡ Iᴍᴀɢᴇ", url=media_data["url"])]]
        if media_data.get("delete_url"):
            buttons.append([InlineKeyboardButton("🗑️ Dᴇʟᴇᴛᴇ", url=media_data["delete_url"])])

        await msg.edit(
            f"✅ **Upload Successful!**\n🔗 `{media_data['url']}`\n📡 Provider: `{media_data['provider']}`",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except Exception as e:
        await msg.edit(f"**Error:** {e}")
    finally:
        last_update_time.pop(msg.id, None)
        if file and os.path.exists(file): os.remove(file)
        if os.path.exists(location): os.rmdir(location)

@Client.on_message(filters.text & filters.private & has_active_session)
async def text_handler(client: Client, message: Message):
    user_sessions.discard(message.from_user.id)
    msg = await message.reply_text("**Processing Text...⏳**", quote=True)

    try:
        user = Telegraph(domain=DOMAIN).create_account(short_name="@NeonFiles")
        content = message.text.html
        content = re.sub(EMOJI_PATTERN, "", content).replace("</emoji>", "")

        title_match = re.findall(TITLE_PATTERN, content)
        if title_match:
            title = title_match[0]
            content = "\n".join(content.splitlines()[1:])
        else:
            title = message.from_user.first_name

        content = content.replace("\n", "<br>")
        
        response = Telegraph(domain=DOMAIN, access_token=user.get("access_token")).create_page(
            title=title,
            html_content=content,
            author_name=str(message.from_user.first_name),
            author_url=f"https://t.me/{message.from_user.username}" if message.from_user.username else None
        )
        
        await msg.edit(f"**https://{DOMAIN}/{response['path']}**")
    except Exception as e:
        await msg.edit(f"**Error:** {e}")
