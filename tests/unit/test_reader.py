# -*- coding: utf-8 -*-
"""
Test the reader interface for pkinit
"""
# Import python libs
import sys
import json
import copy
import os
from collections import OrderedDict

# import pytest
import py
import pytest

# import pop libs
import pop.hub

C1 = {
    "foo": {"default": "bar", "help": "Some text.", "group": "spam", "os": True,},
    "osvar": {"default": "bad", "help": "Override with os var", "os": "poptestosvar",},
    "false": {
        "default": True,
        "help": "Set it to False",
        "options": ["-f"],
        "action": "store_false",
        "group": "spam",
    },
    "nargs": {"default": ["foo", "bar", "baz"], "nargs": 3, "help": "make nargs",},
    "gr1": {"ex_group": "EX", "help": "cheese",},
    "gr2": {"ex_group": "EX", "help": "conflicting cheese",},
    "config": {
        "default": "/dosent_exist_I_hopeasdkjfgkjsahdgakjsdhgkjsdh",
        "options": ["-C"],
        "help": "Location of the config file",
        "group": "orange",
    },
}

F1 = {
    "foo": "quo",
    "new": "not in def",
}

C2 = {
    "foo": {"default": "bar", "help": "Some text.", "group": "spam",},
    "false": {
        "default": True,
        "help": "Set it to False",
        "options": ["-f"],
        "action": "store_false",
        "group": "spam",
    },
    "nargs": {"default": ["foo", "bar", "baz"], "nargs": 3, "help": "make nargs",},
    "gr1": {"ex_group": "EX", "help": "cheese",},
    "gr2": {"ex_group": "EX", "help": "conflicting cheese",},
    "config_dir": {
        "default": "/dosent_exist_I_hopeasdkjfgkjsahdgakjsdhgkjsdh",
        "options": ["-C"],
        "help": "Location of the config directory",
        "group": "orange",
    },
    "config_recurse": {"default": True, "help": "Recurse into directories",},
}

F2 = {
    "foo": "status",
    "new": "in def",
}

C3 = {
    "foo": {"default": "bar", "help": "Some text.", "group": "spam",},
    "config_dir": {
        "default": "/dosent_exist_I_hopeasdkjfgkjsahdgakjsdhgkjsdh",
        "options": ["-C"],
        "help": "Location of the config directory",
        "group": "orange",
        "pattern": "*.conf",
    },
}

F3 = {
    "foo": "status",
    "new": "in def",
}

SUB = {
    "sub": {"desc": "a subparser!", "help": "Some subparsing",},
}

C4 = {
    "foo": {"sub": "sub", "help": "Set some foo!",},
}

C5 = {
    "config_dir": {
        "default": ["/dosent_exist_I_hopeasdkjfgkjsahdgakjsdhgkjsdh"],
        "options": ["-C"],
        "help": "Location of the config directory",
        "group": "orange",
        "nargs": "*",
    },
}

C6 = {
    "config_dir": {
        "default": ["/dosent_exist_I_hopeasdkjfgkjsahdgakjsdhgkjsdh"],
        "options": ["-C"],
        "help": "Location of the config directory",
        "group": "orange",
        "nargs": "*",
        "action": "append",
    },
}

C7 = {
    "config_dir": {
        "default": ["/dosent_exist_I_hopeasdkjfgkjsahdgakjsdhgkjsdh"],
        "options": ["-C"],
        "help": "Location of the config directory",
    },
    "foo": {"help": "Some text.", "positional": True},
}

C8 = {
    "config_dir": {
        "default": ["/dosent_exist_I_hopeasdkjfgkjsahdgakjsdhgkjsdh"],
        "options": ["-C"],
        "help": "Location of the config directory",
    },
    "foo": {"help": "Some text.",},
    "foo_positional_1": {"sub": "sub", "help": "Set some bar!", "positional": True},
    "foo_positional_2": {
        "sub": "sub",
        "help": "Set some bar!",
        "positional": True,
        "display_priority": 1,
    },
}

C9 = {
    "config_dir": {
        "default": ["/dosent_exist_I_hopeasdkjfgkjsahdgakjsdhgkjsdh"],
        "options": ["-C"],
        "help": "Location of the config directory",
    },
    "foo": {"help": "Some text.", "positional": True, "default": "bar", "nargs": "?"},
}

C10 = {
    "foo": {"default": {"bar": "baz"}, "render": "json",},
}


C11 = {
    "foo": {"sub": ["sub", "another"], "help": "Set some foo!",},
}

SUB2 = {
    "sub": {"desc": "a subparser!", "help": "Some subparsing",},
    "another": {"desc": "another subparser!", "help": "Some subparsing",},
}


@pytest.yield_fixture(autouse=True)
def _clean_argv():
    """
    clean out any arguments passed to the script
    """
    argv = sys.argv[:]
    sys.argv = ["blah"]
    yield
    sys.argv = argv


def test_default():
    hub = pop.hub.Hub()
    hub.pop.sub.add("pop.mods.conf")
    opts = hub.conf.reader.read(C1)
    assert opts["foo"] == "bar"
    assert "_subparser_" not in opts


def test_render():
    hub = pop.hub.Hub()
    hub.pop.sub.add("pop.mods.conf")
    sys.argv.append("--foo")
    sys.argv.append('{"bar": "baz"}')
    opts = hub.conf.reader.read(C10)
    assert opts["foo"] == {"bar": "baz"}
    assert "_subparser_" not in opts


def test_render_sans():
    hub = pop.hub.Hub()
    hub.pop.sub.add("pop.mods.conf")
    opts = hub.conf.reader.read(C10)
    assert opts["foo"] == {"bar": "baz"}
    assert "_subparser_" not in opts


def test_os():
    hub = pop.hub.Hub()
    hub.pop.sub.add("pop.mods.conf")
    os.environ["FOO"] = "osvar"
    os.environ["POPTESTOSVAR"] = "good"
    opts = hub.conf.reader.read(C1)
    assert opts["foo"] == "osvar"
    assert opts["osvar"] == "good"


def test_pass():
    hub = pop.hub.Hub()
    hub.pop.sub.add("pop.mods.conf")
    sys.argv.append("--foo")
    sys.argv.append("baz")
    opts = hub.conf.reader.read(C1)
    assert opts["foo"] == "baz"


def test_action():
    hub = pop.hub.Hub()
    hub.pop.sub.add("pop.mods.conf")
    opts = hub.conf.reader.read(C1, args=["-f"])
    assert opts["false"] is False


def test_file(tmpdir):
    hub = pop.hub.Hub()
    hub.pop.sub.add("pop.mods.conf")
    try:
        conf_file = tmpdir.join("config_file")
        conf_file.write(json.dumps(F1))
        sys.argv.append("--config")
        sys.argv.append(conf_file.realpath().strpath)
        opts = hub.conf.reader.read(C1)
        assert opts["new"] == "not in def"
    finally:
        try:
            tmpdir.remove(rec=True, ignore_errors=True)
        except py.error.ENOENT:  # pylint: disable=no-member
            pass


def test_config_dir(tmpdir):
    hub = pop.hub.Hub()
    hub.pop.sub.add("pop.mods.conf")
    try:
        conf_dir = tmpdir.mkdir("cfgdir")
        conf_file = conf_dir.join("config_file")
        conf_file.write(json.dumps(F2))
        sys.argv.append("--config-dir")
        sys.argv.append(conf_dir.realpath().strpath)
        opts = hub.conf.reader.read(C2)
        assert opts["new"] == "in def"
    finally:
        try:
            tmpdir.remove(rec=True, ignore_errors=True)
        except py.error.ENOENT:  # pylint: disable=no-member
            pass


def test_config_dir_multiple_files(tmpdir):
    hub = pop.hub.Hub()
    hub.pop.sub.add("pop.mods.conf")
    try:
        conf_dir = tmpdir.mkdir("cfgdir")
        conf_file = conf_dir.join("config_file-0")
        conf_file.write(json.dumps(F1))
        conf_file = conf_dir.join("config_file-1")
        conf_file.write(json.dumps(F2))
        sys.argv.append("--config-dir")
        sys.argv.append(conf_dir.realpath().strpath)
        opts = hub.conf.reader.read(C2)
        assert opts["new"] == "in def"
    finally:
        try:
            tmpdir.remove(rec=True, ignore_errors=True)
        except py.error.ENOENT:  # pylint: disable=no-member
            pass


def test_config_dir_with_nested_dirs(tmpdir):
    hub = pop.hub.Hub()
    hub.pop.sub.add("pop.mods.conf")
    try:
        conf_dir_1 = tmpdir.mkdir("cfgdir")
        conf_file_1 = conf_dir_1.join("config_file-0")
        conf_file_1.write(json.dumps(F1))
        conf_dir_2 = conf_dir_1.mkdir("cfgdir")
        conf_file_2 = conf_dir_2.join("config_file-1")
        conf_file_2.write(json.dumps(F2))
        sys.argv.append("--config-dir")
        sys.argv.append(conf_dir_1.realpath().strpath)
        opts = hub.conf.reader.read(C2)
        assert opts["new"] == "in def"
    finally:
        try:
            tmpdir.remove(rec=True, ignore_errors=True)
        except py.error.ENOENT:  # pylint: disable=no-member
            pass


def test_config_dir_nargs(tmpdir):
    try:
        hub = pop.hub.Hub()
        hub.pop.sub.add("pop.mods.conf")
        conf_dir_1 = tmpdir.mkdir("cfgdir-1")
        conf_file_1 = conf_dir_1.join("config_file-0")
        # new = 'not in def'
        conf_file_1.write(json.dumps(F1))
        conf_dir_2 = tmpdir.mkdir("cfgdir-2")
        conf_file_2 = conf_dir_2.join("config_file-1")
        # new = 'in def'
        conf_file_2.write(json.dumps(F2))
        opts = hub.conf.reader.read(
            C5,
            args=[
                "--config-dir",
                conf_dir_1.realpath().strpath,
                conf_dir_2.realpath().strpath,
            ],
        )
        assert opts["new"] == "in def"

        # Let's invert the order to confirm
        hub = pop.hub.Hub()
        hub.pop.sub.add("pop.mods.conf")
        conf_dir_3 = tmpdir.mkdir("cfgdir-3")
        conf_file_3 = conf_dir_3.join("config_file-0")
        # new = 'not in def'
        conf_file_3.write(json.dumps(F1))
        conf_dir_4 = tmpdir.mkdir("cfgdir-4")
        conf_file_4 = conf_dir_4.join("config_file-1")
        # new = 'in def'
        conf_file_2.write(json.dumps(F2))
        opts = hub.conf.reader.read(
            C5,
            args=[
                "--config-dir",
                conf_dir_4.realpath().strpath,
                conf_dir_3.realpath().strpath,
            ],
        )
        assert opts["new"] == "not in def"
    finally:
        try:
            tmpdir.remove(rec=True, ignore_errors=True)
        except py.error.ENOENT:  # pylint: disable=no-member
            pass


def test_config_dir_nargs_append(tmpdir):
    try:
        hub = pop.hub.Hub()
        hub.pop.sub.add("pop.mods.conf")
        conf_dir_1 = tmpdir.mkdir("cfgdir-1")
        conf_file_1 = conf_dir_1.join("config_file-0")
        # new = 'not in def'
        conf_file_1.write(json.dumps(F1))
        conf_dir_2 = tmpdir.mkdir("cfgdir-2")
        conf_file_2 = conf_dir_2.join("config_file-1")
        # new = 'in def'
        conf_file_2.write(json.dumps(F2))

        # new dir, inverted order
        conf_dir_3 = tmpdir.mkdir("cfgdir-3")
        conf_file_3 = conf_dir_3.join("config_file-0")
        # new = 'not in def'
        conf_file_3.write(json.dumps(F1))
        conf_dir_4 = tmpdir.mkdir("cfgdir-4")
        conf_file_4 = conf_dir_4.join("config_file-1")
        # new = 'in def'
        conf_file_4.write(json.dumps(F2))
        opts = hub.conf.reader.read(
            C6,
            args=[
                "-C",
                conf_dir_1.realpath().strpath,
                conf_dir_2.realpath().strpath,
                "-C",
                conf_dir_4.realpath().strpath,
                conf_dir_3.realpath().strpath,
            ],
        )
        assert opts["new"] == "not in def"
    finally:
        try:
            tmpdir.remove(rec=True, ignore_errors=True)
        except py.error.ENOENT:  # pylint: disable=no-member
            pass


def test_config_dir_pattern(tmpdir):
    hub = pop.hub.Hub()
    hub.pop.sub.add("pop.mods.conf")
    try:
        conf_dir = tmpdir.mkdir("cfgdir")
        conf_file = conf_dir.join("config_file-0.conf")
        conf_file.write(json.dumps(F1))
        conf_file = conf_dir.join("config_file-1.config")
        conf_file.write(json.dumps(F3))
        sys.argv.append("--config-dir")
        sys.argv.append(conf_dir.realpath().strpath)
        opts = hub.conf.reader.read(C3)
        assert opts["new"] == "not in def"
    finally:
        try:
            tmpdir.remove(rec=True, ignore_errors=True)
        except py.error.ENOENT:  # pylint: disable=no-member
            pass


def test_subs():
    hub = pop.hub.Hub()
    hub.pop.sub.add("pop.mods.conf")
    sys.argv.extend(["sub", "--foo", "bar"])
    opts = hub.conf.reader.read(C4, SUB)
    assert opts["foo"] == "bar"
    assert opts["_subparser_"] == next(iter(SUB.keys()))


def test_multi_subs_1():
    hub = pop.hub.Hub()
    hub.pop.sub.add("pop.mods.conf")
    sys.argv.extend(["sub", "--foo", "bar"])
    opts = hub.conf.reader.read(C11, SUB2)
    assert opts["foo"] == "bar"
    assert opts["_subparser_"] == "sub"


def test_multi_subs_2():
    hub = pop.hub.Hub()
    hub.pop.sub.add("pop.mods.conf")
    sys.argv.extend(["another", "--foo", "baz"])
    opts = hub.conf.reader.read(C11, SUB2)
    assert opts["foo"] == "baz"
    assert opts["_subparser_"] == "another"


def test_version(capsys):
    in_opts = {
        "version": {"action": "version", "version": "1.0.1", "help": "show version"}
    }
    hub = pop.hub.Hub()
    hub.pop.sub.add("pop.mods.conf")
    with pytest.raises(SystemExit):
        hub.conf.reader.read(in_opts, args=["--version"])
    out, _ = capsys.readouterr()
    assert out.strip() == in_opts["version"]["version"]


def test_priority_order(capsys):
    opts = {
        "false": {
            "default": True,
            "help": "Set it to False",
            "options": ["-f"],
            "action": "store_false",
        },
        "true": {
            "default": False,
            "help": "Set it to True",
            "options": ["-t"],
            "action": "store_true",
        },
        "version": {"action": "version", "version": "1.0.1", "help": "show version",},
    }

    # Alphabetical order, regular dict, no explicit order
    in_opts = copy.deepcopy(opts)
    hub = pop.hub.Hub()
    hub.pop.sub.add("pop.mods.conf")
    with pytest.raises(SystemExit):
        hub.conf.reader.read(in_opts, args=["-h"])
    out, _ = capsys.readouterr()
    lines = [
        line.strip()
        for line in out.split("\n")
        if line and "-" in line and "usage" not in line
    ]
    assert lines[0].startswith("-h")
    assert lines[1].startswith("-f, --false")
    assert lines[2].startswith("-t, --true")
    assert lines[3].startswith("--version")

    # Explicit order, regular dict
    in_opts = copy.deepcopy(opts)
    in_opts["version"]["display_priority"] = 1
    in_opts["true"]["display_priority"] = 2

    hub = pop.hub.Hub()
    hub.pop.sub.add("pop.mods.conf")
    with pytest.raises(SystemExit):
        hub.conf.reader.read(in_opts, args=["-h"])
    out, _ = capsys.readouterr()
    lines = [
        line.strip()
        for line in out.split("\n")
        if line and "-" in line and "usage" not in line
    ]
    assert lines[0].startswith("-h")
    assert lines[1].startswith("--version")
    assert lines[2].startswith("-t, --true")
    assert lines[3].startswith("-f, --false")

    # OrderedDict order
    od_in_opts = OrderedDict()
    od_in_opts["false"] = copy.deepcopy(opts["false"])
    od_in_opts["true"] = copy.deepcopy(opts["true"])
    od_in_opts["version"] = copy.deepcopy(opts["version"])

    hub = pop.hub.Hub()
    hub.pop.sub.add("pop.mods.conf")
    with pytest.raises(SystemExit):
        hub.conf.reader.read(od_in_opts, args=["-h"])
    out, _ = capsys.readouterr()
    lines = [
        line.strip()
        for line in out.split("\n")
        if line and "-" in line and "usage" not in line
    ]
    assert lines[0].startswith("-h")
    assert lines[1].startswith("-f, --false")
    assert lines[2].startswith("-t, --true")
    assert lines[3].startswith("--version")

    # OrderedDict explicit order
    ode_in_opts = copy.deepcopy(od_in_opts)
    ode_in_opts["version"]["display_priority"] = 1
    ode_in_opts["true"]["display_priority"] = 2

    hub = pop.hub.Hub()
    hub.pop.sub.add("pop.mods.conf")
    with pytest.raises(SystemExit):
        hub.conf.reader.read(ode_in_opts, args=["-h"])
    out, _ = capsys.readouterr()
    lines = [
        line.strip()
        for line in out.split("\n")
        if line and "-" in line and "usage" not in line
    ]
    assert lines[0].startswith("-h")
    assert lines[1].startswith("--version")
    assert lines[2].startswith("-t, --true")
    assert lines[3].startswith("-f, --false")


def test_ex_group(capsys):
    hub = pop.hub.Hub()
    hub.pop.sub.add("pop.mods.conf")
    sys.argv.extend(["--gr1", "bar", "--gr2", "baz"])
    with pytest.raises(SystemExit):
        opts = hub.conf.reader.read(C1)


def test_argparser_config(capsys):
    opts = {
        "_argparser_": {"description": "My Cool Pack Parsers", "prog": "PaCk-PaRsEr"},
        "false": {
            "default": True,
            "help": "Set it to False",
            "options": ["-f"],
            "action": "store_false",
        },
    }
    hub = pop.hub.Hub()
    hub.pop.sub.add("pop.mods.conf")
    with pytest.raises(SystemExit):
        hub.conf.reader.read(opts, args=["-h"])
    out, _ = capsys.readouterr()
    assert opts["_argparser_"]["description"] in out
    assert "usage: {} [-h] [-f]".format(opts["_argparser_"]["prog"]) in out


def test_positional():
    hub = pop.hub.Hub()
    hub.pop.sub.add("pop.mods.conf")
    sys.argv.extend(["bar", "-C", "/tmp/bin"])
    opts = hub.conf.reader.read(C7)
    assert opts["foo"] == "bar"
    assert opts["config_dir"] == "/tmp/bin"


def test_positional_default():
    hub = pop.hub.Hub()
    hub.pop.sub.add("pop.mods.conf")
    sys.argv.extend(["-C", "/tmp/bin"])
    opts = hub.conf.reader.read(copy.deepcopy(C9))
    assert opts["foo"] == "bar"
    assert opts["config_dir"] == "/tmp/bin"

    hub = pop.hub.Hub()
    hub.pop.sub.add("pop.mods.conf")
    sys.argv.extend(["bin", "-C", "/tmp/bin"])
    opts = hub.conf.reader.read(copy.deepcopy(C9))
    assert opts["foo"] == "bin"
    assert opts["config_dir"] == "/tmp/bin"


def test_subs_positional():
    hub = pop.hub.Hub()
    hub.pop.sub.add("pop.mods.conf")
    sys.argv.extend(["--foo", "bar", "sub", "positional-baz", "positional-bar"])
    opts = hub.conf.reader.read(copy.deepcopy(C8), SUB)
    assert opts["foo"] == "bar"
    assert opts["_subparser_"] == next(iter(SUB.keys()))
    assert opts["foo_positional_2"] == "positional-baz"
    assert opts["foo_positional_1"] == "positional-bar"


def test_subs_positional_missing(capsys):
    # And if we're missing positional arguments
    hub = pop.hub.Hub()
    hub.pop.sub.add("pop.mods.conf")
    sys.argv.extend(["--foo", "bar", "sub", "positional-baz"])
    with pytest.raises(SystemExit):
        hub.conf.reader.read(copy.deepcopy(C8), SUB)
    _, err = capsys.readouterr()
    assert "error: the following arguments are required: foo_positional_1" in err


def test_integrate_simple():
    hub = pop.hub.Hub()
    hub.pop.sub.add("pop.mods.conf")
    hub.conf.integrate.load("tests.conf1")
    assert hub.OPT == {
        "tests.conf1": {
            "log_datefmt": "%H:%M:%S",
            "log_file": "tests.conf1.log",
            "log_fmt_console": "[%(levelname)-8s] %(message)s",
            "log_fmt_logfile": "%(asctime)s,%(msecs)03d [%(name)-17s][%(levelname)-8s] %(message)s",
            "log_level": "info",
            "log_plugin": "basic",
            "someone": "Not just anybody!",
            "stuff_dir": "/tmp/tests.conf1/stuff",
            "test": False,
            "version": False,
        },
    }


def test_integrate_merge():
    hub = pop.hub.Hub()
    hub.pop.sub.add("pop.mods.conf")
    hub.conf.integrate.load(
        ["tests.conf1", "tests.conf2"], cli="tests.conf1", logs=False, version=False
    )
    assert hub.OPT == {
        "tests.conf2": {"monty": False},
        "tests.conf1": {
            "test": False,
            "stuff_dir": "/tmp/tests.conf1/stuff",
            "someone": "Not just anybody!",
        },
    }


def test_integrate_collide():
    hub = pop.hub.Hub()
    hub.pop.sub.add("pop.mods.conf")
    with pytest.raises(KeyError):
        hub.conf.integrate.load(["tests.conf1", "tests.conf2", "tests.conf3"])


def test_integrate_override():
    hub = pop.hub.Hub()
    hub.pop.sub.add("pop.mods.conf")
    over = {"tests.conf1.test": {"key": "test2", "options": ["--test2"]}}
    hub.conf.integrate.load(
        ["tests.conf1", "tests.conf2", "tests.conf3"], over, logs=False, version=False
    )
    assert hub.OPT == {
        "tests.conf2": {"monty": False},
        "tests.conf1": {"stuff_dir": "/tmp/tests.conf1/stuff", "test2": False},
        "tests.conf3": {"test": False},
    }


def test_integrate_dirs():
    hub = pop.hub.Hub()
    hub.pop.sub.add("pop.mods.conf")
    hub.conf.integrate.load("tests.conf1", roots=True)
    assert os.path.isdir(hub.OPT["tests.conf1"]["stuff_dir"])
    assert hub.OPT["tests.conf1"]["stuff_dir"].endswith(".tests.conf1/stuff")


def test_integrate_log():
    hub = pop.hub.Hub()
    hub.pop.sub.add("pop.mods.conf")
    hub.conf.integrate.load("tests.conf1")
    import logging

    log = logging.getLogger(__name__)
    assert bool(log.root.handlers)
    assert not bool(log.handlers)
