.. _conf_integrate_overview:

====================
The Integrate System
====================

Now that you have a clear view of the available constructs in configuration dicts used by
the `conf` system we can talk about the `conf.integrate` module. By itself `conf` is a great
tool to load configs, but `pop` is all about dynamically merging multiple plugin subsystems.
Dynamically merging applications presents a significant issue when it comes to configuration,
`conf` and the `conf.integrate` systems are designed to work together to solve this issue.

Using `conf.integrate` is made to be as easy as possible, but it also means that the
configuration system follows a clear model.

When making a `pop` project, everything is a plugin, but you may have noticed that the
`pop_seed` script makes two python files outside of the plugin system. These files are
`version.py` and `conf.py`. The `version.py` file is hopefully self explanatory. But
the `conf.py` file needs a little explanation.

The Config Dicts
================

The integrate system uses this *conf.py* file to simply define CLI options, local config
options, and options that we assume other systems would share. These types of
configuration data are defined in configuration dicts in *conf.py*.

Simply populate these dicts with configuration data and it can be easily
and dynamically loaded by other `pop` projects.

CONFIG
------

The `CONFIG` dict is where the configuration options used specifically by the subsystems
defined in this project.

CLI_CONFIG
----------

The `CLI_CONFIG` dict is used for configuration data data specific to the command line.
It is only used to set positional arguments, things that define the structure of how
the CLI should be processed.

When using `CLI_CONFIG` the options should still be defined in the `CONFIG` section. The
top level key in the `CLI_CONFIG` will override the `CONFIG` values but having them set
in the `CONFIG` section will allow for the values to be absorbed by plugin systems
that are using your application.

SUBS
----

The `SUBS` dict compliments the `CLI_CONFIG` dict in specifying what subparsers should be
added to the cli when importing this config as the primary cli interface.

Usage
=====

Now, with the conf.py file in place loading the configuration data up is easier then ever!
Just add this one line to your project:

.. code-block:: python

    hub.pop.conf.integrate(<project_name>)

The conf system will get loaded for you and hub.OPT will be populated with namespaced configuration
data as defined in the configuration dicts.

Multiple Projects
-----------------

If multiple projects are used the first argument is a list of projects. The `CLI_CONFIG`
will only be taken from one project. So when using multiple projects the `cli` option can be
passed to specify which project to pull the CLI_CONFIG from:

.. code-block:: python

    hub.pop.conf.integrate(['act', 'grains', 'rem'], cli='rem')

Override Usage
==============

Sometimes configuration options collide. Since the integrate system is used to dynamically merge
multiple projects' configuration options we need to be able to handle these collisions. This
is where the `override` setting comes into play.

If there is a conflict in the configs, then the `conf` system will throw an exception listing
the colliding options. These options will be shown as the package name followed by the config key.
So if the project name passed into integrate is `poppy` and the configuration key is test, then
the collision will be on key `poppy.test`. To overcome the collision we need to create a new
key and potentially new options for the command.

To use the override just define the override dict and pass it into `pop.conf.integrate`:

.. code-block:: python

    override = {'poppy.test': {'key': 'test2', 'options': ['--test2', '-T']}}
    hub.pop.conf.integrate('poppy', override)

Now the collisions are explicitly re-routed and fixed!

Using The Roots System
======================

In many applications directories need to be created and verified. Often the directories also
need to be set up for a specific user if not run with admin privileges. This is where the
`roots` system comes into place.

If you have set up any option(s) that ends in `_dir`, then you can have `conf.integrate` do
some work for you! By setting the `roots` option `conf` will create the directory if it does
not already exist and it will change the paths to those directories to be in a hidden directory
in the user's home directory if not running as the root user.
