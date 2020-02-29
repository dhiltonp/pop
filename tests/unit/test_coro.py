# -*- coding: utf-8 -*-
# pylint: disable=expression-not-assigned

# Import third party libs
import pytest

# Import pop
import pop.hub


@pytest.mark.asyncio
async def test_asyncio_coro():
    hub = pop.hub.Hub()
    hub.pop.sub.add("tests.mods.coro", "mods")
    assert "coro" in hub.mods
    assert "asyncio_demo" in dir(hub.mods.coro)
    try:
        await hub.mods.coro.asyncio_demo()
    except Exception:
        raise
