# Adriana Boysová — website rebuild handoff

Prepared 21 October 2026. Give this file and the supplied materials to the coding agent.

## Goal and overriding design direction

Rebuild Adriana’s existing author portfolio as an independent, responsive static website. She wants it to look as close as possible to the website she already designed. This is a faithful rebuild, not a redesign. Preserve its personality, layout, colours, typography, images, page order and content wherever technically feasible. Fix broken behaviour and responsive layout problems without introducing a different aesthetic.

Do not replace the reference with a generic portfolio template, new branding, invented copy, stock photography or AI-generated imagery. If an exact font or asset is unavailable, identify it and propose the closest practical substitute explicitly.

## Reference and evidence

- Existing domain: https://adrianaboysova.eu
- Indexed Wix reference: https://adrianaboysova.wixsite.com/adriana-boysov
- The domain and direct Wix page could not be fully inspected in the preceding conversation. The exact page inventory, visual design and interactive features have NOT been verified. Do not assume they have.
- User-supplied screenshots, originals and current instructions are essential. Inspect the live site if accessible; use screenshots when it is not. Report any gaps rather than pretending to have inspected missing pages.
- Priority: explicit owner instructions > supplied approved screenshots and content > accessible live site > clearly labelled temporary assumptions. If references conflict materially, ask which version to match.

## Materials folder for the user

Create a folder named `Adriana-Website`. Add this handoff at its root. Suggested subfolders (organisation is helpful, not mandatory):

| Folder/file | What to include |
| --- | --- |
| `01-reference/` | Full-page screenshots of every existing page on desktop; mobile screenshots if available. Include open menus, gallery/lightbox views and footer. A short screen recording can show hover effects or transitions. |
| `02-images/` | Original portraits, book covers, gallery photos, backgrounds, logo/signature and icons. Keep useful filenames; note where each belongs if unclear. |
| `03-text/` | Existing page text copied into documents or text files, including accents, book descriptions, captions and any language versions. No need to retype text the agent can reliably extract. |
| `04-fonts/` | Font names and any font files she is permitted to use on the web, if known. Optional. |
| `05-links/links.txt` | Navigation destinations, social profiles, public contact address, external book/review links, downloads and any existing form destinations. |
| `NOTES.txt` | Pages to keep, any deliberate changes, known bugs, image placement notes and whether a contact form/newsletter is actually wanted. |

Screenshots should show the whole page rather than only its first screen. Name them by page and device, for example `home-desktop.png` and `about-mobile.png`. If mobile is currently broken, label that reference as broken: reproduce the intended appearance, not the bug.

Zip the folder and upload it to a chat-based coding environment, or open the unzipped folder as the project workspace in a local coding environment. Do not put account passwords, API keys or private subscriber lists into the materials or public repository.

## Confirmed scope and deferred choices

- Small author portfolio; the owner says there is no selling on the site.
- Preserve the existing site's content and structure after inventorying the actual references. Do not infer a sitemap from this brief.
- Make it work on desktop, tablet and mobile, including navigation and links.
- No intro video, loading animation or Enter screen in version 1. These can be added later without delaying the main website. Do not display an empty intro placeholder.
- GitHub Pages is the initial hosting target discussed. Netlify is an alternative, not a confirmed switch. Keep the implementation portable between static hosts.
- Newsletter and contact-form services were explored but have not been selected or requested as confirmed additions. Preserve existing features if present, inventory their dependencies, and flag anything requiring a provider. Do not add a non-functional signup form.
- No CMS or visual editor is required unless the owner requests one. Make routine content changes straightforward and document them.

## Implementation guidance

Prefer the smallest maintainable static implementation suitable for the references: HTML/CSS with minimal JavaScript, or a static generator if justified. Avoid an application backend or a heavy framework without a concrete need. Deliver a complete editable source project and deployable static output, not a Wix iframe, redirect wrapper or screenshot of the original site.

Use supplied original assets, produce optimised web copies and retain originals separately. Preserve important image crops and focal points. Keep Slovak diacritics and the correct document language. Do not silently rewrite or translate copy.

Use semantic HTML, keyboard-operable navigation, visible focus states, descriptive image alternatives and reduced-motion support for any existing animation. Match the design closely while correcting serious usability issues; document visible departures.

Ensure internal links and asset paths work for both a GitHub project preview path and a custom-domain root. Avoid routes that require server rewrites. Include page titles, descriptions, favicon, social-sharing metadata, sitemap and robots settings appropriate to the final domain. Do not promise search ranking. Review canonical URLs before launch.

If email/signup functionality is requested, use an approved external service and its supported embed or endpoint. Never expose private credentials in browser code. Include appropriate consent and unsubscribe behaviour through the chosen provider. Do not send mail or enrol contacts during testing.

## Working sequence

1. Read this handoff and inspect all supplied materials. Inventory pages, sections, assets, typography, colours, navigation, interactions and external dependencies. Note missing information concisely.
2. Inspect the live reference when possible. Establish screenshot references at known viewport sizes. Ask only for missing information that materially blocks a faithful build; progress with verified material meanwhile.
3. Implement the homepage faithfully first, then the remaining verified pages using shared styling. Keep any temporary assumptions clearly documented.
4. Run and inspect the actual rendered site. Compare reference and implementation side by side at matching desktop dimensions, then check mobile layouts. Fix mismatched typography, spacing, widths, cropping and hierarchy before polishing incidental effects.
5. Deliver a working reviewable preview, complete source and a concise list of deviations or missing assets. The owner should be able to review the result before the existing domain changes.
6. Provide publishing instructions for the selected host. Do not modify DNS, replace the live website, create subscriptions or publish publicly without the user's authorization for that step.

## Completion checklist

- All verified reference pages and sections are included; no invented content or placeholder text is presented as final.
- Desktop appearance closely follows the approved reference; departures are explained.
- Mobile layout works at approximately 360–390 px, tablet at 768 px, and desktop at 1280–1440 px, with no horizontal overflow or clipped content.
- Navigation, menus, images, downloads and internal/external links work. Contact/signup features either work with the approved service or are explicitly listed as pending.
- Test the actual deployed-path configuration, not just the development server. Check broken assets, console errors, keyboard navigation and image loading.
- Images are suitably compressed and sized; below-the-fold media can load lazily. No unnecessary intro or large video download in version 1.
- Include a README with local preview/build commands, deployment steps and how to edit text, replace images and add a book entry where applicable.
- Include a short launch checklist: account/repository ownership, selected host, domain verification and DNS records to change, preserving existing email records, HTTPS, apex/www behaviour, and post-launch checks. Determine exact provider settings at launch rather than assuming them now.

## Suggested starting instruction to the coding agent

“Read Adriana_Website_Handoff.md and inspect the attached materials. Rebuild Adriana’s existing website as faithfully as possible; do not redesign it. Start by inventorying the references and identifying genuine gaps, then implement a working static preview. Leave the video/Enter intro for later. Keep the project compatible with GitHub Pages and do not change the live domain.”
