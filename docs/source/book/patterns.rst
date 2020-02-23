========
Patterns
========

Before we start into patters, it is necessary to own that there are many new concepts
and terms that are being introduced in Plugin Oriented Programming. It is, after all,
a new programming paradigm!

One of the goals of Plugin Oriented Programming is express the paradigm is as few concepts
as possible. If you recall some of the rules from earlier on, they stated over and over how
critical it is that code can be transferred to new people easily.

Similarly the paradigm needs to be easy to understand. So before you start to say "Hubs,
Subs, and Patterns! Oh My!", let me assure you that there are only a few more concepts
to learn, and that once you use them just a couple of times they quickly start to make sense.

Patterns are critical to Plugin Oriented Programming. When making pluggable software the ways
that plugins are applied needs to be consistent and understandable. This makes the software
pluggable not just because it exists in a plugin framework, but truly pluggable by design.

Patterns Are Extensible
=======================

If software is not written in an extensible and pluggable way then even if it is built inside
of a plugin framework, that does not make the software pluggable.

When making a *Sub* consider how the interface can be extended, and created, via the additions
of plugins. Different established patterns do this in different ways.

Lets take a look at a few of the patterns that exist in the wild to see how these problems
are commonly dealt with.

Collection Pattern
==================

The Collection Pattern is used to collect data. It is useful when downloading and combining
data from multiple sources, or scanning hardware for specific properties. A great example for
this pattern is a little application called "Grains" that is used to collect system data.

The `grains` system creates a common and simple pattern. It runs all of the exposed functions
found in the grains *Sub* and those functions in turn extend a data structure found on the `hub`.

Lets take a look at the `init.py` file for `grains`:

.. code-block:: python

        # Import python libs
        import asyncio


        def __init__(hub):
            # Set up the central location to collect all of the grain data points
            hub.pop.sub.load_subdirs(hub.grains, recurse=True)
            hub.grains.GRAINS = {}


        async def collect(hub):
            """
            Collect the grains that are presented by all of the app-merge projects that
            present grains.
            """
            await hub.grains.init.run_sub(hub.grains)
            # Load up the subs with specific grains
            await hub.grains.init.process_subs()


        async def run_sub(hub, sub):
            """
            Execute the contents of a specific sub, all modules in a sub are executed
            in parallel if they are coroutines
            """
            coros = []
            for mod in sub:
                if mod.__sub_name__ == "init":
                    continue
                for func in mod:
                    ret = func()
                    if asyncio.iscoroutine(ret):
                        coros.append(ret)
            for fut in asyncio.as_completed(coros):
                await fut


        async def process_subs(hub):
            """
            Process all of the nested subs found in hub.grains
            Each discovered sub is hit in lexicographical order and all plugins and functions
            exposed therein are executed in parallel if they are coroutines or as they
            are found if they are natural functions
            """
            for sub in hub.pop.sub.iter_subs(hub.grains, recurse=True):
                await hub.grains.init.run_sub(sub)


The __init__ Function
---------------------

The `__init__` function is simple, as it should be. It recursively loads nested *Subs*
that have been created and sets up a dict on the `hub` inside of the `grains` namespace.
Since the `GRAINS` dict is all caps we know it is not a function or a *Sub*, it is a variable.
The `GRAINS` dict is also located under `hub.grains`. This means that all plugins created on
the *Sub* are intended to have write access to the `hub.grains.GRAINS` variable.

The run_sub Function
--------------------

Next we have the meat of the pattern. The `run_sub` function is simple. It just iterates over
all of the plugins exposed in a *Sub* and calls them! If they are a coroutine then they get
awaited in a batch. But the end result is simple, any plugin that is added will be found,
and all functions will be called when the pattern is executed.

A Grains Plugin
---------------

Now that we have the pattern down, let's say that we add another file to the *Sub* called
`test.py`:

.. code-block:: python

    async def test(hub):
        hub.grains.GRAINS["test"] = True

An Extensible Pattern
---------------------

We now have a simple pattern! The test function will be found and executed inside of the
run_sub function, and that function in turn obeys the interface and adds the desired data
onto the `hub.grains.GRAINS` dict.

Spine Pattern
=============

The spine pattern defines the startup spine of an application. This is a pattern where your
application loads up configuration data, starts worker processes and loads the bulk of the subsystems
to be used.

While many projects will have a simple cli startup sequence, that does not constitute a spine pattern.
Most projects should not have what would be considered a *Spine* pattern, this pattern should
be thought of as a pattern that itself is used to app-merge many other projects.

This is also a reason why loading configuration data or starting an async loop should not happen in
the `__init__` function for any *Sub*.

This is yet another opportunity to cover the fact that all projects should be small and brought
together in tight efficient ways. Here are a few things that are commonly done inside of a
*Spine* pattern:

* Set up the core data structures used by the application
* Load up `conf` and read in the application configuration
* Load up additional subsystems
* Start up an asyncio loop
* Start the main coroutines or functions
* Start the patterns in the *Subs'* `init.py` files

Beacon Pattern
==============

The beacon pattern is used to gather events. In this example we will make a simple
crypto-currency tracker. The *Sub* in this example will be called `beacons`, it uses
an asyncio queue to collect and store data. This would be a simple *init.py*:

.. code-block:: python

    # Import python libs
    import asyncio


    def __init__(hub):
        """
        Set up the local data stores
        """
        hub.beacons.QUE = asyncio.Queue()


    async def start(hub):
        """
        Start the beacon listening process
        """
        gens = []
        for mod in hub.beacons:
            if not hasattr(mod, "listen"):
                continue
            func = getattr(mod, "listen")
            gens.append(func())
        async for ret in hub.pop.loop.as_yielded(gens):
            await hub.beacons.QUE.put(ret)

This example shows iterating over the modules found in the `beacons` *Sub*. The plugins are
defined as needing to implement an async generator function. We call the async generator
function which returns an async generator that gets appended to a list. That list is then
passed to the `as_yielded` function that yields as the next async generator yields. The
yielded data is then added to a QUE that can be ingested elsewhere.

Following this pattern a plugin that emits a beacon could subsequently look like this:

.. code-block:: python

    import asyncio
    import aiohttp

    async def listen(hub):
        while True:
            async with aiohttp.ClientSession() as session:
                async with session.get("https://api.cryptonator.com/api/full/btc-usd") as resp:
                    yield(resp.json())
            await asyncio.sleep(5)

Now we have a bitcoin ticker. More modules could act as means to gather data about other
crypto-currencies. The pattern expressed here makes tracking more coins easy and allows for a
separate *Sub* to process the collected data.

This pattern shows the concept of exposing reusable interfaces in a great way. This example
does not care what is pulling the data off the queue, it just has a single function, to place
said data on the queue. Now many different *Subs* could be used to read the output data in
multiple ways.

Flow Pattern
============

The flow pattern is used for flow based interfaces. This follows an async pattern where
data is queued and passed into and/or out of the subsystem. This is an excellent
pattern for applications that do data processing. Data can be loaded into the pattern,
processed, and sent forward to the next interface for processing. This pattern is used to
link together multiple flow subsystems or to take data from a beacon or collection
pattern and process it.

In the *init.py* file start a coroutine that waits on an async queue that is fed by another
subsystem.

.. code-block:: python

    import asyncio

    def __init__(hub):
        hub.flows.QUE = asyncio.Queue()


    async def start(hub, mod):
        while True:
            data = await hub.beacons.QUE.get()
            ret = await getattr(f"flows.{mod}.process"){data}
            await hub.flows.QUE.put(ret)

Using a flow pattern makes pipe-lining concurrent data fast and efficient. For a more elegant
example take a look at the internals of the `umbra` project.

Router Pattern
==============

The router pattern is used to take input data and route it to the correct function and route
it back. This is typically used with network interfaces. A typical *init.py* will look something
like this:

.. code-block:: python

    import aiohttp

    def start(hub):
        app = asyncio.web.Application()
        app.add_routes([asyncio.web.get("/", hub._.router)])
        aiohttp.web.run_app(app)

    async def router(hub, request):
        data = request.json()
        if "ref" in data:
            return web.json_response(getattr(hub.server, data["ref"])(**data.get("kwargs")))

This example assumes that the sender is sending a json payload with 2 keys, one called "ref"
to reference the function on the `hub` and another called "kwargs" so that any arguments
can also be sent. This can be a great and simple way to expose part of the `hub` to the network.

Now the plugin subsystem can be populated with modules that expose request functions.

Just Examples
=============

There are many ways to create patterns. These examples are not intended to be a document of all
available patterns, but are meant to get you thinking about what kinds of patterns you can
make inside of a Plugin Oriented Programming system.

Remember to make your *Subs* follow patterns to expose a re-usable interface! That will make
every aspect of your code pluggable!

Plugins Allow for App Merging!
==============================

We have eluded to *App Merging* a few times, well, the excitement is finally here! App Merging
is one of the most powerful aspects of Plugin Oriented Programming, and it is in the next
chapter.

Now that you know about the `hub`, *Subs*, plugins, and patterns; there is only one more
high level concept to get familiar with, App Merging. Plugin Oriented Programming apps
are not just made from plugins, they are plugins! Read on to learn how!
