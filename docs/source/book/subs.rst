========================
Plugin Subsystems - Subs
========================

Plugin Subsystems - or *Subs* - are the basic containers for code in Plugin
Oriented Programming. *Subs* contain both plugins and data, these *Subs* are
available to the application via the `hub`.

The concept of the *Sub* is roughly as central and critical to Plugin Oriented
Programming as the concept of a class is to Object Oriented Programming.
This is therefore the central focus of how to create a plugin oriented
application.

Subs Contain Plugins
====================

On the surface, *Subs* appear to simply contain plugins, but this is similar
to classes on the surface, as they appear to just contain data and functions.
Like classes, *Subs* are a canvas for the developer, allowing for the
complexity of the software to be simplified into reusable, flexible, compartments.
While the *Sub* is comparable to the criticality of classes in OOP, it should not be
confused with classes! Plugin Oriented Programming does not have a concept
inheritance for instance.

When a *Sub* is created it gets placed on the hierarchical namespace - the `hub` -
so that any application can call into functions and data exposed by the *Sub*.

The *Sub*'s primary purpose is the present plugins. The plugins are individual
files containing tight code compartments that express an interface.

Adding Subs to a hub
====================

Once a `hub` is available then it is easy to add a *Sub* to the `hub`. Keep in
mind that there are many ways to construct a *Sub*. In the end a *Sub*
only needs to be a directory with *.py* files in it, nothing more. With that
said, there are many ways to identify how to find the directory, or
directories!

But do not despair. `pop` presents many flexible options, but retains a strong
opinion about how to do things right.

Using Dynamic Names
-------------------

The best way to add a Sub to your `hub` is to use *Dynamic Names*. Using
*Dynamic Names* is easy. It requires you to register your *Sub* with the `pop`
configuration system.

Assuming you started with a `pop-seed` project called "poppy", open up the
project's `conf.py` file and add a *Sub* called `rpc`. The `conf.py` file can be
found at `poppy/conf.py` AKA `<Project name>/conf.py`:

.. code-block:: python

    DYNE = {
        "rpc": ["rpc"],
    }

The `conf.py` will already exist, `pop-seed` creates it. When you add a **DYNE**
entry to the `conf.py`, it registers that under this project's plugins for the *Sub*
- in this case named `rpc` - where it can be found.

This means that multiple codebases can contribute plugins to the *Sub*!
Very easily, third party developers can extend your *Sub* without modifying
your code to do it! This is one of the most powerful aspects of Plugin Oriented
Programming called *Vertical App Merging*.

Now that your *Sub* is registered, it can be added to a `hub` by calling
`hub.pop.sub.add` and passing in the `dyne_name` argument:

.. code-block:: python

    hub.pop.sub.add(dyne_name="rpc")

Since the `hub` is available anywhere in your application, it can be called from
anywhere. A plugin can add a new *Sub*, this is a core design consideration of
Plugin Oriented Programming. A plugin cannot be a dead end, it needs to be able
to always add globally available *Subs* onto the `hub`.

Using PyPath
------------

Using the `pypath` system in `pop` is the simplest way to add a *Sub* to your `hub`,
but it does not activate *Vertical App Merging*.

Using `pypath` is simple, just call `hub.pop.sub.add` and pass in the python import
path that, when impoerted, will lead the way to the directory with plugins.

.. code-block:: python

    hub.pop.sub.add('poppy.poppy')

That's it! Now you have a new *Sub* on your `hub` called `poppy` that will find
your plugins by importing `poppy.poppy`, looking at the imported module's `path`
variable and translating that into a directory which is then scanned for plugins.

Recursive Sub Loading
=====================

When a *Sub* gets added to the `hub` it can be desirable to find any directories
under the found director(ies) and add them to the *Sub* as nested *Subs*. This can
be an excellent way to organize code, allowing for *Subs* to exist nested within
each other on the `hub`.

To recursively scan for nested *Subs* just call
`hub.pop.sub.load_subdirs(hub.subname, recurse=True)`. This will look in all of the
directories defined in the loaded Sub and scan for any subdirectories. If those
subdirectories exist they will be found and loaded onto the `hub` as nested *Subs*.

Plugin Loading
==============

By default, plugins in `pop` are lazy loaded. They only get imported when they are
first accessed. This greatly speeds up the creation of a *Sub*. If a *Sub*
contained hundreds of Plugins then it would take some time to load all of the plugins,
typically a few seconds, lazy loading allows this time consumption to be bypassed.

Sometimes it may be desirable to pre-load all of your plugins, to do this just call
`hub.pop.sub.load_all(hub.subname)`.

Some events will trigger loading all plugins. In particular if you decide to iterate
over a *Sub* then the `load_all` call will be executed on the *Sub* if it has not been
called already, therefore ensuring that all plugins are loaded and can be cleanly iterated
over.

The init System
===============

Now that your *Sub* is on your hub, let's take a look at the *Init* system used
by `pop`. This system allows you to initialize your new *Sub*. In a nutshell
you can place an optional plugin in your *Sub* named `init.py` and this plugin
will be automatically loaded when your *Sub* gets created. Think of the `init.py`
as the plugin that defines how your *Sub* will function. Typically the *Sub's*
pattern is defined in the `init.py`, but we will cover patterns in more depth in
the chapter on patterns!

The __init__ Function
=====================

Just like Classes in Python, plugins in `pop` can be initialized. Just create an
**optional** function called `__init__`. This function will be called when the plugin
gets loaded.

Also, as in Python classes, the `__init__` function should not be used to call
code that runs or starts the pattern expressed in the *Sub*. If we were to do this
then it would violate App Merging! The control of a *Sub* should always be separated
from the initialization. This makes the `__init__` function perfect for setting up
data structures on the `hub` that will be needed by the plugins of the *Sub*.

Subs Express Patterns
=====================

When creating a *Sub* it should always express a pattern. Patterns in Plugin Oriented
Programming are used as a consistent, predictable way to make your *Subs* pluggable.

Read on to the next chapter to learn more about patterns and why they are so central
to Plugin Oriented Programming.
