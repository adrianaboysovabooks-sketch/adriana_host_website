# Adriana Boysová — local website preview

For GitHub ownership, collaborator access, updating together and preparing launch metadata, start with [HANDOVER.md](HANDOVER.md).

Faithful static rebuild with a home page and five interior pages: O mne, Zachránené Vianoce, Zamatový jež, Mimóza and Novinky. No website registration, public hosting, DNS changes, subscriptions or replacement of Wix has taken place.

## Preview

From this directory:

```sh
python3 -m http.server 8876 --bind 127.0.0.1
```

Open http://127.0.0.1:8876/ in Firefox. The current review server serves the parent `Adriana` directory, so its URL is http://127.0.0.1:8876/website/ instead. Both root and project-subdirectory hosting are supported by relative local asset paths. No installation or build is required.

The preview is local to this computer. It is not the externally accessible voiceover Site. Closing the server stops the preview. Do not double-click the HTML file for the final review: the book-information dialog fetches a local JSON document and needs HTTP.

## Files to edit

- `index.html`: home-page text, navigation, book cards, author introduction, meetings and contact.
- `o-mne.html`, `zachranene-vianoce.html`, `zamatovy-jez.html`, `mimoza.html`, `novinky.html`: generated static interior pages.
- `content/pages.json`: supplied Slovak copy for the interior pages; `content/links.json`: exact external destinations extracted from the supplied DOCX.
- `scripts/build_pages.py`: regenerate interior pages after editing their content or templates. It reuses the homepage header/footer, updates local navigation and uses Pillow only during development. The deployed website needs no Python, installation or build.
- `assets/styles.css`: layout, responsive breakpoints, colours, typography and reduced-motion treatment.
- `assets/site.js`: mobile menu, layered hero parallax, gentle one-time scroll entrances, current footer year and book-information dialog.
- `assets/images/`: optimised copies only; original assets remain untouched in the supplied materials folder.
- `assets/fonts/`: self-hosted Bodoni Moda and Libre Baskerville, with their OFL licences. These are provisional substitutes; exact reference font names are unverified.
- `content/source-text.txt`: text extracted from `site_text.docx` for the later pages, including original wording and diacritics.
- `content/stastne-nahody.json`: supplied collection description shown by the fourth book card.
- `content/assets.json`: image provenance, including the temporary book-club crop.

To add a book later, duplicate a `.book-card` article, supply an optimised cover, update the title/description, and point the button at the actual detail page. Local images and page links should stay relative for GitHub Pages project paths.

## Intentional preview differences and unresolved items

- No Wix promotional banner or Wix application dependencies.
- Navigation and the first three book-detail links open the rebuilt local pages. The fourth book card opens the supplied description in an accessible native dialog because its reference destination has not been verified.
- RSVP leads to the existing Wix news/event list; a specific booking destination or replacement registration service remains unverified. The Novinky page recreates the existing book-club listing; its information and RSVP links remain on that original service. No form or fake confirmation has been added.
- Facebook and Instagram profile URLs are missing from the brief and DOCX. Their icons are omitted until real destinations are supplied.
- On phones the hero title and introduction appear below the portrait for readable text and a clear photo. No mobile screenshots were supplied; the responsive layout is a documented interpretation.
- The hero portrait moves at 65% of the foreground text’s scrolling speed once the hero reaches the viewport top, creating the requested background/foreground parallax. The photo keeps its original crop and stays clipped within the hero. This follows the owner’s description; the Wix animation has not been independently measured. Motion is disabled for reduced-motion preferences and on small phones.
- The homepage reading portrait now uses the owner’s replacement `DSC_9346 copy.avif` (794×989), served without recompression. Its original portrait layout/crop is retained.
- The book-club photograph is temporarily cropped from the supplied reference screenshot. Replace it with the original.
- Favicon is a provisional typographic “A”, not a new logo; replace with the approved favicon if one exists.
- The Christmas illustration uses a still frame from the supplied book-animation file; it does not autoplay or download a video. Body text uses the supplied Slovak copy. Confirm the existing biography and book-club information before launch rather than silently rewriting them.

## Verification

Firefox 158: inspected full-page desktop and phone screenshots; checked widths 360, 390, 768, 1280 and 1440 px. No document overflow or broken image loads. Local fonts loaded. Mobile menu open/close and Escape, collection dialog content, close and focus return passed. Assets were served under `/website/` to exercise a project-subdirectory deployment path.

Review evidence is in `../review/`. A static asset checker is available with `python3 scripts/check_assets.py`. Firefox screenshot/interaction automation can be repeated using `scripts/check_firefox.py` with a locally started Firefox BiDi listener on port 9224; the check requires the Python `websockets` package already available in this environment. Automation is a development aid only, not a runtime dependency.

This is not yet a full-site or production accessibility sign-off. Remaining pages, complete keyboard/browser review, exact font comparison, social links, event behaviour, final metadata and hosting checks remain in `../NEXT_SESSION.md`.

## Future publishing

The complete source folder is also the static deployment output. Initial target is GitHub Pages; no host has been configured. Use repository root publication or a workflow that uploads this folder. Keep `.nojekyll` when deploying directly. Confirm the owning account/repository and selected host with the owner first.

Before public launch: remove preview `noindex` and replace robots policy, set final canonical/OG URLs and image, create the sitemap for completed local pages, configure the approved domain, and test the actual root/subpath deployment. Only change DNS after explicit launch authorization. Preserve email MX/TXT records, verify HTTPS and apex/www handling, and check redirects from the old page URLs where supported. Retain Wix until the replacement is approved.


## Interior-page verification — 23 October 2026

Firefox checked all five interior pages at 360, 390, 768, 1280 and 1440 px. Checks cover local navigation and book-card destinations, current-page markers, all supplied paragraphs/reviews/reasons, source image loading, transparent decorative AVIF images, mobile menu/Escape, scrolling without JavaScript errors and horizontal overflow. Desktop and phone screenshots and structured results are in `../review/`. Repeat with `python3 scripts/check_pages.py` against the local preview and Firefox BiDi listener. Use `python3 scripts/check_parallax.py` for the homepage's separate foreground/background speeds and visible image coverage.

The Mimóza SME article title is preserved as plain text because the supplied DOCX has no URL for it. Other article/publisher links use the exact destinations supplied in the DOCX. The Christmas page uses the supplied still illustration, book photograph and launch photograph; source files are recorded in `content/assets.json`. Transparent originals remain AVIF to preserve their alpha channels. Neither supplied video is loaded by the website.


## Entrance effects and reading portrait — 23 October 2026

The author name and selected headings/text fade upward gently as they enter view. The pink homepage name rises 44 px over 1.4 seconds (32 px on phones); the book cards rise 34 px over 1.15 seconds (26 px on phones) with a short 110 ms stagger. These featured entrances use explicit animation keyframes so they reliably start below their resting positions. Other text travels 22 px on larger screens and 14 px on phones, fading over about 0.85–1 second. Reveals play once per page visit, so scrolling back does not repeatedly hide text. The hero background's parallax is independent of these foreground entrances.

Reduced-motion preferences and print show everything without entrance animation. If JavaScript or IntersectionObserver is unavailable, normal readable content remains visible. Keyboard focus immediately reveals any pending linked panel. No intro overlay, loading sequence or auto-playing video is added.

`DSC_9346 copy.avif` is copied to `assets/images/author-reading-dsc9346.avif`. The supplied original remains untouched; provenance and dimensions are in `content/assets.json`. Motion targets and timings are in `assets/site.js` and `assets/styles.css`. Repeat the Firefox motion/portrait checks with `python3 scripts/check_entrances.py`; evidence is in `../review/entrance-checks.json` and `*-entrances-*.png`.
