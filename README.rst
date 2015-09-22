ode
===
This is a demo Flask app showcasing an API that returns GeoJSON from
attribute and simple spatial queries. It works on both Python 2 and 3.

If I have more time, I'll probably:

* add some functionality to limit the size of returned requests, or add
  pagination.
* add more spatial functionality, like filtering listing requests by custom
  AOI polygons.
* add more tests for 100% test coverage
* add more backend scripts, and enhance the existing ``import_listings.py``.

Prerequisites
-------------
ode uses PostgreSQL/PostGIS as its backend, so it's important to have that
installed on the system. Configuration is pretty minimal. For demo and testing
purposes, I use the postgres user and create a database called ``listings``.

Installation
------------
From source:

.. code:: bash

        $ ./setup.py install

``setup.py`` should fetch all required Python dependencies.

Scripts
-------

.. code::

        usage: import_listings.py [-h] [--engine_url ENGINE_URL] [--append] csv

        This script imports listing information from a csv file and inserts the data
        into a spatially-enabled listings table within a PostgreSQL database.

        positional arguments:
          csv                   path to the listing csv file

        optional arguments:
          -h, --help            show this help message and exit
          --engine_url ENGINE_URL
                                string that indicates database dialect and connection
                                arguments
          --append              append listing data to an existing table


Directory tree
--------------

.. code::

        .
        |-- ez_setup.py
        |-- ode
        |   |-- data
        |   |   `-- listings.csv
        |   |-- __init__.py
        |   `-- models.py
        |-- README.rst
        |-- requirements.txt
        |-- scripts
        |   `-- import_listings.py
        |-- setup.py
        `-- tests
            `-- test_get_request.py

