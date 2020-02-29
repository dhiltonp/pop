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


@pytest.mark.asyncio
async def test_async_simple_contracts():
    hub = pop.hub.Hub()
    hub.pop.sub.add("tests.coro", "coro")
    ret = await hub.coro.test.simple()
    assert ret == True
    assert hub.PRE
    assert hub.POST


@pytest.mark.asyncio
async def test_async_generator_contracts():
    hub = pop.hub.Hub()
    hub.pop.sub.add("tests.coro", "coro")
    inum = 0
    async for num in hub.coro.test.gen():
        assert num == inum
        inum += 1
    assert hub.PRE
    assert hub.POST
