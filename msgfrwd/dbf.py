from . import *

CACHE = {}


async def get_db():
    if CACHE:
        return CACHE
    data = eval((await db.get("FRWD_DB")) or "{}")
    CACHE.update(data)
    return data


async def add_new(name, sc, ds):
    a = await get_db()
    if name in a:
        return False
    a[name] = {"source": sc, "dest": ds}
    await db.set("FRWD_DB", str(a))
    CACHE.update(a)
    return True


async def del_db(name):
    a = await get_db()
    if name in a:
        a.pop(name)
        CACHE.pop(name)
        await db.set("FRWD_DB", str(a))
        return True
    return False


async def get_by_name(name):
    a = await get_db()
    return a.get(name) or {}


async def get_lists(ids):
    a = await get_db()
    dst = []
    for name in a:
        if ids in eval(str(name.get("source")) or "[]"):
            dst.extend(eval(str(name.get("dest")) or "[]"))
    return dst
