import collections.abc as abc
import pop.hub
import pop.exc
import pytest


@pytest.fixture(scope="function")
def hub():
    hub = pop.hub.Hub()
    yield hub


class TestMutableNamespacedMap:
    def test_init(self, hub):
        """
        Verify that an init dict is loaded into the namespace
        """
        init_dict = {"1": 2, "3": 4}
        mnm = hub.pop.data.map(init_dict)
        assert mnm == init_dict

    def test_init_dict(self, hub):
        """
        Verify that a dict is converted into a mutable mapping namespace from self.update
        """
        init_dict = {"k": {}}
        mnm = hub.pop.data.map(init_dict)
        assert mnm == init_dict
        assert isinstance(mnm["k"], abc.MutableMapping)

    def test_setitem(self, hub):
        mnm = hub.pop.data.map()
        mnm["k"] = 1
        assert mnm._store["k"] == 1

    def test_setitem_nested_dict(self, hub):
        mnm = hub.pop.data.map()
        value = {"a": {"b": {"c": {}}}}
        mnm["k"] = value
        assert mnm._store["k"] == value
        assert isinstance(mnm._store["k"], abc.MutableMapping)
        assert isinstance(mnm._store["k"]["a"], abc.MutableMapping)
        assert isinstance(mnm._store["k"]["a"]["b"], abc.MutableMapping)
        assert isinstance(mnm._store["k"]["a"]["b"]["c"], abc.MutableMapping)

    def test_delitem(self, hub):
        mnm = hub.pop.data.map()
        mnm["k"] = "value"
        del mnm["k"]
        assert mnm == {}

    def test_getitem(self, hub):
        mnm = hub.pop.data.map({"k": "v"})
        assert mnm.get("k") == "v"

    def test_getattr(self, hub):
        init_dict = {"k": "v"}
        mnm = hub.pop.data.map(init_dict)
        assert mnm.k == "v"

    def test_getattr_nested(self, hub):
        d = {"d": {}}
        c = {"c": d}
        b = {"b": c}
        a = {"a": b}
        mnm = hub.pop.data.map(a)

        assert isinstance(mnm.a, abc.MutableMapping)
        assert mnm.a == b
        assert isinstance(mnm.a.b, abc.MutableMapping)
        assert mnm.a.b == c
        assert isinstance(mnm.a.b.c, abc.MutableMapping)
        assert mnm.a.b.c == d
        assert isinstance(mnm.a.b.c.d, abc.MutableMapping)
        assert mnm.a.b.c.d == {}

    def test_setattr(self, hub):
        mnm = hub.pop.data.map()
        mnm.key = "value"
        assert mnm._store["key"] == "value"

    def test_setattr_create_nest(self, hub):
        """
        verify that nested namespace values that have never been set get created when they are accessed
        """
        mnm = hub.pop.data.map()
        mnm.a.b.c = 1

        assert isinstance(mnm.a, abc.MutableMapping)
        assert "b" in mnm.a
        assert isinstance(mnm.a.b, abc.MutableMapping)
        assert "c" in mnm.a.b
        assert mnm.a.b.c == 1

    def test_len(self, hub):
        length = 100
        mnm = hub.pop.data.map({str(d): d for d in range(length)})
        assert len(mnm) == len(mnm._store) == length

    def test_str(self, hub):
        mnm = hub.pop.data.map(
            {"a": {}, "b": 1, "c": False, "d": None, "e": lambda: ""}
        )
        assert str(mnm) == str(mnm._store)


class TestDynamicMutableNamespacedMap:
    def test_init(self, hub):
        """
        Verify that an init dict is loaded into the namespace
        """
        init_dict = {"1": 2, "3": 4}
        dmap = hub.pop.data.dmap(init_dict)
        assert dmap == init_dict

    def test_init_dict(self, hub):
        """
        Verify that a dict is converted into a mutable mnmping namespace from self.update
        """
        init_dict = {"k": {}}
        dmap = hub.pop.data.dmap(init_dict)
        assert dmap == init_dict
        assert isinstance(dmap["k"], abc.MutableMapping)

    def test_setitem(self, hub):
        pass  # This is an integration test

    def test_setitem_nested_dict(self, hub):
        pass  # This is an integration test

    def test_delitem(self, hub):
        pass  # This is an integration test

    def test_getitem(self, hub):
        dmap = hub.pop.data.dmap({"k": "v"})
        assert dmap.get("k") == "v"

    def test_getattr(self, hub):
        init_dict = {"k": "v"}
        dmap = hub.pop.data.dmap(init_dict)
        assert dmap.k == "v"

    def test_getattr_nested(self, hub):
        d = {"d": {}}
        c = {"c": d}
        b = {"b": c}
        a = {"a": b}
        dmap = hub.pop.data.dmap(a)

        assert isinstance(dmap.a, abc.MutableMapping)
        assert dmap.a == b
        assert isinstance(dmap.a.b, abc.MutableMapping)
        assert dmap.a.b == c
        assert isinstance(dmap.a.b.c, abc.MutableMapping)
        assert dmap.a.b.c == d
        assert isinstance(dmap.a.b.c.d, abc.MutableMapping)
        assert dmap.a.b.c.d == {}

    def test_setattr(self, hub):
        pass  # This is an integration test

    def test_setattr_create_nest(self, hub):
        pass  # This is an integration test

    def test_len(self, hub):
        length = 100
        dmap = hub.pop.data.dmap({str(d): d for d in range(length)})
        assert len(dmap) == len(dmap._store) == length

    def test_str(self, hub):
        dmap = hub.pop.data.dmap(
            {"a": {}, "b": 1, "c": False, "d": None, "e": lambda: ""}
        )
        assert str(dmap) == str(dmap._store)

    def test_get_caller(self, hub):
        pass  # This is an integration test

    @pytest.mark.asyncio
    async def test_refresh(self, hub):
        pass  # This is an integration test
