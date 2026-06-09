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
        content = response.content.decode()
        self.assertIn('<urlset', content)
        self.assertIn('<loc>', content)
        self.assertIn('/features/arabic-voiceover/', content)
        self.assertIn('/features/virtual-try-on/', content)
        self.assertIn('/features/image-resizer/', content)

    def test_google_verification(self):
        response = self.client.get('/google91f4a71bffa82687.html')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/html')
        self.assertEqual(response.content.decode(), 'google-site-verification: google91f4a71bffa82687.html')

    def test_feature_pages(self):
        for path in ['/features/arabic-voiceover/', '/features/virtual-try-on/', '/features/image-resizer/']:
            response = self.client.get(path)
            self.assertEqual(response.status_code, 200)


