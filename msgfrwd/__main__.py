import json

from .dbf import *
from telethon import events
from telethon.tl.types import User


async def start_bot(token: str) -> None:
    await client.start(bot_token=token)
    client.me = await client.get_me()
    print(client.me.username, "is Online Now.")


client.loop.run_until_complete(start_bot(BOT_TOKEN))


@client.on(events.NewMessage(incoming=True, pattern="\\/start"))
async def starters(event):
    await event.reply("Hello")


async def check_ch(chats):
    ch = []
    for chat in chats:
        try:
            chat = int(chat)
        except:
            pass
        ch.append((await client.get_entity(chat)).id)
    return chats


@client.on(events.NewMessage(incoming=True, pattern="\\/forward"))
async def frwd(e):
    texts = [x for x in e.text.split(maxsplit=3) if x]
    fnc = texts[1].lower()
    if not ("add" in fnc or "del" in fnc):
        return
    name = texts[2].lower()
    if "add" in fnc:
        if await get_by_name(name):
            return await e.reply(
                f"Name: __{name}__ already exists, Delete it or use diff name."
            )
        sc, ds = texts[3].split("->")
        sc = await check_ch([s.strip() for s in sc.strip().split(",") if s])
        ds = await check_ch([d.strip() for d in ds.strip().split(",") if d])
        await add_new(name, sc, ds)
        await e.reply("Added Successfully")
    elif "del" in fnc:
        await del_db(name)
        await e.reply("Deleted Successfully")


@client.on(events.NewMessage(incoming=True, pattern="\\/get ?(.*)"))
async def gt(e):
    name = (e.pattern_match.group(1) or "").strip().lower()
    if name:
        data = get_by_name(name)
        if not data:
            return await e.reply(f"No data for {name}")
        return await e.reply(json.dumps(data, indent=4))
    data = await get_db()
    return await e.reply(json.dumps(data, indent=4)[:4096])


@client.on(events.NewMessage(incoming=True))
async def de(e: events.NewMessage.Event):
    if e.fwd_from or not e.chat or isinstance(e.chat, User):
        return
    dst = await get_lists(e.chat.id)
    if dst:
        send = []
        for chat in dst:
            try:
                if chat in send:
                    continue
                await e.message.forward_to(chat)
                send.append(chat)
            except BaseException:
                pass


client.run_until_disconnected()


# ➡️ One to One Chat
# /forward add work1 22222 -> 66666

# ➡️ Many to One Chat
# /forward add work1 22222,33333 -> 66666

# ➡️ One to Many Chat
# /forward add work1 22222 -> 66666,77777

# ➡️ Many to Many Chat
# /forward add work1 22222,33333 -> 66666,77777
