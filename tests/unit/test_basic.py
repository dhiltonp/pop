# -*- coding: utf-8 -*-
# pylint: disable=expression-not-assigned

# Import third party libs
import pytest

# Import pack
import pop.hub
import pop.exc


def test_basic():
    hub = pop.hub.Hub()
    hub.pop.sub.add("tests.mods")
    hub.mods.test.ping()
    assert hub.mods.test.ping() == {}
    assert hub.mods.test.demo() is False
    assert hub.mods.test.ping() == hub.mods.foo.bar()


def test_subdirs():
    hub = pop.hub.Hub()
    hub.pop.sub.add("tests.sdirs")
    hub.pop.sub.load_subdirs(hub.sdirs)
    assert hub.sdirs.test.ping()
    assert hub.sdirs.l11.test.ping()
    assert hub.sdirs.l12.test.ping()
    assert hub.sdirs.l13.test.ping()


def test_subdirs_recurse():
    hub = pop.hub.Hub()
    hub.pop.sub.add("tests.sdirs")
    hub.pop.sub.load_subdirs(hub.sdirs, recurse=True)
    assert hub.sdirs.test.ping()
    assert hub.sdirs.l11.test.ping()
    assert hub.sdirs.l11.l2.test.ping()
    assert hub.sdirs.l12.l2.test.ping()
    assert hub.sdirs.l13.l2.test.ping()


def test_getattr():
    hub = pop.hub.Hub()
    hub.pop.sub.add("tests.mods")
    hub.mods.test.ping()
    assert getattr(hub, "mods.test.ping")() == {}
    assert getattr(hub.mods.test, "demo")() is False
    assert hub.mods.test.ping() == getattr(hub, "mods.foo.bar")()


def test_iter_sub():
    hub = pop.hub.Hub()
    hub.pop.sub.add("tests.mods")
    mods = []
    for mod in hub.mods:
        mods.append(mod.__sub_name__)
    assert mods == sorted(hub.mods._loaded.keys())


def test_iter_subs_rec():
    hub = pop.hub.Hub()
    hub.pop.sub.add("tests.sdirs")
    hub.pop.sub.load_subdirs(hub.sdirs, recurse=True)
    subs = []
    for sub in hub.pop.sub.iter_subs(hub.sdirs, recurse=True):
        subs.append(sub._subname)
    assert subs == ["l11", "l2", "l12", "l2", "l13", "l2"]


def test_iter_loads():
    hub = pop.hub.Hub()
    hub.pop.sub.add("tests.mods.iter")
    for mod in hub.iter:
        if mod.__sub_name__ == "init":
            continue
        mod.run()
    assert hub.iter.DATA == {"bar": True, "foo": True}


def test_iter_sub_nested():
    hub = pop.hub.Hub()
    hub.pop.sub.add("tests.mods")
    mods = []
    for _ in hub.mods:
        for mod in hub.mods:
            mods.append(mod.__sub_name__)
        break
    assert mods == sorted(hub.mods._loaded.keys())


def test_iter_hub():
    hub = pop.hub.Hub()
    hub.pop.sub.add("tests.mods")
    subs = []
    for sub in hub:
        subs.append(sub._subname)
    assert subs == sorted(hub._subs.keys())


def test_iter_hub_nested():
    hub = pop.hub.Hub()
    hub.pop.sub.add("tests.mods")
    subs = []
    for _ in hub:
        for sub in hub:
            subs.append(sub._subname)
        break
    assert subs == sorted(hub._subs.keys())


def test_iter_vars():
    hub = pop.hub.Hub()
    hub.pop.sub.add("tests.mods")
    funcs = []
    for var in hub.pop.sub:
        funcs.append(var.name)
    assert funcs == sorted(hub.pop.sub._funcs.keys())


def test_iter_vars_nested():
    hub = pop.hub.Hub()
    hub.pop.sub.add("tests.mods")
    funcs = []
    for _ in hub.pop.sub:
        for var in hub.pop.sub:
            funcs.append(var.name)
        break
    assert funcs == sorted(hub.pop.sub._funcs.keys())


def test_nest():
    """
    Test the ability to nest the subs in a deeper namespace
    """
    hub = pop.hub.Hub()
    hub.pop.sub.add("tests.mods")
    hub.pop.sub.add("tests.mods.nest", sub=hub.mods)
    assert hub.mods.nest.basic.ret_true()


def test_this():
    hub = pop.hub.Hub()
    hub.pop.sub.add("tests.mods")
    hub.mods.test.ping()
    assert hub.mods.test.this() == {}


def test_func_attrs():
    hub = pop.hub.Hub()
    hub.pop.sub.add("tests.mods")
    assert "bar" in hub.mods.test.attr.__dict__
    assert hub.mods.test.attr.func.bar is True
    assert hub.mods.test.attr.func.func is not hub.mods.test.attr.func


def test_ref_sys():
    hub = pop.hub.Hub()
    hub.pop.sub.add("tests.mods")
    hub.mods.test.ping()
    assert hub.pop.ref.last("mods.test.ping")() == {}
    path = hub.pop.ref.path("mods.test.ping")
    assert len(path) == 4
    assert hasattr(path[0], "mods")
    assert hasattr(path[1], "test")
    assert hasattr(path[2], "ping")
    rname = "Made It!"
    hub.pop.ref.create("mods.test.Foo", rname)
    assert hub.mods.test.Foo == rname


def test_module_level_direct_call():
    hub = pop.hub.Hub()
    hub.pop.sub.add("tests.mods")
    with pytest.raises(Exception):
        hub.mods.test.module_level_non_aliased_ping_call()
    assert hub.mods.test.module_level_non_aliased_ping_call_fw_hub() == {}


def test_contract():
    hub = pop.hub.Hub()
    hub.pop.sub.add("tests.mods", contracts_pypath="tests.contracts")
    with pytest.raises(Exception) as context:
        hub.mods.test.ping(4)


def test_inline_contract():
    hub = pop.hub.Hub()
    hub.pop.sub.add("tests.cmods")
    assert hub.cmods.ctest.cping()
    assert hub.CPING


def test_no_contract():
    hub = pop.hub.Hub()
    hub.pop.sub.add("tests.mods")
    with pytest.raises(TypeError) as context:
        hub.mods.test.ping(4)


def test_contract_manipulate():
    hub = pop.hub.Hub()
    hub.pop.sub.add("tests.mods", contracts_pypath="tests.contracts")
    assert "override" in hub.mods.all.list()
    assert "post called" in hub.mods.all.list()
    assert "post" in hub.mods.all.dict()


def test_contract_sigs():
    hub = pop.hub.Hub()
    # TODO: This test needs to cover more cases
    with pytest.raises(pop.exc.ContractSigException) as exc:
        hub.pop.sub.add("tests.csigs")
        hub.csigs.sigs.first(4, 6, 8)
    exstr = str(exc.value)
    assert "Kwargs are not permitted as a parameter" in exstr
    assert 'Parameter "z" does not have the correct name: b' in exstr
    assert 'Parameter "a" is past available positional params' in exstr
    assert 'Parameter "args" is not in the correct position for *args' in exstr
    assert (
        'Parameter, "a" is type "<class \'inspect._empty\'>" not "<class \'str\'>"'
        in exstr
    )
    assert 'Parameter, "c" is type "<class \'str\'>" not "typing.List"' in exstr
    assert 'Parameter "bar" is past available positional params' in exstr
    assert "missing" in exstr


def test_private_function_cross_access():
    hub = pop.hub.Hub()
    hub.opts = "OPTS!"
    hub.pop.sub.add("tests.mods")
    # Let's make sure that the private function is not accessible through
    # the packed module
    with pytest.raises(AttributeError) as exc:
        hub.mods.priv._private() == "OPTS!"

    # Let's confirm that the private function has access to the cross
    # objects
    assert hub.mods.priv.public() == "OPTS!"


def test_private_function_cross_access_with_contracts():
    hub = pop.hub.Hub()
    hub.opts = "OPTS!"
    hub.pop.sub.add("tests.mods", contracts_pypath="tests.contracts")
    # Let's make sure that the private function is not accessible through
    # the packed module
    with pytest.raises(AttributeError) as exc:
        hub.mods.priv._private() == "OPTS!"

    # Let's confirm that the private function has access to the cross
    # objects
    assert hub.mods.priv.public() == "OPTS!"


def test_cross_in_virtual():
    hub = pop.hub.Hub()
    hub.opts = "OPTS!"
    hub.pop.sub.add("tests.mods", contracts_pypath="tests.contracts")
    assert hub.mods.virt.present() is True


def test_virtual_ret_true():
    hub = pop.hub.Hub()
    hub.opts = "OPTS!"
    hub.pop.sub.add("tests.mods", contracts_pypath="tests.contracts")
    assert hub.mods.truev.present() is True


def test_mod_init():
    hub = pop.hub.Hub()
    hub.context = {}
    hub.pop.sub.add(
        pypath="tests.mods.packinit", subname="mods", contracts_pypath="tests.contracts"
    )
    assert "LOADED" in hub.context
    assert hub.mods.packinit.loaded() is True

    # Now without force loading, at least a function needs to be called
    hub = pop.hub.Hub()
    hub.context = {}
    hub.pop.sub.add(
        pypath="tests.mods.packinit",
        subname="mods",
        contracts_pypath="tests.contracts",
        load_all=False,
    )
    assert hub.context == {"NEW": True}
    assert "LOADED" not in hub.context
    assert hub.mods.packinit.loaded() is True
    # And now __mod_init__ has been executed
    assert "LOADED" in hub.context

    # don't run init
    hub = pop.hub.Hub()
    hub.context = {}
    hub.pop.sub.add(
        pypath="tests.mods.packinit",
        subname="mods",
        contracts_pypath="tests.contracts",
        init=False,
        load_all=False,
    )
    assert hub.context == {}


def test_pack_init():
    hub = pop.hub.Hub()
    hub.context = {}
    hub.pop.sub.add(
        pypath="tests.mods.packinit", subname="mods", contracts_pypath="tests.contracts"
    )
    assert hub.mods.init.check() is True


def test_non_module_functions_are_not_packed():
    hub = pop.hub.Hub()
    hub.pop.sub.add("tests.mods")
    hub.mods._load_all()
    assert "scan" not in dir(hub.mods.test)
    try:
        hub.mods.test.call_scan() is True
    except TypeError:
        pytest.fail(
            "The imported 'scan' function in 'tests.mods.test' was wrongly packed"
        )


def test_double_underscore():
    hub = pop.hub.Hub()
    hub.pop.sub.add("tests.mods")
    hub.mods.test.double_underscore()


def test_unique_name():
    """
    Verify that the assigned module name inside of the python sys.modules
    is unique
    """
    hub = pop.hub.Hub()
    hub.pop.sub.add(dyne_name="dyne1")
    mname = hub.dyne3.init.mod_name()
    assert not mname.startswith(".")


def test_dyne():
    hub = pop.hub.Hub()
    hub.pop.sub.add(dyne_name="dyne1")
    assert hub.dyne1.INIT
    assert hub.dyne2.INIT
    assert hub.dyne3.INIT
    assert hub.dyne1.test.dyne_ping()
    assert hub.dyne1.nest.nest_dyne_ping()
    assert hub.dyne2.test.dyne_ping()
    assert hub.dyne2.nest.nest_dyne_ping()
    assert hub.dyne3.test.dyne_ping()
    assert hub.dyne3.nest.nest_dyne_ping()


def test_dyne_nest():
    hub = pop.hub.Hub()
    hub.pop.sub.add(dyne_name="dn1")
    hub.pop.sub.load_subdirs(hub.dn1, recurse=True)
    assert hub.dn1.nest.dn1.ping()
    assert hub.dn1.nest.dn2.ping()
    assert hub.dn1.nest.dn3.ping()
    assert hub.dn1.nest.next.test.ping()
    assert hub.dn1.nest.next.last.test.ping()


def test_dyne_extend():
    hub = pop.hub.Hub()
    hub.pop.sub.add(dyne_name="dn1")
    hub.pop.sub.load_subdirs(hub.dn1, recurse=True)
    assert hub.dn1.nest.over.in_dn1()
    assert hub.dn1.nest.over.in_dn2()
    assert hub.dn1.nest.over.in_dn3()


def test_dyne_overwrite():
    hub = pop.hub.Hub()
    hub.pop.sub.add(dyne_name="dn1")
    hub.pop.sub.load_subdirs(hub.dn1, recurse=True)
    # Assure that the first instance of a function gets overwritten
    assert hub.dn1.nest.over.source() == "dn2"
