Waelsteng
=========
    [wel stæŋ]  / *noun* 
    
    1) literal: "death pole" or "slaugher pole"; 
    2) Anglo Saxon tool for impailing enemies or those who had done wrong; 
    3) A collection of django testing tools

Testing Django Views
--------------------

.. automodule:: awl.waelsteng
    :noindex:
    :members: FakeRequest


Testing Admin Classes
---------------------

.. automodule:: awl.waelsteng
    :members: create_admin, AdminToolsMixin


WRunner
-------

This is an alternate to :class:`DiscoverRunner`.  Main differences are:

* Creates and destroys a media directory for uploads during testing
* Calls a dynamic method for loading test data
* Allows for short-form versions of test labels
* Sets static file handling to :class:`StaticFilesStorage`

Like any other runner, you can use it for your django tests by changing your
settings:

.. code-block:: python

    TEST_RUNNER = 'awl.waelsteng.WRunner'

Configuration is done inside of the django settings module:

.. code-block:: python

    WRUNNER = {
        'CREATE_TEMP_MEDIA_ROOT':True,
        'TEST_DATA':'package.module.function_name'
    }

If ``CREATE_TEMP_MEDIA_ROOT`` is set, then a directory is created and the
``settings.MEDIA_ROOT`` attribute is changed for the tests.  The directory is
then destoryed upon test completion.

If ``TEST_DATA`` is set, then the named function is loaded and run after the
database is created.  This hook can be used to create test data.

Shortcut test labels (using :func:`wrench.waelstow.find_shortcut_tests`) are
supported by this runner.  Any label that starts with "=" is checked against
all tests for substring matches.  
