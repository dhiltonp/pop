=========
Instances
=========

One of the largest challenges for developers moving over from OOP to Plugin
Oriented Programming is dealing with the concept of class instances. In
OOP it is fundamental to create a class and then created instances of said
class.

With the prevalence of *Subs* in Plugin Oriented Programming it becomes
easy to over conflate them with classes in OOP. While they share a few
conceptual overlaps, *Subs* are NOT classes, nor should they be treated as
such.

A developer will then, often, search for another situation where they can
conflate the concept of classes. They will often then reach for plugins.
Plugins are also, NOT classes.

Finally, classes can be used and when they are created they follow the same
rules for being exposed on the `hub` as functions. But even this practice is
mildly discouraged.

Classes should be used in Plugin Oriented Programming only when it is necessary
to either extend an existing library, or to create a type like interface
that is critical to an application. Classes should not be used for other
interfaces.

So why then is this chapter called "Instances"? The concept of an instance
goes beyond OOP and is still critical in software engineering and needs to be
fundamentally addressed in the development of a programming paradigm. Plugin
Oriented Programming does this through the namespace, rather than through
the heap, which is common for OOP languages.

Loosely Coupled Design
======================

Lets start by talking about loosely coupled and tightly coupled design. In
a tightly coupled design multiple constructs are tightly associated, they
exist in the same space and they tightly rely on each other. Plugin
Oriented Programming is, by definition, loosely coupled. By introducing
constructs that are both structured and loosely coupled it makes development
of highly portable code easier.

But, by definition, Plugin Oriented Programming is also tightly coupled.
Through app merging it becomes easy to create sub-api systems that are loosely
coupled, but also to create simple, abstract, high-level interfaces as well.
The continued goal is Plugin Oriented Programming, is to expose a system
that is highly opinionated, with significant flexibility, and solves both
sides of traditionally complicated problems.

This is one of the strengths of OOP, it allows for classes to be created
that can easily be linked together into larger applications. Unfortunately
if does not address coupling from an application vs library perspective and
it does not address data/function coupling.

The static nature of data/function coupling in OOP creates a tightly coupled
interface around classes, which leads to over isolation and over encapsulation
of code.

Plugin Oriented Programming seeks to overcome this challenge by making the
coupling between data and functions loose. This is accomplished via associative
coupling via the namespace.

When this happens, all of the data and functions are laid bare for the entire
application to see. This makes the loose coupling that is expressed in app merging
possible. This also makes the way in which instances are worked with very different
from traditional OOP development.

Plugin Oriented Programming also attempts to resolve the challenges with
loosely coupled design. Interfaces and messages get normalized via the construct
of the `hub` and are kept simple, small and consistent across local and remote
execution environments. Interdependency is expressed naturally through how the
code is constructed, as all Plugin Oriented code naturally expresses a consistent
hierarchical API.

Re Used Functions and Data on the Hub
=====================================

Using Python as an implementation example, when a class is instantiated, Python
creates instances of all of the functions, as objects, inside of the class
instance. This means that the functions defined in a class exist relative to
the class instance itself.

Plugin Oriented Programming creates instances of the functions relative to the
*Sub* that they exist in, but the function can interact with multiple named datasets
on the `hub`. This design is much more similar to how Julia creates classes.

In Julia a class is just a data structure, it is associated with functions
purely through the virtue of its type. So a method that operates on a type
simply accepts an instance of that type as an argument.

Plugin Oriented Programming rests in between these two constructs and introduces
a namespace. Functions in a *Sub* belong to the *Sub*, but functions in a *Sub*
can also work with named instances which are all tracked on the `hub`.

Here is some code to illustrate how this works. Lets assume we have a *Sub*
called `net`, the `init.py` file looks like this:

.. code-block:: python

    import uuid

    def __init__(hub):
        hub.net.POOLS = {}

    def pool(hub, pool):
        """
        Create the named connection pool
        """
        hub.net.POOLS[pool] = {}

    def add(hub, pool, addr, port):
        """
        Add a remote connection to the named pool
        """
        cname = uuid.uuid4()
        hub.net.POOLS[pool][cname] = hub.net.con.add(addr, port)
        return cname


In this simple example, we set up a data store on the hub called `POOLS` which
represents connection pools. Next we create a new pool, this gives us a named
instance that we can work with. Just pass the pool name into the functions that
operate on pools to have the pool get looked up on the `hub`.

Next we add a connection to the pool, this not only allows us to create a connection
that is tied to a specific pool. It also allows us to create nested references. In
this case we can now have many connections in each pool. This type of functional
layering allows for connections to be easily addressed at the pool layer and at
the connection layer.

Finally, there is the concept of decoupled management. A common source of memory leaks
is having too many connections open without cleaning the connections up. In this simple
example all of the connections are located in a predictable place. This makes it easy
to set up functions that can routines check in on the network connections and tidy
them up if they are experiencing any sort of difficulty.
