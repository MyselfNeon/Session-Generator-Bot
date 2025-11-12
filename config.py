# ---------------------------------------------------
# File Name: config.py
# Author: NeonAnurag
# GitHub: https://github.com/MyselfNeon/
# Telegram: https://t.me/MyelfNeon
# Created: 2025-11-21
# Last Modified: 2025-11-22
# Version: Latest
# License: MIT License
# ---------------------------------------------------

from os import environ

# Telegram Account Api Id And Api Hash
API_ID = int(environ.get("API_ID", ""))
API_HASH = environ.get("API_HASH", "")

# Your Main Bot Token 
BOT_TOKEN = environ.get("BOT_TOKEN", "")

# Owner ID For Broadcasting 
OWNER_ID = int(environ.get("OWNER_ID", "841851780")) # Owner Id or Admin Id

# Give Your Force Subscribe Channel Id Below And Make Bot Admin With Full Right.
F_SUB = environ.get("F_SUB", "-1002384933640")

# Mongodb Database Uri For User Data Store 
MONGO_DB_URI = environ.get("MONGO_DB_URI", "")

# Log channel ID for restart and new user logs
LOG_CHANNEL = -1001889915480

# Port To Run Web Application 
PORT = int(environ.get('PORT', 8080))

# Keep-Alive URL
KEEP_ALIVE_URL = environ.get("KEEP_ALIVE_URL", "")  # <-- Add this line


# MyselfNeon
# Don't Remove Credit 🥺
# Telegram Channel @NeonFiles
