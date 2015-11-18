0.8.1
======

* added "as" syntax to accessor templatetag

0.8
===

* added accessor templatetag

0.7
===

* removed unused imports
* added getitem templatetag

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
