import asyncio
import aiohttp
import logging
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_DB_URI, OWNER_ID

# ========================
# CONSTANTS
# ========================
BOSS_ID = 841851780  # Universal boss — always notified
DEFAULT_INTERVAL = 500  # seconds

# Runtime caches
status_cache = {}      # {url: "up"/"down"}
failure_counts = {}    # {url: consecutive_failures}
running_tasks = {}     # {url: asyncio.Task}
monitor_interval = DEFAULT_INTERVAL
db = None


# ========================
# INIT ON STARTUP
# ========================
@Client.on_startup()
async def init_monitor(bot: Client):
    """Initialize MongoDB and resume all monitors."""
    global db
    client = AsyncIOMotorClient(MONGO_DB_URI)
    db = client["neon_monitor"]

    # Resume previous monitors
    async for doc in db.monitors.find():
        url = doc["url"]
        if url not in running_tasks:
            running_tasks[url] = asyncio.create_task(ping_url(bot, url))

    logging.info(f"✅ Loaded {len(running_tasks)} active monitors.")


# ========================
# CORE PING FUNCTION
# ========================
async def ping_url(bot: Client, url: str):
    """Ping a URL repeatedly and alert when status changes."""
    global monitor_interval
    notify_ids = {BOSS_ID, OWNER_ID}

    async with aiohttp.ClientSession() as session:
        while True:
            try:
                async with session.get(url, timeout=10) as resp:
                    if resp.status == 200:
                        # Back online case
                        if status_cache.get(url) == "down":
                            for uid in notify_ids:
                                await bot.send_message(
                                    uid,
                                    f"✅ [{url}] is **back online!** 🎉"
                                )
                        status_cache[url] = "up"
                        failure_counts[url] = 0
                    else:
                        await handle_failure(bot, url, f"HTTP {resp.status}", notify_ids)
            except Exception as e:
                await handle_failure(bot, url, str(e), notify_ids)

            await asyncio.sleep(monitor_interval)


async def handle_failure(bot, url, error, notify_ids):
    """Handle URL failure and notify after repeated errors."""
    failure_counts[url] = failure_counts.get(url, 0) + 1

    # Alert after 3 consecutive failures
    if failure_counts[url] == 3 and status_cache.get(url) != "down":
        status_cache[url] = "down"
        for uid in notify_ids:
            await bot.send_message(
                uid,
                f"❌ [{url}] seems **DOWN!**\nError: `{error}`"
            )


# ========================
# COMMANDS
# ========================

@Client.on_message(filters.command("malive"))
async def malive_cmd(bot, message):
    """Add a new URL to monitor."""
    global db
    if len(message.command) < 2:
        return await message.reply("⚙️ Usage: `/malive <url>`", quote=True)

    url = message.text.split(maxsplit=1)[1].strip()
    existing = await db.monitors.find_one({"url": url})
    if existing:
        return await message.reply("⚠️ This URL is already being monitored.")

    await db.monitors.insert_one({"url": url})
    running_tasks[url] = asyncio.create_task(ping_url(bot, url))
    await message.reply(f"✅ Now monitoring:\n`{url}`")


@Client.on_message(filters.command("msee"))
async def msee_cmd(bot, message):
    """List all monitored URLs."""
    global db
    urls = [doc async for doc in db.monitors.find()]
    if not urls:
        return await message.reply("❌ No URLs are being monitored yet.")
    msg = "🔍 **Monitored URLs:**\n" + "\n".join(
        [f"{i+1}. `{doc['url']}`" for i, doc in enumerate(urls)]
    )
    await message.reply(msg)


@Client.on_message(filters.command("mstatus"))
async def mstatus_cmd(bot, message):
    """Show current monitor status."""
    if not running_tasks:
        return await message.reply("❌ No running monitors.")
    msg = "🧠 **Monitor Status:**\n"
    for i, url in enumerate(running_tasks.keys(), start=1):
        stat = status_cache.get(url, "checking")
        emoji = "✅" if stat == "up" else ("❌" if stat == "down" else "⚙️")
        msg += f"{i}. {emoji} `{url}` - {stat.upper()}\n"
    await message.reply(msg)


@Client.on_message(filters.command("mtime"))
async def mtime_cmd(bot, message):
    """Display and update monitor interval."""
    global monitor_interval
    buttons = InlineKeyboardMarkup(
        [[InlineKeyboardButton("⏱ Change Time", callback_data="change_time")]]
    )
    await message.reply(
        f"⏲ Current monitor interval: **{monitor_interval} sec**",
        reply_markup=buttons
    )


@Client.on_callback_query(filters.regex("change_time"))
async def change_time_cb(bot, query):
    await query.message.reply(
        "🕒 Send the new monitor interval in **seconds** (e.g., 600)"
    )


@Client.on_message(filters.text & filters.private)
async def time_setter(bot, message):
    """Set monitor interval if numeric value is sent."""
    global monitor_interval
    if message.text.isdigit():
        monitor_interval = int(message.text)
        await message.reply(f"✅ Monitor interval updated to {monitor_interval} seconds.")


@Client.on_message(filters.command("mdel"))
async def mdel_cmd(bot, message):
    """List monitored URLs to delete."""
    global db
    urls = [doc async for doc in db.monitors.find()]
    if not urls:
        return await message.reply("❌ No URLs found to delete.")

    msg = "🗑 **Select URL number(s) to delete:**\n"
    for i, doc in enumerate(urls, 1):
        msg += f"{i}. `{doc['url']}`\n"
    msg += "\nSend numbers separated by commas (e.g., `1,3`)"

    await message.reply(msg)


@Client.on_message(filters.regex(r"^\d+(,\d+)*$"))
async def delete_selected(bot, message):
    """Delete monitors based on user selection."""
    global db
    urls = [doc async for doc in db.monitors.find()]
    indexes = [int(i) - 1 for i in message.text.split(",") if i.isdigit()]
    deleted = []

    for i in indexes:
        if 0 <= i < len(urls):
            url = urls[i]["url"]
            await db.monitors.delete_one({"url": url})
            task = running_tasks.pop(url, None)
            if task:
                task.cancel()
            status_cache.pop(url, None)
            failure_counts.pop(url, None)
            deleted.append(url)

    if deleted:
        await message.reply(
            "🧹 Deleted and stopped monitoring:\n" +
            "\n".join(f"• `{u}`" for u in deleted)
        )
    else:
        await message.reply("⚠️ No valid URLs to delete.")
