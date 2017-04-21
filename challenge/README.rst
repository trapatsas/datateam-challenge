About the project
=================

Quick Start
-----------

- Unzip the archive **challenge_trapatsas_panayotis.tar.gz**
- Change directory ``` cd challenge/ ```
- Execute ``` pip install -r requirements.txt ```
- Inside **configuration** folder, open **settings-production.ini** and in section [Redis] change properties HOST and PORT to provide access to your redis server. Then save the file.
- Inside **configuration** folder, open **settings-test.ini** and in section [Redis] change properties HOST and PORT to provide access to your *test* redis server. Then save the file.
- Return to root folder and execute:
    1. ``` python -m unittest tests ``` to run all tests
    2. ``` python -m challenge ``` to run the project

Installation
------------

Dependencies
~~~~~~~~~~~~

This solution requires:

- Python (>= 3.2)
- Git
- Redis 3.2 or later (with GEO API support)

Redis should be populated with the iata codes or the application should be started using the optional argument *"-p yes"* to populate the database during initialization.

Requirements
~~~~~~~~~~~~

While inside the root directory, execute:

``` pip install -r requirements.txt ```

to install the necessary Python packages.

Settings
--------

Application settings can be changed by altering the configuration files (.ini) located in **configuration** directory.

The files use a specific naming convention: *settings-<ENVIRONMENT NAME>.ini*

You can create your own configuration file by copying one existing and changing the <ENVIRONMENT NAME>.

If you want to start the application using your file, the you should pass the relevant <ENVIRONMENT NAME> after the **"-e"** argument as explained below.

Usage
-----

**[!]** Please run all commands inside the project root directory

Example - Display help
~~~~~~~~~~~~~~~~~~~~~~

Displays help and exits

```
$ python -m challenge -h
usage: __main__.py [-h] [-e ENVIRONMENT] [-p POPULATE]
```

Script populates Redis with iata airport codes and then queries the database
to find the closest airport for a given pair of lat/long coordinates

optional arguments:
  -h, --help            show this help message and exit
  -e ENVIRONMENT, --environment ENVIRONMENT
                        Sets the environment. Relevant settings file MUST
                        exist.
  -p POPULATE, --populate POPULATE
                        Populates Redis with the available iata codes. Values:
                        yes|no

Example - Run with settings
~~~~~~~~~~~~~~~~~~~~~~~~~~~

```
$ python -m challenge -e production -p yes
```

The script expects to find a configuration file named *"configuration/settings-production.ini"* with the appropriate settings and then run the application using these settings. Default value: *"production"*

The are 2 existing sets of configuration: *production* and *test*. You may copy or change them to reflect your own settings.

Example - Run tests
~~~~~~~~~~~~~~~~~~~

```
$ python -m unittest tests
```

Runs all tests and displays the result. Also, requires access to a Redis server. Connection information can be changed in file *"configuration/settings-test.ini"*.
