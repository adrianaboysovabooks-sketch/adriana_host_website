# Adriana — resume here

## GitHub handover preparation — 6 November 2026

Start with `website/HANDOVER.md` for account ownership, collaborator invitations, shared updates, preview and publishing instructions. `website/scripts/prepare_site.py` now creates a separate deployment folder for a supplied HTTPS root/project URL. It adds canonical and Open Graph URL/image metadata, defaults to noindex, and generates the six-page sitemap/robots policy only with `--indexable`. No source page indexing settings were changed and nothing was published. The supplied hero photograph is used for sharing; owner review remains pending.

Verified: all six pages' local assets/links/fragments, duplicate IDs, image alt attributes, language, headings, skip links and navigation labels. Three preparation regression tests cover root/project URLs, review/final indexing and source/output protection. This is a static structure review, not a new browser or complete accessibility audit. Existing browser evidence remains dated 23 October. External destinations require a live check before launch.

`adriana-website-handover-2026-11-06.zip` is the source package for her PC/GitHub, with hidden configuration files and without Python caches or surrounding private reference materials. She can own the repository and invite Mimi as a collaborator. Final hosting/account/domain choices and the owner content/asset decisions below are still pending.

## Authorized scope and current state

Faithful independent static rebuild, compatible with GitHub Pages. User authorized the other pages after the homepage on 23 October. Keep everything local until public launch is explicitly approved. No hosting registration, DNS changes, subscriptions or replacement of Wix have occurred. Use Firefox for browser checks (explicit user preference).

Source: `website/`. Main instructions: `Adriana_Website_Handoff.md`. References: `Site screenshots/`, `site_text.docx`, `Wormhole R83XKA/`. Read `website/README.md` for implementation/editing details.

Implemented: Domov, O mne (`o-mne.html`), Zachránené Vianoce (`zachranene-vianoce.html`), Zamatový jež (`zamatovy-jez.html`), Mimóza (`mimoza.html`), and Novinky (`novinky.html`). Homepage navigation and three book-detail links are local. The fourth book, Šťastné náhody, retains its accessible information dialog because no dedicated reference page/route was supplied. Original Slovak copy and verified DOCX article/publisher links are preserved. Book-club information and RSVP remain on the existing Wix service; no replacement registration form or fake submission has been added.

Homepage portrait now scrolls at 65% of the foreground text speed, clipped within the hero with its original crop. This follows the user's description of the desired layered effect. Small phones and reduced-motion users have a still parallax layout. Selected foreground text also has gentle once-only fade-up entrances (22 px desktop / 14 px phone). The pink name has a clearer 44 px / 1.4 s rise and the book cards a 34 px / 1.15 s rise with 110 ms stagger (32/26 px on phones), using explicit keyframes to reliably show the short upward movement. These effects are disabled for reduced motion, printing and unsupported observers. Keyboard focus reveals controls immediately.

Preview: http://127.0.0.1:8876/website/ while the parent-folder server runs. Start with `python3 -m http.server 8876 --bind 127.0.0.1 --directory /home/mimi/projects/Adriana`. This is local-only and unrelated to the hosted Voiceover Lab testing site.

## Editing and verification

Interior pages are static generated HTML. Edit `website/content/pages.json` for copy, `website/content/links.json` for verified external links, or `website/scripts/build_pages.py` for interior markup. Then run `python3 website/scripts/build_pages.py` from this folder. Shared header/footer come from `index.html`. All styling is in `website/assets/styles.css`. Original source images remain untouched; asset provenance is in `website/content/assets.json`.

Firefox verification: homepage plus each of the five interior pages at 360/390/768/1280/1440 px; local navigation/current markers; all supplied paragraph/review/reason text; images and transparent AVIFs; no horizontal overflow; mobile menus/Escape; homepage dialog content/focus return. Parallax checked at multiple scroll positions on desktop/tablet and still on phones/reduced-motion branch. Screenshots and JSON evidence are in `review/`. Reusable checks: `check_assets.py`, `check_firefox.py`, `check_pages.py`, `check_parallax.py`, and `check_entrances.py` under `website/scripts/`. Browser scripts use the isolated Firefox BiDi listener at port 9224 and installed Python websockets.

## Remaining decisions before launch

1. Owner review of all six local pages and the strengthened parallax. Mobile interior layouts are interpretations; no mobile references were supplied.
2. Confirm exact fonts (current Bodoni Moda/Libre Baskerville substitutes), social-profile URLs, the original book-club image. The reading portrait has been replaced with the supplied higher-resolution `DSC_9346 copy.avif` (794×989). The latter is still a documented screenshot crop.
3. Confirm desired book-club details/booking destination. Keep existing RSVP links until chosen; no event backend is authorized.
4. Supply the missing Mimóza SME article URL if it should be linked. The title is currently preserved as plain text.
5. Christmas illustration is a still from the supplied animation. No videos, intro or loading screen are used.
6. Before explicit launch: final metadata, indexing/robots, sitemap and canonical/OG URLs; final accessibility/link review; repository/host/domain ownership; HTTPS; redirects; preserve existing email DNS. Retain Wix until replacement approval.
