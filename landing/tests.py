from django.test import TestCase

class SEORoutingTestCase(TestCase):
    def test_robots_txt(self):
        response = self.client.get('/robots.txt')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/plain')
        self.assertIn('User-agent: *', response.content.decode())
        self.assertIn('Sitemap: ', response.content.decode())

    def test_sitemap_xml(self):
        response = self.client.get('/sitemap.xml')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/xml')
        self.assertIn('<urlset', response.content.decode())
        self.assertIn('<loc>', response.content.decode())

    def test_google_verification(self):
        response = self.client.get('/google91f4a71bffa82687.html')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/html')
        self.assertEqual(response.content.decode(), 'google-site-verification: google91f4a71bffa82687.html')


