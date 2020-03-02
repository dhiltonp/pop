import time


def __init__(hub):
    hub.mods.dmap.DMAP = hub.pop.data.dmap()


def collect_setitem(hub):
    hub.mods.dmap.load_setitem()


def load_setitem(hub):
    hub.mods.dmap.DMAP["item"] = "value"


def collect_setattr(hub):
    hub.mods.dmap.load_setattr()


def load_setattr(hub):
    hub.mods.dmap.DMAP.item = "value"


def collect_setitem_nested(hub):
    hub.mods.dmap.load_setitem_nested()


def load_setitem_nested(hub):
    hub.mods.dmap.DMAP["item"] = {"a": {"b": {}}}


def collect_setattr_nested(hub):
    hub.mods.dmap.load_setattr_nested()


def load_setattr_nested(hub):
    hub.mods.dmap.DMAP.item.a.b = {}


def collect_time(hub):
    hub.mods.dmap.load_time()


def load_time(hub):
    hub.mods.dmap.DMAP.time = time.time()


async def acollect_time(hub):
    await hub.mods.dmap.aload_time()


async def aload_time(hub):
    hub.mods.dmap.DMAP.time = time.time()
