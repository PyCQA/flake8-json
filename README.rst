Flake8-JSON
===========

This is a plugin for Flake8 that will format the output as JSON. The output of
the default JSON formatter is not pretty-printed. If you'd like the output to
be pretty-printed, use json-pretty instead.

CodeClimate support is also offered through this plugin as of v20.12.0


Installation
------------

.. code-block:: bash

    pip install flake8-json


Usage
-----

.. code-block:: bash

    flake8 --format=json ...

.. code-block:: bash

    flake8 --format=json-pretty ...

.. code-block:: bash

    flake8 --format=codeclimate ...


Competitors
-----------

None that I could find on PyPI


Maintenance Policy
------------------

This project is seeking maintainers. Please open an issue if you're interested
and ensure that you've read the PyCQA's `Code of Conduct`_.


.. _Code of Conduct:
    http://meta.pycqa.org/en/latest/code-of-conduct.html
