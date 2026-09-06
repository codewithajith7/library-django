from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from app.models import Book

class BookCRUDTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.dummy_image = SimpleUploadedFile(
            name='test_cover.jpg',
            content=b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b',
            content_type='image/jpeg'
        )
        self.book1 = Book.objects.create(
            title="Clean Code",
            author="Robert C. Martin",
            genre="Technology",
            isbn="978-0132350884",
            price=39.99,
            cover=self.dummy_image
        )

    def test_dashboard_welcome_view(self):
        response = self.client.get(reverse('welcome'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Clean Code")
        self.assertContains(response, "Total Catalog Books")

    def test_admin_dashboard_view(self):
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Admin Control Center")
        self.assertContains(response, "Genre Distribution")
        self.assertEqual(response.context['total_books'], 1)


    def test_create_book(self):
        new_image = SimpleUploadedFile(
            name='new_cover.jpg',
            content=b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b',
            content_type='image/jpeg'
        )
        response = self.client.post(reverse('add_book'), {
            'title': 'The Pragmatic Programmer',
            'author': 'Andrew Hunt',
            'genre': 'Technology',
            'isbn': '978-0201616224',
            'price': '44.95',
            'cover': new_image
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Book.objects.filter(title="The Pragmatic Programmer").exists())

    def test_read_book_list_and_search(self):
        response = self.client.get(reverse('get_all_books'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Clean Code")

        # Test search query
        response_search = self.client.get(reverse('get_all_books') + '?q=Martin')
        self.assertContains(response_search, "Clean Code")

        response_nomatch = self.client.get(reverse('get_all_books') + '?q=NonExistentTitle')
        self.assertContains(response_nomatch, "No books matched your criteria")

    def test_read_book_detail(self):
        response = self.client.get(reverse('book_detail', args=[self.book1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Clean Code")
        self.assertContains(response, "Robert C. Martin")

    def test_update_book(self):
        updated_image = SimpleUploadedFile(
            name='updated_cover.jpg',
            content=b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b',
            content_type='image/jpeg'
        )
        response = self.client.post(reverse('edit_book', args=[self.book1.id]), {
            'title': 'Clean Code (Updated Edition)',
            'author': 'Robert C. Martin',
            'genre': 'Software Engineering',
            'isbn': '978-0132350884',
            'price': '49.99',
            'cover': updated_image
        })
        self.assertEqual(response.status_code, 302)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Clean Code (Updated Edition)')
        self.assertEqual(self.book1.genre, 'Software Engineering')


    def test_delete_book(self):
        response = self.client.post(reverse('delete_book', args=[self.book1.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Book.objects.filter(id=self.book1.id).exists())
