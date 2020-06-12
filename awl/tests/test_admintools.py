# awl.tests.test_admintools.py
from django.contrib.admin.utils import label_for_field
from django.test import TestCase
from django.utils.safestring import SafeData

from screwdriver import parse_link

from awl.waelsteng import AdminToolsMixin
from awl.tests.models import (Author, Book, Chapter, Driver, VehicleMake, 
    VehicleModel)
from awl.tests.admin import (BookAdmin, ChapterAdmin, DriverAdmin,
    VehicleModelAdmin)

# ============================================================================

class AdminToolsTest(TestCase, AdminToolsMixin):
    def test_admin_obj_mixin(self):
        # setup the admin site and id
        self.initiate()

        book_admin = BookAdmin(Book, self.site)
        chapter_admin = ChapterAdmin(Chapter, self.site)

        tolstoy = Author.objects.create(name='Tolstoy')
        war = Book.objects.create(name='War and Peace', author=tolstoy)
        ch1 = Chapter.objects.create(name='Part I.I', book=war)

        # make sure we get a safe string
        html = self.field_value(book_admin, war, 'show_author')
        self.assertTrue(issubclass(html.__class__, SafeData))

        # check the basic __str__ named link from Book to Author
        html = self.field_value(book_admin, war, 'show_author')
        url, text = parse_link(html)
        self.assertEqual('Author(id=1 Tolstoy)', text)
        self.assertEqual('/admin/tests/author/?id__exact=1', url)

        # check the template based name link of Book from Chapter
        html = self.field_value(chapter_admin, ch1, 'show_book')
        url, text = parse_link(html)
        self.assertEqual('Book.id=1', text)
        self.assertEqual('/admin/tests/book/?id__exact=1', url)

        # check the double dereferenced Author from Chapter
        html = self.field_value(chapter_admin, ch1, 'show_author')
        url, text = parse_link(html)
        self.assertEqual('Author(id=1 Tolstoy)', text)
        self.assertEqual('/admin/tests/author/?id__exact=1', url)

        # check readonly, double dereferenced Author from Chapter
        result = self.field_value(chapter_admin, ch1, 'readonly_author')
        self.assertEqual('Author(id=1 Tolstoy)', result)
        result = self.field_value(chapter_admin, ch1, 'readonly_book')
        self.assertEqual('RO Book.id=1', result)

        # check the title got set correctly
        label = label_for_field('show_book', ch1, chapter_admin)
        self.assertEqual(label, 'My Book')

        # check that empty values work properly
        ch2 = Chapter.objects.create(name='Part I.II')
        result = self.field_value(chapter_admin, ch2, 'show_author')
        self.assertEqual('', result)

        book = Book.objects.create(name='book')
        ch2.book = book
        ch2.save()
        result = self.field_value(chapter_admin, ch2, 'show_author')
        self.assertEqual('', result)

        result = self.field_value(chapter_admin, ch2, 'readonly_author')
        self.assertEqual('', result)


    def test_fancy_modeladmin(self):
        # setup the admin site and id
        self.initiate()

        driver_admin = DriverAdmin(Driver, self.site)
        vehiclemodel_admin = VehicleModelAdmin(VehicleModel, self.site)

        toyota = VehicleMake.objects.create(name='Toyota')
        tercel = VehicleModel.objects.create(name='Tercel', vehiclemake=toyota,
            year=1999)
        bob = Driver.objects.create(name='Bob', vehiclemodel=tercel, 
            rating=0.35)

        vehiclemake_field = driver_admin.list_display[2]
        vehiclemodel_field = driver_admin.list_display[3]
        ro_vehiclemake_field = driver_admin.list_display[4]
        ro_vehiclemodel_field = driver_admin.list_display[5]
        rating_field = driver_admin.list_display[6]
        rating_field_templated = driver_admin.list_display[7]

        year_field = vehiclemodel_admin.list_display[2]
        default_set_field = vehiclemodel_admin.list_display[3]
        custom_set_field = vehiclemodel_admin.list_display[4]

        # make sure we get a safe string
        html = self.field_value(driver_admin, bob, vehiclemake_field)
        self.assertTrue(issubclass(html.__class__, SafeData))

        # check the basic __str__ named link from Student to Teacher
        html = self.field_value(driver_admin, bob, vehiclemake_field)
        url, text = parse_link(html)
        self.assertEqual('VehicleMake(id=1 Toyota)', text)
        self.assertEqual('/admin/tests/vehiclemake/?id__exact=1', url)

        # check the template based name link of Course from Student
        html = self.field_value(driver_admin, bob, vehiclemodel_field)
        url, text = parse_link(html)
        self.assertEqual('Toyota Tercel id=1', text)
        self.assertEqual('/admin/tests/vehiclemodel/?id__exact=1', url)

        # check readonly fields
        result = self.field_value(driver_admin, bob, ro_vehiclemake_field)
        self.assertEqual('VehicleMake(id=1 Toyota)', result)
        result = self.field_value(driver_admin, bob, ro_vehiclemodel_field)
        self.assertEqual('RO Toyota Tercel id=1', result)

        # check the titles got set correctly
        label = label_for_field(vehiclemodel_field, bob, driver_admin)
        self.assertEqual(label, 'My Vehicle Model')
        label = label_for_field(ro_vehiclemodel_field, bob, driver_admin)
        self.assertEqual(label, 'RO Vehicle Model')

        # check that empty values work properly
        fred = Driver.objects.create(name='Fred')
        result = self.field_value(driver_admin, fred, vehiclemodel_field)
        self.assertEqual('<i>no model</i>', result)
        result = self.field_value(driver_admin, fred, vehiclemake_field)
        self.assertEqual('', result)

        result = self.field_value(driver_admin, fred, ro_vehiclemodel_field)
        self.assertEqual('', result)
        result = self.field_value(driver_admin, fred, ro_vehiclemake_field)
        self.assertEqual('', result)

        # check formatted field
        result = self.field_value(driver_admin, bob, rating_field)
        self.assertEqual('0.3', result)

        # check templated field
        result = self.field_value(driver_admin, bob, rating_field_templated)
        self.assertEqual('Bob 0.35', result)

        # check display with title
        result = self.field_value(vehiclemodel_admin, tercel, year_field)
        self.assertEqual(1999, result)

        label = label_for_field(year_field, tercel, vehiclemodel_admin)
        self.assertEqual(label, 'YEAR TITLE')

        # check display with title with empty result
        yearless = VehicleModel.objects.create(name='Yearless', 
            vehiclemake=toyota)
        result = self.field_value(vehiclemodel_admin, yearless, year_field)
        self.assertEqual('<i>no year</i>', result)

        # Validate the add_fk_link method with default values
        html = self.field_value(vehiclemodel_admin, tercel,
            default_set_field)
        url, text = parse_link(html)
        self.assertEqual('1 Driver', text)
        self.assertEqual('/admin/tests/driver/?vehiclemodel__id=1', url)

        label = label_for_field(default_set_field, tercel, vehiclemodel_admin)
        self.assertEqual('Driver', label)

        # Validate the add_fk_link method with custom values
        html = self.field_value(vehiclemodel_admin, tercel,
            custom_set_field)
        url, text = parse_link(html)
        self.assertEqual('Tercel 1 Driver Title', text)
        self.assertEqual('/admin/tests/driver/?vehiclemodel__id=1', url)

        label = label_for_field(custom_set_field, tercel, vehiclemodel_admin)
        self.assertEqual('Driver Title', label)

        # Validate add_fk_link, vehicle with no drivers
        driverless = VehicleModel.objects.create(name='Driverless', 
            vehiclemake=toyota)
        html = self.field_value(vehiclemodel_admin, driverless,
            custom_set_field)
        self.assertEqual('<i>no drivers</i>', html)
