# user_tracker_standalone.py
from pyrogram import Client, filters
from pyrogram.types import Message
from pymongo import MongoClient
from config import MONGO_DB_URI
import json

# MongoDB setup
mongo_client = MongoClient(MONGO_DB_URI)
db = mongo_client["MyselfNeon"]
users_collection = db["saverestricted_users"]

def register_user(user):
    """Register user if not already in DB."""
    if not users_collection.find_one({"id": user.id}):
        users_collection.insert_one({
            "name": user.first_name or "",
            "username": user.username or "None",
            "id": user.id
        })

def get_all_users():
    """Return all users as list."""
    users = list(users_collection.find({}, {"_id": 0}))
    return users

# --- Automatic registration for any message ---
@Client.on_message(filters.private)
async def auto_register_user(client: Client, message: Message):
    """Auto-register any user who sends a private message."""
    register_user(message.from_user)

# --- Command to check all users ---
@Client.on_message(filters.private & filters.command("users", prefixes="/"))
async def users_handler(client: Client, message: Message):
    """Send list of all users + JSON file."""
    users = get_all_users()
    total = len(users)
    text = f"List of all Users are Below -\n👥 Total Registered Users: {total}"
    await message.reply_text(text)
    
    # Send JSON file
    users_json = json.dumps(users, indent=2, ensure_ascii=False)
    await message.reply_document(
        document=bytes(users_json, "utf-8"),
        file_name="SaveRestricted.json"
    )
