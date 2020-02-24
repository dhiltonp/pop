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
multiple operating systems. We can take network management for example.


Func Alias
==========

Function Alias

Instance Management
===================

Make dicts on the hub that contain instances.
