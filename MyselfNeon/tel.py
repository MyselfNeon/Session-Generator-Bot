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

# --- Constants & State ---
DOMAIN = "graph.org"  # Hardcoded domain
EMOJI_PATTERN = re.compile(r'<emoji id="\d+">')
TITLE_PATTERN = re.compile(r"title:? (.*)", re.IGNORECASE)

# This set stores the User IDs of people who have sent /tel
user_sessions = set()
# Tracker to prevent FloodWait errors (stores last edit time)
last_update_time = {}

# --- Custom Filter ---
async def check_session_func(_, __, message):
    """Check if the user has activated the bot via /tel"""
    return message.from_user and message.from_user.id in user_sessions

has_active_session = filters.create(check_session_func)

# --- Simple Progress Function (Local) ---
async def simple_progress(current, total, message):
    """
    Edits the message with simple percentage text.
    Updates only every 3 seconds to avoid FloodWait.
    """
    percentage = current * 100 / total
    now = time.time()
    
    # Get last update time for this specific message
    last_time = last_update_time.get(message.id, 0)

    # Update if 3 seconds passed OR download is complete (100%)
    if now - last_time > 3 or current == total:
        last_update_time[message.id] = now
        try:
            await message.edit(f"**Downloading... {int(percentage)}%**")
        except Exception:
            pass # Ignore errors if message was deleted or unchanged

# --- Helper Function: Upload Logic ---
def upload_file(file_path):
    # Fetch API Key directly from OS Environment
    imgbb_key = os.getenv("IMGBB_API_KEY")
    
    # 1. Try ImgBB
    if imgbb_key:
        try:
            with open(file_path, "rb") as f:
                response = requests.post(
                    "https://api.imgbb.com/1/upload",
                    params={"key": imgbb_key},
                    files={"image": f},
                    timeout=60,
                )
            if response.ok:
                data = response.json()["data"]
                return {"provider": "imgbb", "url": data["url"], "delete_url": data.get("delete_url")}
        except Exception as e:
            logger.error(f"ImgBB Error: {e}")

    # 2. Fallback to Envs.sh
    try:
        with open(file_path, "rb") as f:
            response = requests.post("https://envs.sh", files={"file": f}, timeout=60)
        if response.ok:
            return {"provider": "envs.sh", "url": response.text.strip()}
    except Exception as e:
        logger.error(f"Envs.sh Error: {e}")
        return None


# --- Handler 1: The Activation Command (/tel) ---
@Client.on_message(filters.command("tel") & filters.private)
async def ask_content_handler(client: Client, message: Message):
    """Activates the session for the user."""
    user_id = message.from_user.id
    user_sessions.add(user_id)
    
    await message.reply_text(
        "**✅ Mode Activated!**\n\n"
        "Please send the **Photo** (to upload) or **Text** (for Telegraph) now.\n"
        "__I will only process the next message you send.__",
        quote=True
    )


# --- Handler 2: Image Upload (Only runs if has_active_session) ---
@Client.on_message(filters.photo & filters.private & has_active_session)
async def photo_handler(client: Client, message: Message):
    
    user_sessions.discard(message.from_user.id) # Remove from session

    msg = await message.reply_text("**Processing Photo... 0%**", quote=True)
    
    file = None
    location = f"./downloads/{message.from_user.id}_{int(time.time())}/"

    try:
        # Pass simple_progress function here
        file = await message.download(
            location, 
            progress=simple_progress, 
            progress_args=(msg,)
        )
        
        await msg.edit("**__☁️ Uploading to Cloud...__**")
        media_data = upload_file(file)

        if not media_data:
            await msg.edit("**⚠️ Upload Failed.**")
            return

        buttons = [[InlineKeyboardButton("🌐 Vɪᴇᴡ Iᴍᴀɢᴇ", url=media_data["url"])]]
        if media_data.get("delete_url"):
            buttons.append([InlineKeyboardButton("🗑️ Dᴇʟᴇᴛᴇ", url=media_data["delete_url"])])

        text = (
            f"✅ **Upload Successful!**\n"
            f"🔗 `{media_data['url']}`\n"
            f"📡 Provider: `{media_data['provider']}`"
        )
        await msg.edit(text, reply_markup=InlineKeyboardMarkup(buttons))

    except Exception as e:
        logger.error(e)
        await msg.edit(f"**Error:** {e}")
    finally:
        # Clean up memory dict
        last_update_time.pop(msg.id, None)
        # Clean up files
        if file and os.path.exists(file): os.remove(file)
        if os.path.exists(location): os.rmdir(location)


# --- Handler 3: Text to Telegraph (Only runs if has_active_session) ---
@Client.on_message(filters.text & filters.private & has_active_session)
async def text_handler(client: Client, message: Message):
    
    user_sessions.discard(message.from_user.id) # Remove from session

    msg = await message.reply_text("**Processing Text....⏳**", quote=True)

    try:
        short_name = "@NeonFiles"
        user = Telegraph(domain=DOMAIN).create_account(short_name=short_name)
        
        content = message.text.html
        content = re.sub(EMOJI_PATTERN, "", content).replace("</emoji>", "")

        title_match = re.findall(TITLE_PATTERN, content)
        title = title_match[0] if title_match else message.from_user.first_name
        
        if title_match:
            content = "\n".join(content.splitlines()[1:])

        content = content.replace("\n", "<br>")
        author_url = f"https://telegram.dog/{message.from_user.username}" if message.from_user.username else None

        response = Telegraph(domain=DOMAIN, access_token=user.get("access_token")).create_page(
            title=title,
            html_content=content,
            author_name=str(message.from_user.first_name),
            author_url=author_url,
        )
        
        await msg.edit(f"**https://{DOMAIN}/{response['path']}**")

    except Exception as e:
        logger.error(e)
        await msg.edit(f"**Error:** {e}")
