0.23.1
======

* made second parameter to json_post_required decorator optional

0.23.0
======

* added json_post_required() decorator

0.22.2
======

* updated minimum library requirements for django 2.0.2 and 2.1.2 to reflect
security updates

0.22.1
======

* test labels weren't working properly, due to a problem in waelstow the 
bug was hidden; waelstow 0.10.2 fixes the issue; WRunner.build_suite() 
could be vastly simplified with the change as well

0.22
====

* added ability to change the title for a list_display item using 
fancy_modeladmin() 

0.21.1
======

* fixed a bug where multiple uses of fancy_modeladmin() resulted all classes
using the same list_display field

0.21
====

* added fancy_modeladmin() which is a replacement for make_admin_mixin, 
simpler to use and supports other types of list_display modifiers

0.20
====

* added print_setting django management command which prints django settings
to the screen, useful for getting setting info into external scripts

0.19
====

* added "add_obj_ref()" method to admintools make_admin_mixin utility

0.18.2
======

* forgot to update sample_site with new test classes

0.18.1
======

* fixed bug in admintools: django 2.0 admin requires explicit marking of 
strings safe, some
* updated sample_site and test models to be understandable classes (Books,
Authors, etc.) instead of abstract (Inner, Outer, Nested)
* updated sample_site to work with django 2.0

0.18
====

* added get_field_names() utility

0.17.1
======

* upgraded dependancies to a working version of screwdriver
* changed wheel build to be universal

0.17
====

* Removed dependancies on deprecated "wrench" library

0.16
====

* Support for Django 2.0
* no longer test for Django 1.10 (should work, not tested)

0.15
====

* WRunner now supports creating a temporary directory for MEDIA_ROOT and
removing it on exit

0.14
====

* removed Django 1.8, 1.9 compatability (may still work, no longer tested)
* added Django 1.11 compatability
* added python 3.6 compatability
* added Choices object 
    * easy way of creating django's tuple-of-tuple structure used in choices
    lists, etc.
* added QuerySetChain: a query set that chains other querysets together

0.13
====

* added support for python 3.5

0.12
====

* added support for Django 1.10

0.11.1
======

* improved handling of messages_from_response() so that it can deal with
responses without contexts but with the message cookie set

0.11
====

* Added messages_from_response() helper in waelsteng which pulls
contrib.message objects out of a response from client.get() or client.post()

0.10.2
======

* added "follow=False" keyword to AdminToolsMixin.authed_get()

0.10.1
======

* improved KeyError handling in the accessor template tag

0.10
====

* made django-awl compatible with Django 1.9
* separated models and abstract models to avoid depracation warnings being
in Django 1.9 
    * even if only loading an abstract model from models.py the module gets
    loaded and django sees the concrete models in the file which aren't in
    INSTALLED_APPS and issues a warning
    * now only concrete models are in models.py and the abstract ones are in
    absmodel.spy

0.9
===

* added css_colours module, tests for values that are valid CSS colours

0.8.2
======

* fixed getitem template filter so that it handles key errors silently

0.8.1
======

* added "as" syntax to accessor templatetag

0.8
===

* added accessor templatetag

0.7
===

* removed unused imports
* added getitem template filter

0.6.1
=====

* yet another make_admin_obj_mixin null bug, yay! for testing

0.6
===

* removed django 1.7 compatibility
* internal change from AnchorParser to wrench.utils.parse_link
* fixed bug where make_admin_obj_mixin wasn't handling null FK properly

0.5.1
=====

* fixed documentation errors in rankedmodels
* fixed bug where the wrong obj was being shown in the admin_obj_link

0.5
===

* django version of default_logging_dict
* fixed bug in WRunner where empty test labels did not return all tests

0.4
===

* added utilities:
    * refetch_for_update
    * render_page
    * render_page_to_string
* added model classes:
    * Counter
    * Lock
* added model abstract class:
    * ValidatingMixin
* re-ogranized testing structure to deal with migrations needed from the
    addition of the new concrete model classes 

0.3
===

* added context processor extra_context

0.2
===

* added a new DiscoverRunner implementation: WRunner

0.1
===

* initial commit to pypi
