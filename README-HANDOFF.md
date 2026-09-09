# RSC Buses (Ronan Byrne Bus Hire) — squaretwo build

Static site, no framework, no build dependencies beyond Python 3.
Deploys to Vercel as a plain static site (`vercel.json` sets `trailingSlash`).

## How it is built

All pages are generated from **`site-src/build.py`**. Edit content there, then:

```
python site-src/build.py
```

That rewrites `index.html`, `services/`, `golf-trips/`, `areas/`, `about/`,
`faqs/`, `contact/`, `404.html`, `sitemap.xml` and `robots.txt`.
**Do not hand-edit the generated .html files** — a rebuild wipes them.

Assets (`assets/style.css`, `assets/site.js`, `assets/favicon.svg`) are NOT
generated. Edit those directly.

## Outstanding items

1. **Team photo.** Sorica will send a photo of herself and Ronan once the
   uniforms arrive. Slot is on the About page (the one remaining `ph(...)`
   placeholder in `build.py`). Drop the file in `assets/img/` and swap the
   `ph(...)` for `photo(...)`.
2. **Seat counts.** The fleet section (home page, `FLEET` in `build.py`)
   lists vehicle types with no capacities. Ask Sorica for seat counts per
   vehicle and add them to each card.
3. **Reviews.** None supplied. No testimonial section on the build yet.
4. **Golf trips.** Sorica said they are "just getting everything in order"
   with golf work but that bookings are becoming more frequent. The golf
   page presents it as live. Confirm with her that is fine.

## Phone

`087 181 7897` (supplied by Sorica, 9 Sep 2026). Set once as `PHONE` /
`PHONE_E164` in `build.py`; it drives the top bar, the first item in the
mobile menu, the CTA band, the contact card, the footer and the schema
`telephone`. The nav button stays a quote link to `/contact/` so the two
paths are distinct.

## Assets

Client originals (6 phone photos, all portrait, plus `New logo.pdf`) live in
`assets/raw/` and are **gitignored** (25 MB). Processed web versions are in
`assets/img/`:

- `hero-fleet.jpg` (1600w) — home hero, midi-coach + Setra coach
- 4:3 crops at 1200w for every other slot (see `SERVICE_PHOTOS` and `FLEET`
  in `build.py` for which goes where)
- `logo.png` / `logo-white.png` — the full square client logo
- `logo-bus.png` / `logo-bus-white.png` — the coach mark alone, used in the
  header and footer lockup alongside a Libre Baskerville wordmark (the
  square logo is too tall for a 74px header)
- `favicon.png`, `og.jpg`

The fleet visible in the photos: Setra full-size coach (09-TS-1), TURAS
midi-coach (161-CE-1342), two Ford Transit minibuses (182-WX-1447 navy,
161-WX-3461 silver), Mercedes Sprinter (141-D-23073) and a Debon enclosed
luggage trailer. Every vehicle is liveried "Ronan Byrne" in script; the new
logo is "RSC Buses". The About page acknowledges both.

Brand navy from the logo is `#0f2532` (`--navy-deep` in style.css).

## Client brief (source: Sorica Byrne, office@rscbuses.ie, 3 Sep 2026)

- Family-run, based in Aughrim, Co. Wicklow, 10+ years trading.
- Founded by Ronan Byrne, run today by Ronan and his wife Sorica.
- 7 drivers total including Ronan. Sorica does the office work.
- **No booking system** — deliberate. Email enquiry only.
- Covers all of Leinster, further travel subject to availability.
- Golf trips are a growth area and expected to become the main line of business.
- All drivers fully Garda vetted, documentation current, buses checked regularly.
- Services: schools, airport transfers, concerts, sporting events, weddings,
  stag and hen parties, local runs, private group travel, golf trips.

## Enquiry form

`assets/site.js` composes a `mailto:` to `office@rscbuses.ie` from the form
fields. No backend, nothing to host. If a real endpoint is wanted later,
POST to it from the same submit handler.

`/contact/?service=<slug>` pre-selects the service dropdown — the service
cards across the site link in that way.

## SEO

- Per-page title, description, canonical, OG tags.
- `LocalBusiness` JSON-LD on every page (name, area served, address, email).
- `FAQPage` JSON-LD on the home page and `/faqs/`.
- `sitemap.xml` + `robots.txt` generated with the build.
- Add `telephone` to schema by filling in `PHONE_E164`.
