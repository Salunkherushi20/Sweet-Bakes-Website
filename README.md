# Sweet Bakes Website

A responsive static bakery website for cake inspiration and custom cake enquiries.

## Pages
- `index.html` — Home
- `treats.html` — Cake categories and product inspiration
- `custom-cake.html` — Custom cake enquiry draft form
- `our-story.html` — About Sweet Bakes

Primary calls to action open dedicated pages rather than scrolling the homepage. Each page has its own SEO title and meta description. Relative links are used for GitHub Pages project hosting.

## Audit and repairs
- Added shared JavaScript for mobile navigation and automatic footer year.
- Added accessible expanded-state labels to the mobile menu.
- Removed duplicate meta descriptions from the Treats and Our Story pages.
- Added a custom cake enquiry form with required fields, URL cake preselection, message draft generation and copy support.
- The enquiry form is browser-only: it does not send or store personal information. Customers must manually copy and send the prepared draft.
- Checked page files for required HTML structure, titles, descriptions, navigation and form markup through GitHub Actions.

## Run locally
Open `index.html` in a browser. Keep the four HTML files in the same directory. External Unsplash photography needs an internet connection.

## Publish with GitHub Pages
Repository **Settings → Pages → Deploy from a branch → main → /(root) → Save**. The site URL is `https://salunkherushi20.github.io/Sweet-Bakes-Website/`.

## Before business launch
- Add only verified business contact details, actual pricing, and availability.
- Connect enquiries to a secure, tested delivery method before promising that messages are submitted.
- Product images load from Unsplash. Confirm the selected image licensing and replace images if required.
- Do not add passwords, private keys, or customer data to this public repository.
