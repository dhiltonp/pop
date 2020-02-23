===============
Getting Started
===============

Plugin Oriented programming is implemented in Python via a project called `pop`.
Gettign started with `pop` is easy and the rest of this book will be using `pop`
to illustrate aspects of Plugin Oriented Programming.

The `pop` project makes using Plugin Oriented Programming easy by providing the
implementation, but also the tools, that make gettign started and maintianing
projects easy.

Getting started is a cinch, just install `pop` and make a project.

Install and Run
===============

The `pop` project is available on pypi and can be easily installe via Python's
package manager, `pip`:

.. code-block:: bash

    pip install pop

Once `pop` is installed, make a new directory and run `pop-seed` to make a new
project, in this case, called poppy:

.. code-block:: bash

    mkdir poppy
    pop-seed poppy

This will generate all of the Python boiler plate code that you need to make
a standard python project, as well as the style enforcement code to make
your project clean.

Once this has run you will see a direcotry called `poppy` that contains the
`conf.py`, `scripts.py` and `version.py`, as well as another `poppy` directory.

As we go through how `pop` works the results of this command will become aparent.

The `pop-seed` command also left a file called `run.py`. This allows you to easily
run your `pop` project from the root of the source code tree. Give it a shot:

.. code-block:: bash

    python3 run.py

You should see the output `poppy works`, this is being run from
`poppy/poppy/init.py`.

Moving Forward
==============

Getting started with `pop` is covered in the `pop` quickstart guide but it makes
sense to cover the basics here. `pop-seed` will be referenced in a number of
places moving forward, as well as files like the `conf.py`. This brief respite
was provided here to ensure that there is a little context.
