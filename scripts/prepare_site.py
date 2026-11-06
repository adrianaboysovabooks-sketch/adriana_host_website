"""Prepare a portable hosting folder; never upload or alter source pages.

Python standard library only. Defaults to a review site excluded from indexing.
"""
import argparse
import html
import re
import shutil
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


def prepare(base_url, output, indexable=False):
    parsed = urlsplit(base_url)
    if (parsed.scheme != 'https' or not parsed.hostname or parsed.username
            or parsed.password or parsed.query or parsed.fragment
            or any(c.isspace() for c in base_url)
            or any(p in ('.', '..') for p in parsed.path.split('/'))):
        raise ValueError('Use a full HTTPS site URL without credentials, query or fragment.')
    base = urlunsplit((parsed.scheme, parsed.netloc, parsed.path.rstrip('/') + '/', '', ''))
    output = Path(output).resolve()
    if output == ROOT or ROOT in output.parents or output in ROOT.parents:
        raise ValueError('Output must be outside the source website folder.')
    if output.exists():
        raise ValueError('Output already exists. Choose a new folder to preserve previous copies.')
    output.mkdir(parents=True)
    shutil.copytree(ROOT / 'assets', output / 'assets')
    (output / 'content').mkdir()
    shutil.copy2(ROOT / 'content/stastne-nahody.json', output / 'content/stastne-nahody.json')
    (output / '.nojekyll').touch()
    urls = []
    for page in sorted(ROOT.glob('*.html')):
        url = base if page.name == 'index.html' else base + page.name
        urls.append(url)
        source = page.read_text(encoding='utf-8')
        source = re.sub(r'\s*<meta name="robots"[^>]*>', '', source)
        source = re.sub(r'\s*<link rel="canonical"[^>]*>', '', source)
        source = re.sub(r'\s*<meta property="og:(?:url|image|image:alt|site_name)"[^>]*>', '', source)
        escape = lambda value: html.escape(value, quote=True)
        metadata = [
            f'<meta name="robots" content="{"index, follow" if indexable else "noindex, nofollow"}">',
            f'<link rel="canonical" href="{escape(url)}">',
            f'<meta property="og:url" content="{escape(url)}">',
            '<meta property="og:site_name" content="Adriana Boysová">',
            f'<meta property="og:image" content="{escape(base + "assets/images/hero.webp")}">',
            '<meta property="og:image:alt" content="Adriana Boysová v kaviarni">',
        ]
        source = source.replace('</head>', '  ' + '\n  '.join(metadata) + '\n</head>')
        (output / page.name).write_text(source, encoding='utf-8')
    robots = 'User-agent: *\n' + ('Allow: /\n' if indexable else 'Disallow: /\n')
    if indexable:
        namespace = 'http://www.sitemaps.org/schemas/sitemap/0.9'
        ET.register_namespace('', namespace)
        sitemap = ET.Element(f'{{{namespace}}}urlset')
        for url in urls:
            ET.SubElement(ET.SubElement(sitemap, f'{{{namespace}}}url'), f'{{{namespace}}}loc').text = url
        ET.ElementTree(sitemap).write(output / 'sitemap.xml', encoding='utf-8', xml_declaration=True)
        robots += f'Sitemap: {base}sitemap.xml\n'
    (output / 'robots.txt').write_text(robots, encoding='utf-8')
    return output


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base-url', required=True, help='Actual root or GitHub project URL, including repository path.')
    parser.add_argument('--output', required=True, help='New output directory outside website/.')
    parser.add_argument('--indexable', action='store_true', help='Enable search indexing and generate sitemap for an approved launch.')
    args = parser.parse_args()
    try:
        result = prepare(args.base_url, args.output, args.indexable)
    except ValueError as error:
        parser.error(str(error))
    print(f'Prepared {result}; indexing {"enabled" if args.indexable else "disabled"}. Nothing uploaded.')
