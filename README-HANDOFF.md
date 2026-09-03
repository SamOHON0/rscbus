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

## Outstanding items before this goes to the client

1. **Phone number is missing.** Sorica's email never gave one. Set `PHONE` and
   `PHONE_E164` at the top of `build.py` and every phone CTA (top bar, nav
   button, contact card, schema `telephone`) switches on automatically. Until
   then the site routes everything to `office@rscbuses.ie`.
2. **Photos.** Every image is a dashed placeholder box (`.ph` in style.css).
   Sorica sent `Bus pictures.zip` on 3 Sep — drop the extracted images into
   `assets/img/` and replace each `ph(...)` call in `build.py` with a real
   `<img>`. Placeholders are labelled with what shot belongs there.
3. **Logo.** Sorica sent `New logo.pdf` on 3 Sep. Current header/footer mark is
   a temporary SVG wordmark defined as `LOGO` in `build.py`. Swap it for the
   real mark and re-check the `--navy` / `--amber` tokens in style.css against
   the client's actual colours — the whole palette flows from those tokens.
4. **Driver/uniform photo.** Sorica said she will send a photo of herself and
   Ronan once the uniforms arrive. That slot is on the About page.
5. **Reviews/testimonials.** None supplied. There is no testimonial section on
   the build yet — worth asking for 3 or 4 before launch.

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
