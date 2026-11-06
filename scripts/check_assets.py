"""Check local HTML/CSS asset paths without third-party packages."""
from html.parser import HTMLParser
from pathlib import Path
import re
root = Path(__file__).resolve().parents[1]
missing = []
class CheckHTML(HTMLParser):
    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key in ('href', 'src') and value and not value.startswith(('http:', 'https:', 'mailto:', '#', 'data:')):
                if not (root / value).exists():
                    missing.append(value)
for page in root.glob('*.html'):
    parser = CheckHTML()
    parser.feed(page.read_text())
for css in root.rglob('*.css'):
    for value in re.findall(r'url\(["\x27]?([^\)"\x27]+)', css.read_text()):
        if not value.startswith(('data:', 'http:', 'https:')) and not (css.parent / value).exists():
            missing.append(str(css.relative_to(root)) + ': ' + value)
if missing:
    raise SystemExit('Missing assets: ' + ', '.join(missing))
print('PASS: local HTML, CSS, image and font paths resolve.')
