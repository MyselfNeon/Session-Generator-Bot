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
_initialized = False  # Prevent re-initialization


# ========================
# INIT FUNCTION
# ========================
async def init_monitor(bot: Client):
    """Initialize DB and reload all monitors."""
    global db, _initialized
    if _initialized:
        return  # avoid double init if plugins reload

    client = AsyncIOMotorClient(MONGO_DB_URI)
    db = client["neon_monitor"]

    async for doc in db.monitors.find():
        url = doc["url"]
        if url not in running_tasks:
            running_tasks[url] = asyncio.create_task(ping_url(bot, url))

    logging.info(f"✅ Loaded {len(running_tasks)} monitors from DB.")
    _initialized = True


# ========================
# PING FUNCTION
# ========================
async def ping_url(bot: Client, url: str):
    """Continuously ping a URL and send alerts."""
    global monitor_interval
    notify_ids = {BOSS_ID, OWNER_ID}

    async with aiohttp.ClientSession() as session:
        while True:
            try:
                async with session.get(url, timeout=10) as resp:
                    if resp.status == 200:
                        if status_cache.get(url) == "down":
                            for uid in notify_ids:
                                await bot.send_message(
                                    uid,
                                    f"✅ <b>{url}</b> is <b>back online!</b> 🎉",
                                    parse_mode="html"
                                )
                        status_cache[url] = "up"
                        failure_counts[url] = 0
                    else:
                        await handle_failure(bot, url, f"HTTP {resp.status}", notify_ids)
            except Exception as e:
                await handle_failure(bot, url, str(e), notify_ids)

            await asyncio.sleep(monitor_interval)


async def handle_failure(bot, url, error, notify_ids):
    """Handle repeated failures before alerting."""
    failure_counts[url] = failure_counts.get(url, 0) + 1

    if failure_counts[url] == 3 and status_cache.get(url) != "down":
        status_cache[url] = "down"
        for uid in notify_ids:
            await bot.send_message(
                uid,
                f"❌ <b>{url}</b> seems <b>DOWN!</b>\nError: <code>{error}</code>",
                parse_mode="html"
            )


# ========================
# COMMANDS
# ========================
@Client.on_message(filters.command("malive"))
async def malive_cmd(bot, message):
    """Add a new URL to monitor."""
    global db
    await init_monitor(bot)

    if len(message.command) < 2:
        return await message.reply(
            "⚙️ Usage: <code>/malive &lt;url&gt;</code>",
            quote=True,
            parse_mode="html"
        )

    url = message.text.split(maxsplit=1)[1].strip()
    existing = await db.monitors.find_one({"url": url})
    if existing:
        return await message.reply(
            "⚠️ This URL is already being monitored.",
            parse_mode="html"
        )

    await db.monitors.insert_one({"url": url})
    running_tasks[url] = asyncio.create_task(ping_url(bot, url))
    await message.reply(
        f"✅ Now monitoring:\n<code>{url}</code>",
        parse_mode="html"
    )


@Client.on_message(filters.command("msee"))
async def msee_cmd(bot, message):
    """See all saved monitor URLs."""
    global db
    await init_monitor(bot)

    urls = [doc async for doc in db.monitors.find()]
    if not urls:
        return await message.reply("❌ No URLs are being monitored yet.", parse_mode="html")
    msg = "🔍 <b>Monitored URLs:</b>\n" + "\n".join(
        [f"{i+1}. <code>{doc['url']}</code>" for i, doc in enumerate(urls)]
    )
    await message.reply(msg, parse_mode="html")


@Client.on_message(filters.command("mstatus"))
async def mstatus_cmd(bot, message):
    """Show runtime monitoring status."""
    await init_monitor(bot)

    if not running_tasks:
        return await message.reply("❌ No running monitors.", parse_mode="html")
    msg = "🧠 <b>Monitor Status:</b>\n"
    for i, url in enumerate(running_tasks.keys(), start=1):
        stat = status_cache.get(url, "checking")
        emoji = "✅" if stat == "up" else ("❌" if stat == "down" else "⚙️")
        msg += f"{i}. {emoji} <code>{url}</code> - {stat.upper()}\n"
    await message.reply(msg, parse_mode="html")


@Client.on_message(filters.command("mtime"))
async def mtime_cmd(bot, message):
    """Show and set monitor interval."""
    global monitor_interval
    buttons = InlineKeyboardMarkup(
        [[InlineKeyboardButton("⏱ Change Time", callback_data="change_time")]]
    )
    await message.reply(
        f"⏲ Current monitor interval: <b>{monitor_interval} sec</b>",
        reply_markup=buttons,
        parse_mode="html"
    )


@Client.on_callback_query(filters.regex("change_time"))
async def change_time_cb(bot, query):
    await query.message.reply(
        "🕒 Send the new monitor interval in <b>seconds</b> (e.g., 600)",
        parse_mode="html"
    )


@Client.on_message(filters.private & filters.regex(r"^\d+$"))
async def time_setter(bot, message):
    """Set new monitor time if numeric value received."""
    global monitor_interval
    if message.text.isdigit():
        monitor_interval = int(message.text)
        await message.reply(
            f"✅ Monitor interval updated to <b>{monitor_interval}</b> seconds.",
            parse_mode="html"
        )


@Client.on_message(filters.command("mdel"))
async def mdel_cmd(bot, message):
    """Delete a monitored URL."""
    global db
    await init_monitor(bot)

    urls = [doc async for doc in db.monitors.find()]
    if not urls:
        return await message.reply("❌ No URLs found to delete.", parse_mode="html")

    msg = "🗑 <b>Select URL number(s) to delete:</b>\n"
    for i, doc in enumerate(urls, 1):
        msg += f"{i}. <code>{doc['url']}</code>\n"
    msg += "\nSend numbers separated by commas (e.g., <code>1,3</code>)"

    await message.reply(msg, parse_mode="html")


@Client.on_message(filters.regex(r"^\d+(,\d+)*$"))
async def delete_selected(bot, message):
    """Process user’s delete selection."""
    global db
    await init_monitor(bot)

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
            "\n".join(f"• <code>{u}</code>" for u in deleted),
            parse_mode="html"
        )
    else:
        await message.reply("⚠️ No valid URLs to delete.", parse_mode="html")
