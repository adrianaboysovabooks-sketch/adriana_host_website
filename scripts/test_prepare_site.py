"""Verify hosting URLs, indexing policy and source isolation."""
import tempfile
import unittest
from pathlib import Path
from xml.etree import ElementTree as ET
from prepare_site import ROOT, prepare


class PrepareSiteTests(unittest.TestCase):
    def test_root_and_project_launch(self):
        before = {p.name: p.read_bytes() for p in ROOT.glob('*.html')}
        for base in ['https://adrianaboysova.eu/', 'https://example.github.io/adriana-website/']:
            with self.subTest(base=base), tempfile.TemporaryDirectory() as tmp:
                output = prepare(base, Path(tmp) / 'public', indexable=True)
                locations = [node.text for node in ET.parse(output / 'sitemap.xml').findall('.//{*}loc')]
                self.assertEqual(len(locations), 6)
                self.assertIn(base, locations)
                for page in output.glob('*.html'):
                    url = base if page.name == 'index.html' else base + page.name
                    source = page.read_text()
                    self.assertIn(f'rel="canonical" href="{url}"', source)
                    self.assertIn(f'property="og:url" content="{url}"', source)
                    self.assertIn(base + 'assets/images/hero.webp', source)
                    self.assertNotIn('noindex', source)
                    self.assertEqual(source.count('rel="canonical"'), 1)
                self.assertIn('Sitemap: ' + base + 'sitemap.xml', (output / 'robots.txt').read_text())
                self.assertTrue((output / 'content/stastne-nahody.json').exists())
                self.assertTrue((output / '.nojekyll').exists())
                self.assertFalse((output / 'content/source-text.txt').exists())
                self.assertFalse((output / 'scripts').exists())
        self.assertEqual(before, {p.name: p.read_bytes() for p in ROOT.glob('*.html')})

    def test_review_stays_excluded(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = prepare('https://example.github.io/review', Path(tmp) / 'public')
            self.assertIn('noindex, nofollow', (output / 'index.html').read_text())
            self.assertIn('Disallow: /', (output / 'robots.txt').read_text())
            self.assertFalse((output / 'sitemap.xml').exists())
            with self.assertRaises(ValueError):
                prepare('https://example.org', output)

    def test_invalid_target_and_source_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            for url in ['http://example.org', 'https://example.org/?x=1', 'https://u:p@example.org', 'https://example.org/../bad']:
                with self.subTest(url=url), self.assertRaises(ValueError):
                    prepare(url, Path(tmp) / 'public')
        with self.assertRaises(ValueError):
            prepare('https://example.org', ROOT / 'public')


if __name__ == '__main__':
    unittest.main()
