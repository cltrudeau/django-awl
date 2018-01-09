# awl.tests.test_admintools.py
from django.contrib.admin.utils import label_for_field
from django.test import TestCase
from django.utils.safestring import SafeData

from screwdriver import parse_link

from awl.waelsteng import AdminToolsMixin
from awl.tests.models import Author, Book, Chapter
from awl.tests.admin import BookAdmin, ChapterAdmin

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
