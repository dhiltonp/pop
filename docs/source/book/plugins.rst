=======
Plugins
=======

Plugins comprise the medium for software development within Plugin Oriented
Programming. When people start with Plugin Oriented Programming they often
struggle letting go of Object Oriented Programming and rethinking an
application as a collection of plugins.

This section will outline not only how to code in plugins, but also how to
think about many of the core concepts of programming through the lens of
plugins that exist on a `hub`. This transition is critical to understanding
Plugin Oriented programming, as well as how plugins should be built so retain
pluggability.

Functions and the hub
=====================

The primary building block to use is functions. Classes are available, but
the excessive use of classes is discouraged. Functions exist relative to data,
as it is stored on the `hub`, and instances should never be thought of as
*Subs* or *Plugins*, or even locations on the `hub`. An instance is a named
reference which points to a collection of data on the `hub`.

All functions on the `hub` receive, as their first argument, the `hub`. This
can be thought of in a similar way to how `self` is passed as the first argument
to a method in a class. The `hub` that is sent as the first argument is THE `hub`,
the shared hierarchical namespace used by the entire application.

With a reference to the `hub` available to all functions, it becomes easy to
call separate applications and invoke patterns on separate *Subs*.

For this example, let us suppose that we are in a *Sub* called `poppy`, in the
`init.py` file:

.. code-block:: python

    def get_data(hub, a, b):
        data = {a: b}

    def run(hub):
        data = hub.poppy.init.get_data(7, 8)

In this example, we call the `get_data` function on the `hub`. When this happens
the `hub` itself is transparently passed to the called function. This is similar
in behavior to how the `self` variable is passed inside of classes.

Private Functions
=================

In Plugin Oriented Programming, it is wise to expose more functions, allowing more
calls to be available. This practice pushes developers to maintain clean interfaces
to functions and maintain overall portability of code. But private functions are still
available.

Making a function private is simple, just precede the name of the function with an
underscore (`_`).

Here is a simple example:

.. code-block:: python

    # A public function exposed on the hub
    def foo(hub):
        return True

    # A private function, only available locally
    def _bar():
        return True

Since private functions are not exposed on the hub, they cannot be called via the hub
and do not receive the hub as the first argument.

There is nothing wrong with manually passing a reference to the `hub` to a private
function and is a common practice.

Virtual Names
=============

Virtual names allow for plugins to get renamed dynamically. This can be very useful
when creating dynamically assigned plugins. A good example here is normalizing
multiple operating systems or apis into a single exposed interface.

We can take network management for example. Lets say that you wanted to make a system
that allowed you to ask any operating system to give you network information
and every operating system recived the same input and gave the same output. Even though
the code dynamically determined which plugin to run for you?

Lets assume that we are in a *Sub* called `net` and in a plugin called `windows_query.py`
and `linux_query.py`. We then want the plugins to be exposed on the `hub` as `query`, but
only loaded if running the rspective platform:

The `windows_query.py` file:

.. code-block:: python

    import sys

    __virtualname__ = 'query'

    def __vitual__(hub):
        """
        Only load on Windows
        """
        if sys.platform.lower().startswith("win"):
            return True
        return False


    def interfaces(hub):
        # get windows network data

The `linux_query.py` file:

.. code-block:: python

    import sys

    __virtualname__ = 'query'

    def __vitual__(hub):
        """
        Only load on Linux
        """
        if sys.platform.lower().startswith("linux"):
            return True
        return False


    def interfaces(hub):
        # get Linux network data


This example is a little contrived to illustrate a point. Since the `__virtualname__` variable
is set then the plugin will show up as `query` on the hub for both files. The trick is making
sure that they only show up on the correct platforms. This is what the `__virtual__` function is
for, it is called when the plugin is loaded and if ti returns `False`, then the plugin is
discarded and not loaded up onto the `hub`.

This makes it very easy to make dynamic decisions based on variables like platform and configuration
to dynamically decide which plugins to load under what circumstances.


Func Alias
==========

Sometimes it is desirable to to load up a function name onto the `hub` that is not
the same as the function name in the file. This can be very useful because Python
uses a number of common names as built in variables and functions that you don't
want to override.

When making function names on the `hub` it is important to remember that you are creating
an API interface that may be exposed, not only internally to your application, but also
over the network. This means that having clean, self describing, terse, names can be
very helpful.

Instead of making long names it is good to utilize the information that is exposed in
the path on the `hub` to your function. This allows for variable names to be short
while still  communicating the nature of the function.

A simple example can be writing a system to expose an API. Lets suppose that we are
making plugins to communicate with a cloud API. It is simple to make a function
called `list` in a plugin called `network` in a *Sub* called `azure`. This way
the function ref on the hub is self explanatory; `hub.azure.network.list`.

This presents the follow on problem that the func alias system is built for. The
`list` function is a built in function for Python that should not be overwritten!
Oh what to do?

Simple! If you add a dict to your plugin called `__func_alias__` then you can
cleanly map one function name to another, allowing you to expose the API
interface that you feel is clean without violating any Python rules:

.. code-block:: python

    __func_alias__ = {'list_': 'list'}

    def list_(hub):
        # Code

Now this function will be exposed on the hub as `list` even though it is, to all
Python loading rules called `list_`.

The Initializer Function
========================

Every module can have an initializer function. This is a function that gets called
when the plugin gets loaded. These functions ca be very effective as setting up
data structures on the `hub` or loading a local cache needed by the plugin.

Remember, that the initializer is called dynamically and should execute very
quickly, it is unwise to add code to an initializer that takes a long time to run!

Adding as initializer is very easy, just add a function called `__init__` to the
plugin. This is designed to be intuitive for Python developers, as the `__init__`
function is used in Python classes as well.

.. code-block:: python

    def __init__(hub):
        hub.poppy.plugin.DATA = {}

This example is very simple, but it is a very common pattern to use. Just
adding a new variable to the plugin's namespace in the `__init__` function
makes the variable available to all of the function in the plugin.

Data on the hub
===============

Placing data on the `hub` is a powerful way to manage the data used in plugins and
*Subs*. Any new dataset can be cleanly added to to the `hub`. Here is a simple example:

.. code-block:: python

    def __init__(hub):
        hub.poppy.plugin.DATA = {}
        hub.poppy.POPPY_THINGS = {}
        # While you are not restricted from adding data directly to the hub, it is strongly discouraged
        hub.GLOBAL_THINGS = {}

    def foo(hub):
        hub.poppy.plugin.DATA['something useful'] = 37

Now these data structures are available to all applications on the `hub`. This allows
for data to be globally available but namespaced so other parts of the application don't
manipulate the data.
