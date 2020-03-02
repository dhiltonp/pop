import collections.abc as abc
import pop.contract as contract
import pop.hub
import pop.exc
import pytest


@pytest.fixture(scope="function")
def hub():
    hub = pop.hub.Hub()
    hub.pop.sub.add("tests.integration.data.mods")
    yield hub


class TestDynamicMutableNamespacedMap:
    def test_setitem(self, hub):
        hub.mods.dmap.collect_setitem()
        # Verify that the value was set
        assert hub.mods.dmap.DMAP._store["item"] == "value"

        # Verify that the contract was stored
        assert isinstance(hub.mods.dmap.DMAP._ref["item"], contract.Contracted)
        assert hub.mods.dmap.DMAP._ref["item"].ref == "mods.dmap"
        assert hub.mods.dmap.DMAP._ref["item"].name == "load_setitem"

    def test_setitem_nested_dict(self, hub):
        hub.mods.dmap.collect_setitem_nested()

        # Verify that the values were set
        assert hub.mods.dmap.DMAP._store["item"] == {"a": {"b": {}}}

        # Verify that the dictionaries were all transformed into DMAPs
        assert isinstance(hub.mods.dmap.DMAP._store["item"], abc.MutableMapping)
        assert isinstance(
            hub.mods.dmap.DMAP._store["item"]._store["a"], abc.MutableMapping
        )
        assert isinstance(
            hub.mods.dmap.DMAP._store["item"]._store["a"]._store["b"],
            abc.MutableMapping,
        )

        # Verify that they all share the same contract
        assert isinstance(hub.mods.dmap.DMAP._ref["item"], contract.Contracted)
        assert hub.mods.dmap.DMAP._ref["item"].name == "load_setitem_nested"

        assert isinstance(
            hub.mods.dmap.DMAP._store["item"]._ref["a"], contract.Contracted
        )
        assert hub.mods.dmap.DMAP._store["item"]._ref["a"].name == "load_setitem_nested"

        assert isinstance(
            hub.mods.dmap.DMAP._store["item"]._store["a"]._ref["b"], contract.Contracted
        )
        assert (
            hub.mods.dmap.DMAP._store["item"]._store["a"]._ref["b"].name
            == "load_setitem_nested"
        )

        assert isinstance(
            hub.mods.dmap.DMAP._store["item"]._store["a"]._store["b"]._parent_ref,
            contract.Contracted,
        )
        assert (
            hub.mods.dmap.DMAP._store["item"]._store["a"]._store["b"]._parent_ref.name
            == "load_setitem_nested"
        )

    def test_delitem(self, hub):
        hub.mods.dmap.collect_setitem()
        del hub.mods.dmap.DMAP["item"]
        assert "item" not in hub.mods.dmap.DMAP._store
        assert "item" not in hub.mods.dmap.DMAP._ref

    def test_setattr(self, hub):
        hub.mods.dmap.collect_setattr()
        # Verify that the value was set
        assert hub.mods.dmap.DMAP._store["item"] == "value"

        # Verify that the contract was stored
        assert isinstance(hub.mods.dmap.DMAP._ref["item"], contract.Contracted)
        assert hub.mods.dmap.DMAP._ref["item"].ref == "mods.dmap"
        assert hub.mods.dmap.DMAP._ref["item"].name == "load_setattr"

    def test_setattr_create_nest(self, hub):
        hub.mods.dmap.collect_setattr_nested()

        # Verify that the dictionaries were all transformed into DMAPs
        assert isinstance(hub.mods.dmap.DMAP._store["item"], abc.MutableMapping)
        assert isinstance(
            hub.mods.dmap.DMAP._store["item"]._store["a"], abc.MutableMapping
        )
        assert isinstance(
            hub.mods.dmap.DMAP._store["item"]._store["a"]._store["b"],
            abc.MutableMapping,
        )

        assert isinstance(hub.mods.dmap.DMAP._ref["item"], contract.Contracted)
        assert hub.mods.dmap.DMAP._ref["item"].name == "load_setattr_nested"

        assert isinstance(
            hub.mods.dmap.DMAP._store["item"]._ref["a"], contract.Contracted
        )
        assert hub.mods.dmap.DMAP._store["item"]._ref["a"].name == "load_setattr_nested"

        assert isinstance(
            hub.mods.dmap.DMAP._store["item"]._store["a"]._ref["b"], contract.Contracted
        )
        assert (
            hub.mods.dmap.DMAP._store["item"]._store["a"]._ref["b"].name
            == "load_setattr_nested"
        )

        assert isinstance(
            hub.mods.dmap.DMAP._store["item"]._store["a"]._store["b"]._parent_ref,
            contract.Contracted,
        )
        assert (
            hub.mods.dmap.DMAP._store["item"]._store["a"]._store["b"]._parent_ref.name
            == "load_setattr_nested"
        )

    @pytest.mark.asyncio
    async def test_refresh(self, hub):
        await hub.mods.dmap.acollect_time()

        time = hub.mods.dmap.DMAP.time
        await hub.mods.dmap.DMAP.refresh("time")
        assert time != hub.mods.dmap.DMAP.time

    @pytest.mark.asyncio
    async def test_synchronous_refresh(self, hub):
        hub.mods.dmap.collect_time()

        time = hub.mods.dmap.DMAP.time
        hub.mods.dmap.DMAP.refresh("time")
        assert time != hub.mods.dmap.DMAP.time
