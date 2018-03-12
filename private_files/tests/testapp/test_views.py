import six
from django.test import TestCase, override_settings


class TestFileProtection(TestCase):

    @classmethod
    def setUpClass(cls):
        from .factories import UserFactory, DocumentFactory
        super(TestFileProtection, cls).setUpClass()
        cls.first_user = UserFactory.create(username='first', email='first@example.com')
        cls.second_user = UserFactory.create(username='second', email='second@example.com')
        cls.first_user_doc = DocumentFactory.create(owner = cls.first_user)
        cls.second_user_doc = DocumentFactory.create(owner=cls.second_user)

    def test_can_download_owned(self):
        """Test that a user can download their owned files"""
        self.client.login(username='first', password='thepassword')
        resp = self.client.get(self.first_user_doc.attachment.url)
        self.assertEqual(resp.status_code, 200)

    def test_cannot_download_unowned(self):
        """Test that a user can not download files not owned by them"""
        self.client.login(username='first', password='thepassword')
        resp = self.client.get(self.second_user_doc.attachment.url)
        self.assertEqual(resp.status_code, 403)

    @override_settings(PRIVATE_DOWNLOAD_HANDLER='private_files.handlers.x_accel_redirect')
    def test_x_accel_redirect_allowed_download_status(self):
        """Test that a user can download their owned files"""
        self.client.login(username='first', password='thepassword')
        resp = self.client.get(self.first_user_doc.attachment.url)
        self.assertEqual(resp.status_code, 200)

    @override_settings(PRIVATE_DOWNLOAD_HANDLER='private_files.handlers.x_accel_redirect')
    def test_x_accel_redirect_allowed_header(self):
        """Test that the X-Accel-Redirect header is set correctly"""
        self.client.login(username='first', password='thepassword')
        resp = self.client.get(self.first_user_doc.attachment.url)
        self.assertEqual(resp['X-Accel-Redirect'], "/%s" % six.text_type(self.first_user_doc.attachment))

    @override_settings(PRIVATE_DOWNLOAD_HANDLER='private_files.handlers.x_sendfile')
    def test_x_sendfile_allowed_download_status(self):
        """Test that a user can download their owned files"""
        self.client.login(username='first', password='thepassword')
        resp = self.client.get(self.first_user_doc.attachment.url)
        self.assertEqual(resp.status_code, 200)

    @override_settings(PRIVATE_DOWNLOAD_HANDLER='private_files.handlers.x_sendfile')
    def test_x_sendfile_allowed_header(self):
        """Test that the X-Sendfile header is set correctly"""
        self.client.login(username='first', password='thepassword')
        resp = self.client.get(self.first_user_doc.attachment.url)
        self.assertEqual(resp['X-Sendfile'], self.first_user_doc.attachment.path)