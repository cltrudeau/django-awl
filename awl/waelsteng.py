# awl.waelsteng.py
#
# DOCUMENTATION ALERT: autodoc is explicit about what is included in this
# module in order to handle some better grouping of items.  New things will
# need to be explicitly added to docs/waelsteng.rst
#
import os, shutil
from unittest import TestSuite

from django.conf import settings
from django.contrib import admin
from django.contrib.admin.utils import lookup_field
from django.contrib.auth.models import User
from django.test.runner import DiscoverRunner, reorder_suite

from six.moves.html_parser import HTMLParser

from wrench.utils import dynamic_load
from wrench.waelstow import find_shortcut_tests

# ============================================================================
# View Testing Tools
# ============================================================================

class FakeRequest(object):
    """Simulates a request object"""
    def __init__(self, user=None, method='GET', cookies={}, data={}):
        """Constructor

        :param user:
            Django User object to include in the request.  Defaults to None.
            If none is given then the parameter is not set at all
        :param method:
            Request method.  Defaults to 'GET'
        :param cookies:
            Dict containing cookies for the request.  Defaults to empty
        :param data:
            Dict for get or post fields.  Defaults to empty
        """
        super(FakeRequest, self).__init__()
        self.method = method
        self.COOKIES = cookies
        if user:
            self.user = user
        if method == 'GET':
            self.GET = data
        else:
            self.POST = data

        self.path = '/fake/path/'

    def get_host(self):
        return 'test_host'


def create_admin(username='admin', email='admin@admin.com', password='admin'):
    """Create and save an admin user.

    :param username:
        Admin account's username.  Defaults to 'admin'
    :param email:
        Admin account's email address.  Defaults to 'admin@admin.com'
    :param password:
        Admin account's password.  Defaults to 'admin'
    :returns:
        Django user with staff and superuser privileges
    """
    admin = User.objects.create_user(username, email, password)
    admin.is_staff = True
    admin.is_superuser = True
    admin.save()
    return admin

# ============================================================================
# Tools for testing Django Admin Modules
# ============================================================================

class AnchorParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        self.href = ''
        for attr in attrs:
            if attr[0] == 'href':
                self.href = attr[1]
                break


class AdminToolsMixin(object):
    """This mixin is used to help test django admin objects using the django
    client interface.  A superuser is created during setup which can then be
    used throughout.  

    .. note::

        :class:`AdminToolsMixin.initiate` must be called in the inheritor's
        :class:`TestCase.setUp` method to properly initialize.

    Once :class:`AdminToolsMixin.intiate` is called, the following will be
    available:

    :param site:
        An instance of an ``AdminSite`` to test against
    :param admin_user:
        A User object with staff and superuser privileges
    """
    #: Admin account's username during the tests
    USERNAME = 'admin'
    #: Admin account's password during the tests
    PASSWORD = 'admin'
    #: Admin account's email during the tests
    EMAIL = 'admin@admin.com'

    def initiate(self):
        """Sets up the :class:`AdminSite` and creates a user with the
        appropriate privileges.  This should be called from the inheritor's
        :class:`TestCase.setUp` method.
        """
        self.site = admin.sites.AdminSite()
        self.admin_user = create_admin(self.USERNAME, self.EMAIL, self.PASSWORD)
        self.authed = False

    def authorize(self):
        """Authenticates the superuser account via the web login."""
        response = self.client.login(username=self.USERNAME, 
            password=self.PASSWORD)
        self.assertTrue(response)
        self.authed = True

    def authed_get(self, url, response_code=200, headers={}):
        """Does a django test client ``get`` against the given url after
        logging in the admin first.

        :param url:
            URL to fetch
        :param response_code:
            Expected response code from the URL fetch.  This value is
            asserted.  Defaults to 200
        :param headers:
            Optional dictionary of headers to send in the request
        :returns:
            Django testing ``Response`` object
        """
        if not self.authed:
            self.authorize()

        response = self.client.get(url, **headers)
        self.assertEqual(response_code, response.status_code)
        return response

    def authed_post(self, url, data, response_code=200, follow=False,
            headers={}):
        """Does a django test client ``post`` against the given url after
        logging in the admin first.

        :param url:
            URL to fetch
        :param data:
            Dictionary to form contents to post
        :param response_code:
            Expected response code from the URL fetch.  This value is
            asserted.  Defaults to 200
        :param headers:
            Optional dictionary of headers to send in with the request
        :returns:
            Django testing ``Response`` object
        """
        if not self.authed:
            self.authorize()

        response = self.client.post(url, data, follow=follow, **headers)
        self.assertEqual(response_code, response.status_code)
        return response

    def visit_admin_link(self, admin_model, instance, field_name,
            response_code=200, headers={}):
        """This method is used for testing links that are in the change list
        view of the django admin.  For the given instance and field name, the
        HTML link tags in the column are parsed for a URL and then invoked
        with :class:`AdminToolsMixin.authed_get`.

        :param admin_model:
            Instance of a :class:`admin.ModelAdmin` object that is responsible
            for displaying the change list
        :param instance:
            Object instance that is the row in the admin change list
        :param field_name:
            Name of the field/column to containing the HTML link to get a URL
            from to visit
        :param response_code:
            Expected HTTP status code resulting from the call.  The value of
            this is asserted.  Defaults to 200.
        :param headers:
            Optional dictionary of headers to send in the request
        :returns:
            Django test ``Response`` object
        :raises AttributeError:
            If the column does not contain a URL that can be parsed
        """
        html = self.field_value(admin_model, instance, field_name)
        try:
            parser = AnchorParser()
            parser.feed(html)
            url = parser.href
            if not url:
                raise AttributeError()
        except:
            raise AttributeError('href could not be parsed from *%s*' % html)

        return self.authed_get(url, response_code=response_code,
            headers=headers)

    def field_value(self, admin_model, instance, field_name):
        """Returns the value displayed in the column on the web interface for
        a given instance.

        :param admin_model:
            Instance of a :class:`admin.ModelAdmin` object that is responsible
            for displaying the change list
        :param instance:
            Object instance that is the row in the admin change list
        :field_name:
            Name of the field/column to fetch
        """
        _, _, value = lookup_field(field_name, instance, admin_model)
        return value

    def field_names(self, admin_model):
        """Returns the names of the fields/columns used by the given admin
        model.

        :param admin_model:
            Instance of a :class:`admin.ModelAdmin` object that is responsible
            for displaying the change list
        :returns:
            List of field names
        """
        request = FakeRequest(user=self.admin_user)
        return admin_model.get_list_display(request)

# ============================================================================
# Alternate Runner
# ============================================================================

class WRunner(DiscoverRunner):
    # documentation for this is directly in waelsteng.rst
    def __init__(self, **kwargs):
        if 'verbosity' not in kwargs:
            kwargs['verbosity'] = 2

        w_settings = getattr(settings, 'WRUNNER', {})
        self.test_media_root = w_settings.get('MEDIA_ROOT', '')
        self.test_data = w_settings.get('TEST_DATA', '')

        super(WRunner, self).__init__(**kwargs)

    def setup_test_environment(self, **kwargs):
        super(WRunner, self).setup_test_environment(**kwargs)
        settings.STATICFILES_STORAGE = \
            'django.contrib.staticfiles.storage.StaticFilesStorage'

        if self.test_media_root:
            settings.MEDIA_ROOT = self.test_media_root
            try:
                os.makedirs(self.test_media_root)
            except:
                pass # ignore errors if directory existed

    def setup_databases(self, **kwargs):
        result = super(WRunner, self).setup_databases(**kwargs)

        if self.test_data:
            data_fn = dynamic_load(self.test_data)
            data_fn()

        return result

    def teardown_databases(self, old_config, **kwargs):
        super(WRunner, self).teardown_databases(old_config, **kwargs)
        if self.test_media_root:
            shutil.rmtree(self.test_media_root)

    def build_suite(self, test_labels, extra_tests=None, **kwargs):
        shortcut_labels = []
        full_labels = []
        for label in test_labels:
            if label.startswith('='):
                shortcut_labels.append(label)
            else:
                full_labels.append(label)

        shortcut_tests = []
        if shortcut_labels:
            suite = super(WRunner, self).build_suite([], extra_tests, **kwargs)
            shortcut_tests = find_shortcut_tests(suite, shortcut_labels)

        if full_labels:
            suite = super(WRunner, self).build_suite(full_labels, extra_tests,
                **kwargs)
            suite.addTests(shortcut_tests)
        elif shortcut_tests:
            # only have shortcut labels
            suite = TestSuite(shortcut_tests)
        else:
            # no labels at all, do the default
            suite = super(WRunner, self).build_suite([], extra_tests, **kwargs)

        # parent implementation reorders, so we'll do it too
        return reorder_suite(suite, self.reorder_by)
