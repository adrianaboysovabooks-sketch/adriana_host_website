# Adriana's website: ownership and updates

The complete editable website is this folder. No Node/npm setup is needed.
The six pages are ready for local review. Launch decisions are listed below.

## Put it in Adriana's GitHub

1. Adriana signs into her own GitHub account and GitHub Desktop on her PC.
2. In GitHub Desktop choose File → New repository. Name it `adriana-website` and create it.
3. Copy everything from this folder into that new repository folder, with `index.html`, `assets/` and `content/` directly at its root. Include `.nojekyll` and `.gitignore`. Do not copy the surrounding references or review screenshots.
4. Commit with summary `Add Adriana's website`, then Publish repository. Keep it private during handover and leave Pages disabled until a public preview is approved.

## Give Mimi access

Adriana owns the repository; Mimi uses her own GitHub account.

1. Ask Mimi for her GitHub username.
2. Adriana opens the website repository on github.com.
3. Open Settings → Collaborators (under Access) → Add people.
4. Search for Mimi's username, select the correct account, then click Add NAME to REPOSITORY.
5. Mimi accepts the invitation from GitHub/email. She can then clone the repository and push updates. If GitHub displays a role selector, choose Write for routine code updates.

This grants access to the website repository, not Adriana's whole account. No shared password is needed. Personal repositories can have collaborators even when private on GitHub Free.

Official instructions: https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/repository-access-and-collaboration/inviting-collaborators-to-a-personal-repository

## Updating together

Each person clones the same repository in GitHub Desktop using their own account. Before editing, Fetch origin and Pull any updates. Edit, preview, commit with a short description, then Push origin. Tell the other person when editing the same page to reduce conflicts. For changes Adriana should review first, use a branch and pull request.

Use the shared repository as the main copy after handover. Connect Mimi's local working copy to that repository rather than continuing with a separate untracked copy.

## Local preview

From the repository folder, with Python 3 installed:

```sh
python3 -m http.server 8876 --bind 127.0.0.1
```

On Windows, use `py -m http.server 8876 --bind 127.0.0.1` if `python3` is unavailable. Open http://127.0.0.1:8876/ in Firefox. Keep the terminal open; Ctrl+C stops the preview. HTTP is required for the fourth book's information dialog.

See README.md for the content files and page-generation instructions. Editing existing HTML/CSS needs no packages; regenerating the interior pages requires Pillow.

## Prepare metadata for the chosen address

The source pages keep their review-only noindex policy. Once the real preview address is known, run the following from the repository folder, replacing the example account and path:

```sh
python3 scripts/prepare_site.py --base-url https://ACCOUNT.github.io/adriana-website/ --output ../adriana-preview
```

This creates a separate hosting folder with page-specific canonical/OG URLs and a sharing image using the supplied hero photo. It remains excluded from indexing. No files are uploaded. Noindex/robots are search-engine requests, not access controls: anyone with a public preview URL can view it.

For an approved final launch at the existing domain:

```sh
python3 scripts/prepare_site.py --base-url https://adrianaboysova.eu/ --output ../adriana-launch --indexable
```

Use the actual agreed domain, including `www` if selected. This enables indexing and adds a six-page sitemap and its robots.txt reference. The script refuses to overwrite existing output. Use a new output folder each time. Python 3's standard library is sufficient; Windows users can substitute `py`.

Publish the generated folder's contents, including `.nojekyll`, as the hosting root. Keep the editable source in GitHub. For a simple source-only review, direct root publication also works, but final metadata needs the preparation step. If using generated output, regenerate and publish it after source changes; source pushes alone do not update a separately published folder. We can configure that automation once the repository/host are chosen.

GitHub Pages can publish a branch's root or `/docs` folder, or use Actions. GitHub Free requires a public repository for Pages; paid plans also support private source repositories. A private source repository does not make a Pages site private by default.

Official setup: https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site

## Checks and remaining launch decisions

Local checks:

```sh
python3 scripts/check_assets.py
python3 scripts/check_structure.py
python3 -m unittest discover -s scripts -p test_prepare_site.py
```

Automated structure checks cover local links/fragments, duplicate IDs, image alternatives, page headings, navigation labels and skip links. They do not establish full accessibility compliance or verify external websites.

Adriana still needs to review the six pages, confirm fonts and biography/event details, supply social profile URLs and the original book-club photo, and choose the booking destination. The missing Mimóza SME article URL can be added when supplied. The favicon remains a provisional A. Review the supplied hero as the sharing image.

Once public launch is approved: confirm account/repository and final URL, prepare final output, check the actual hosted pages and external destinations, configure HTTPS and apex/www handling, plan old Wix URL redirects where supported, and only then change DNS. Preserve existing email MX/TXT records and retain Wix until the replacement is approved. No DNS or live hosting has been changed by this handover preparation.
