import asyncio, os, tempfile, shutil, math, random, string
from pathlib import Path
from urllib.parse import urljoin, urlparse
import aiohttp
from pyrogram import Client, filters
from pyrogram.types import Message

CONCURRENT_DOWNLOADS = 6
SEGMENT_RETRIES = 3
DOWNLOAD_CHUNK = 64*1024
ACTIVE_TASKS = {}

def _short_id(n=5):
    return ''.join(random.choices(string.ascii_uppercase+string.digits, k=n))

async def download_segment(session, url, dest, sem, cancel_event):
    attempt=0
    while attempt<SEGMENT_RETRIES and not cancel_event.is_set():
        try:
            async with sem:
                async with session.get(url, timeout=60) as r:
                    r.raise_for_status()
                    with open(dest,"wb") as f:
                        async for c in r.content.iter_chunked(DOWNLOAD_CHUNK):
                            if cancel_event.is_set(): return False
                            f.write(c)
            return True
        except: attempt+=1; await asyncio.sleep(1+attempt)
    return False

def ffmpeg_path():
    path = shutil.which("ffmpeg")
    if not path: raise RuntimeError("ffmpeg not found in PATH")
    return path

async def merge_ffmpeg(input_m3u8, output_file, cancel_event):
    ff = ffmpeg_path()
    proc = await asyncio.create_subprocess_exec(ff, "-y","-allowed_extensions","ALL","-i",str(input_m3u8),"-c","copy",str(output_file))
    while proc.returncode is None:
        if cancel_event.is_set(): proc.kill(); await proc.wait(); raise asyncio.CancelledError()
        await asyncio.sleep(0.5)
    stdout, stderr = await proc.communicate()
    if proc.returncode !=0: raise RuntimeError(f"ffmpeg failed: {stderr.decode(errors='ignore')}")

async def m3u8_to_mp4(url, workdir, filename=None, progress_cb=None, cancel_event=None):
    cancel_event = cancel_event or asyncio.Event()
    async with aiohttp.ClientSession() as session:
        txt = await (await session.get(url)).text()
        lines = [l.strip() for l in txt.splitlines() if l.strip()]
        segs = []
        for i,l in enumerate(lines):
            if l.startswith("#EXTINF"):
                for j in range(i+1,min(i+4,len(lines))):
                    if not lines[j].startswith("#"): segs.append(lines[j]); break
        if not segs:
            for l in lines:
                if not l.startswith("#"): segs.append(l)
        total = len(segs)
        if progress_cb: await progress_cb("queued",0,total)
        sem = asyncio.Semaphore(CONCURRENT_DOWNLOADS)
        local_files=[]
        tasks=[]
        workdir.mkdir(parents=True,exist_ok=True)
        for idx,s in enumerate(segs):
            u = urljoin(url,s)
            dest = workdir/f"seg_{idx:05d}.ts"
            local_files.append(dest.name)
            tasks.append((u,dest))
        done=0
        async def worker(it):
            nonlocal done
            u,d = it
            ok = await download_segment(session,u,d,sem,cancel_event)
            done+=1
            if progress_cb: await progress_cb("downloading",done,total)
            return ok
        results = await asyncio.gather(*[worker(it) for it in tasks], return_exceptions=True)
        if cancel_event.is_set(): raise asyncio.CancelledError()
        for r in results:
            if r is False or isinstance(r,Exception): raise RuntimeError("Segment failed")
        lp = workdir/"playlist.m3u8"
        with open(lp,"w") as f:
            f.write("#EXTM3U\n#EXT-X-VERSION:3\n")
            for n in local_files: f.write(f"#EXTINF:0.0,\n{n}\n")
            f.write("#EXT-X-ENDLIST\n")
        if progress_cb: await progress_cb("merging",0,1)
        out_name = filename or (Path(urlparse(url).path).stem or "output")
        out_file = workdir/f"{out_name}.mp4"
        await merge_ffmpeg(lp,out_file,cancel_event)
        if progress_cb: await progress_cb("done",1,1)
        return out_file

@Client.on_message(filters.command("m3u8"))
async def cmd_m3u8(c:Client,m:Message):
    args = m.text.split(maxsplit=2)
    url=None; filename=None
    if len(args)>=2: url=args[1].strip()
    if len(args)==3: filename=args[2].strip()
    elif m.reply_to_message and m.reply_to_message.text:
        for p in m.reply_to_message.text.split():
            if p.startswith("http") and "m3u8" in p: url=p; break
    if not url: await m.reply_text("Usage: /m3u8 <m3u8_link> [filename]"); return
    task_id = _short_id()
    tempdir = Path(tempfile.mkdtemp(prefix=f"m3u8_{task_id}_"))
    cancel_event = asyncio.Event()
    ACTIVE_TASKS[task_id]=cancel_event
    status = await m.reply_text(f"Task {task_id} queued...")
    async def progress(phase,done,total):
        if phase=="queued": t=f"Found {total} segments..."
        elif phase=="downloading": t=f"Downloading {done}/{total} ({math.floor(done/total*100)}%)\nTask ID: {task_id}\n/cancel {task_id}"
        elif phase=="merging": t=f"Merging segments..."
        elif phase=="done": t=f"Finished. Uploading..."
        else: t=f"{phase} {done}/{total}"
        try: await status.edit_text(t)
        except: pass
    try:
        out_file = await m3u8_to_mp4(url,tempdir,filename,progress,cancel_event)
        await status.edit_text("Uploading video...")
        await c.send_video(m.chat.id,str(out_file),caption=f"{out_file.name} | from {url}")
        await status.delete()
    except asyncio.CancelledError:
        await status.edit_text(f"Task {task_id} canceled.")
    except Exception as e:
        await status.edit_text(f"Error: {e}")
    finally:
        del ACTIVE_TASKS[task_id]
        shutil.rmtree(tempdir,ignore_errors=True)

@Client.on_message(filters.command("cancel"))
async def cancel_task(c:Client,m:Message):
    args = m.text.split(maxsplit=1)
    if len(args)!=2: await m.reply_text("Usage: /cancel <TaskID>"); return
    tid = args[1].strip().upper()
    if tid in ACTIVE_TASKS:
        ACTIVE_TASKS[tid].set()
        await m.reply_text(f"Task {tid} cancellation requested.")
    else: await m.reply_text(f"Task {tid} not found or already finished.")
