# Reference inventory — 21 October 2026

Authority: `Adriana_Website_Handoff.md`, supplied screenshots and `site_text.docx`. This is a faithful static rebuild, not a redesign. User additionally requested subtle scrolling on the home page. As of 23 October, local implementation includes the home page plus all five verified navigation pages. No public hosting or DNS changes.

## Pages and sections

| Page | Evidence | Preview status |
| --- | --- | --- |
| Domov | Screenshots 16.20.36–16.21.08; DOCX HOME | Implemented: portrait hero → four books → author introduction → meetings → contact → footer |
| O mne | Screenshots 16.21.19–16.21.33; DOCX O MNE | Implemented locally as `o-mne.html` |
| Zachránené Vianoce | Supplied screenshot sequence 16.21.39 onward; DOCX | Implemented locally as `zachranene-vianoce.html` |
| Zamatový jež | Supplied screenshots, notably 16.22.15–16.22.20; DOCX | Implemented locally as `zamatovy-jez.html` |
| Mimóza | Screenshots 16.22.29–16.22.39; DOCX | Implemented locally as `mimoza.html` |
| Novinky / Knižný klub | Screenshots 16.22.54 and home meeting card | Listing rebuilt locally as `novinky.html`; information/RSVP remain on the existing Wix service |
| Šťastné náhody | Fourth home card; supplied collection description | No dedicated reference route verified; home card temporarily opens supplied text |

Page identifiers and routes above also appear in the fetched Wix runtime pages map. Wix also lists event detail/registration and schedule routes. Their content/interaction has not been verified and is not presumed to be a request for a booking backend.

## Asset map

| Supplied original | Role |
| --- | --- |
| DSC_9482 copy.jpg | Home portrait in pink blouse |
| zj-1000-1000-transparent.png | Zamatový jež cover/card |
| IMG_8188.jpeg | Zachránené Vianoce cover/card |
| mimóza.png | Mimóza cover/card |
| IMG_8184 (1).jpeg | Šťastné náhody cover/card |
| DSC_9346 copy.avif | Home author reading portrait, updated 23 October (794×989); replaces the earlier low-resolution image.jpeg |
| foto kniznica.jpg | O mne library portrait |
| T3XX0036.jpg | O písaní / Mimóza bookshop photograph |
| 481019783_612167181786648_6561240449470810076_n.jpg | Zamatový jež detail photograph |
| AdrianaBoysová-23.jpg | Book event/group photograph |
| AdrianaBoysová-34.jpg | Zachránené Vianoce event/books photograph |
| knihy.avif | Prepared for the O mne books section |
| Yellow Mimosa Branch.avif | Decorative mimosa branch |
| Screenshot 2025-12-09 173811.avif | Illustrated sleeping child, likely Christmas book page |
| Two Pixlr MP4 files | Not loaded by the site; the Christmas book page uses a still frame extracted from its supplied illustration clip |
| site_text.docx embedded images | Reference book grid and older English layout snippets; approved Slovak text takes precedence |

The original open-book photograph used for Knižný klub has not been found. A temporary image-only reference crop is documented in `website/content/assets.json`. Original assets have not been edited.

## Design and interaction observations

Cream canvas, pale blush book section, pink meetings band, muted terracotta/rose accents, dark serif body type, high-contrast display serif headings, thin book-card borders. Wide photographic hero with fuchsia author name and light introduction. Navigation order follows supplied screenshot. Exact fonts, exact viewport scaling and live animation parameters remain unverified; the CSS documents responsive interpretation.

No supplied mobile reference, approved social profile URLs or confirmed RSVP endpoint. External article/publisher hyperlinks were extracted from DOCX. A complete final link map still needs to be assembled for the detail pages.
