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
