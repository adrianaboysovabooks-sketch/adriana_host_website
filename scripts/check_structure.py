"""Check static navigation and basic accessibility structure, without dependencies."""
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


class Document(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.path = path
        self.tags = []
        self.feed(path.read_text(encoding='utf-8'))

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))


documents = {p.resolve(): Document(p) for p in ROOT.glob('*.html')}
errors = []
for path, doc in documents.items():
    def require(condition, message):
        if not condition:
            errors.append(f'{path.name}: {message}')
    ids = Counter(attrs['id'] for _, attrs in doc.tags if 'id' in attrs)
    require(all(count == 1 for count in ids.values()), 'duplicate ID')
    require(sum(tag == 'h1' for tag, _ in doc.tags) == 1, 'expected one h1')
    require(sum(tag == 'main' for tag, _ in doc.tags) == 1, 'expected one main landmark')
    require(any(tag == 'html' and attrs.get('lang') == 'sk' for tag, attrs in doc.tags), 'missing Slovak document language')
    require(any(tag == 'a' and attrs.get('href') == '#main' for tag, attrs in doc.tags), 'missing skip link')
    for tag, attrs in doc.tags:
        if tag == 'img':
            require('alt' in attrs, 'image has no alt attribute')
        if tag == 'nav':
            require(bool(attrs.get('aria-label') or attrs.get('aria-labelledby')), 'navigation has no accessible label')
        for key in ('href', 'src'):
            value = attrs.get(key)
            if not value:
                continue
            url = urlsplit(value)
            if url.scheme or url.netloc:
                continue
            target = (path.parent / unquote(url.path)).resolve() if url.path else path
            if target.is_dir():
                target /= 'index.html'
            require(target.exists(), f'missing destination {value}')
            if url.fragment and target in documents:
                target_ids = {a.get('id') for _, a in documents[target].tags}
                require(unquote(url.fragment) in target_ids, f'missing fragment {value}')
        if attrs.get('aria-controls'):
            require(all(identifier in ids for identifier in attrs['aria-controls'].split()), 'aria-controls target missing')
if errors:
    raise SystemExit('\n'.join(errors))
print(f'PASS: {len(documents)} pages; local links/fragments, IDs, language, headings, landmarks, alt attributes and navigation labels.')
