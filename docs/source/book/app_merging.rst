===================================
App Merging - Making Apps Pluggable
===================================

One of the great challenges in software development is the separation of the
app from the library. While it has been taught over and over to place as much
code as possible in libraries, this is just not how the world works. It is
far to easy to place large amounts of code in an application and not make
the components of the application into a library.

Why is this? It is not a entirely technical problem. This is a deeply human problem.

Humans want to do things that are easy, we often make choices about how to
build and create things, not based on what is wise, or good engineering,
but based on what we perceive to be easy!

Take special note of the word "Perceive". We don't make choices based on what
is actually easy, but what we THINK is easy. This is a hallmark of engineering today,
to take shortcuts that destroy our productivity down the road.

To solve this problem we must make technical options that are both easy to
execute and scale. This is a difficult feat! The mere nature of scaling
software is deeply complicated.

App Merging seeks to solve this problem. Making complex systems work is based
on the creation of reusable components that can be put together in grad ways.
When making a large building almost every component of the building already
exists and can be purchased without customization. The new building will require
some custom components, and a few new ones, but the vast majority of them will
already exist.

In Plugin Oriented Programming the components of larger software systems get created
in a pluggable way, by design. When you are presented with a very complex problem
often the best way to solve it is by making the surface area of the problem smaller.
Reshape what aspects of the problem can be solved so that the difficult bit
is only applied to the smallest space that it needs to be. Plugin Oriented Programming
is built with this express situation in mind.

Horizontal App Merging
======================

App Merging  comes in two flavors, Horizontal and Vertical. Horizontal is similar
to importing a library, but instead of the import being relative to a code file
like it is in so many languages, it is relative to the `hub`.

This means that *Horizontal App Merging* is just the act of adding a new *Sub*
onto your `hub` from another application. That's it!

This solves the App vs Library problem, because when you make an app in Plugin
Oriented Programming, it IS ALSO A LIBRARY! Instead of trying to teach people to
write code in two distinct worlds, why not just make a world where everything is
pluggable?

There are a few more considerations to *Horizontal App Merging*. If it were so
simple then it would have been solved years ago! The main issue we have it
application startup and configuration. Apps need to be configured! Plugin
Oriented Programming solves this issue as well. If apps need configuration
to be applied during startup then the interface for multiple apps to get
configured needs to be normalized.

Configuration Integration
-------------------------

Plugin Oriented Programming therefore cannot work without the `conf.integrate`
system that is built into `pop`. The `conf.integrate` system allows for the
configuration from multiple applications to be merged together in a consistent
namespace.

When setting up configuration from applications information needs to be taken
from multiple sources and applied in the correct order. Command line flags,
configuration files, defaults, and environment data all need to be accounted
for. Defaults are over ridden by config files, which are overridden by
environment data, which are overridden by command line flags.

The gathered configuration data is then added to the `hub` in dict called `OPT`.
Each application's configuration is then stored in `OPT` under the name of the
application that defined the configuration parameter. The `conf.integrate` system
also allows for configuration collisions to be taken care of. This allows for
configurations that are set for multiple applications to be seamlessly merged into
one large application.

Vertical App Merging
====================

*Horizontal App Merging* allows for subs and configurations from multiple codebases to be merged onto a
single application. *Vertical App Merging* allows for plugins to be dynamically merged
from multiple codebases. This means that if you define a new *Sub* called `rainbows` you
can define that *Sub* as a *Dynamic Name*. When this happens a third party
can extend your *Sub*. If you define your Sub as a *Dynamic Name* then
anyone else can define a standalone project that extends your *Sub*, or even a collection
of *Subs*.

This allows third parties to publish extensions and contributions to your code without
you having to review their code, or maintain their code. This is helpful on many levels.

Valuable Time
-------------

The best judge of code viability is public use, but large amounts of code is merged
into widely used projects every day. The result is that the head of a software project
must review all code that is submitted to their project.

Your time, as a head of a project, is FAR more valuable being used authoring new
features and capabilities, than being consumed in code reviews. The world's best
developers are robbed from their trade on an ongoing basis, by needing to review
and more often than not reject, code that they never wanted in the project to begin
with.

Contributions can be deeply beneficial, but hey can also make the creator of a
codebase a slave to their community. Many open source developers quit because of
the difficulty involved in maintaining a community. These people are excellent
software developers, but instead they get forced into becoming community stewards.
Worse still, established communities are very often taken over by hostile members
who are not kind to the original developer.

Why would we continue to subject ourselves to this abuse? *Vertical App Merging*
is directly intended to address this problem. Instead of needing to review code
contributors can publish and maintain their own code, in their own communities.
This allows for the contribution count to drop to more manageable levels and
becomes focused on the areas of the code that are most important to the developer
running the project.

This also creates a more healthy community, without a single gatekeeper, that has
been forced to be a gatekeeper, different groups can operate independently. They
can grow independently, and prove their merit as developers independently. This
drives better code, more development for engineers and allows the best engineers to
do what they love, be an engineer.
