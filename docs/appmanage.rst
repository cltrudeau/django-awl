Installable Django App Tools
============================

When writing installable Django Apps, you need a hook to be able to run and
test them within a Django environment. The ``makemanage`` command creates a
``manage.py`` file for you in your project directory with exactly those hooks.

By default, ``makemanage`` looks for a "src" directory with a single module
inside of it as well as a directory named "tests". You can configure those
directories along with other parameters as well. The resulting ``manage.py``
script calls :func:`awl.appmanage.boot_django` to configure your environment.

Command line arguments to ``makemanage`` are:

* ``--src`` *dir_name*

    * Name of the directory that holds the module definition. If not provided,
      ``src`` is assumed

* ``--module`` *mod_name*

    * Name of the module to add to the ``INSTALLED_APPS`` settings

* ``--test`` *dir_name*

    * Name of the directory where tests can be found. If not provided, looks
      for ``tests``, otherwise acts as if there are none.

* ``--noawl``

    * Flag to indicate that the ``awl`` app should not be included in the
      resulting environment

* ``--root_url`` *text*

    * Provide a value for the ``ROOT_URL`` setting

* ``--template_dirs`` *text*

    * Comma separated list of directory names where Django looks for templates

* ``--config`` *text*

    * JSON dictionary to be used as ``**kwargs`` in the call that defines
      ``settings.py`` values

* ``--shebang`` *text*

    * Contents for the first line in the output script. On systems where
      ``os.name`` returns 'posix', defaults to '#!/usr/bin/env python',
      otherwise empty


.. automodule:: awl.appmanage
    :members:
