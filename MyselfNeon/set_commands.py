# ------------------------------------------------
# File Name: Set_Commands.py
# Description: Auto Add Commands on new Deploys
# ------------------------------------------------

import asyncio
from pyrogram import Client
from pyrogram.types import BotCommand

# --- Edit This List ---
SET_COMMANDS = [
    ("start", "Check Alive Status"),
    ("generate", "Generate Session Strings"),
    ("broadcast", "Broadcast Msgs to Users")
]

# --- Internal Auto Sync Logic---
async def sync_bot_commands(app: Client):
    # 01. Wait for the Bot to Fully connect to Telegram Servers
    while not app.is_connected:
        await asyncio.sleep(1)

    print("Checking Command Sync...")

    try:
        # 02. --- Format the Commands ---
        commands = [BotCommand(cmd, desc) for cmd, desc in SET_COMMANDS]

        # 03. --- Push to Telegram ---
        await app.set_bot_commands(commands)
        
        print(f"✓ Commands Synced with Telegram: {SET_COMMANDS}")
    except Exception as e:
        print(f"✗ Failed to Sync Commands: {e}")

# --- Plugin Entry ---
def init(app: Client):
    # Runs Parallel to your Bot Starting Up
    app.loop.create_task(sync_bot_commands(app))

