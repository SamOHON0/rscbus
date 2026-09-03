#!/usr/bin/env python3
"""RSC Buses static site builder.

Run:  python site-src/build.py
Writes the HTML pages, sitemap.xml and robots.txt into the project root.

Edit content HERE, not in the generated .html files - a rebuild overwrites them.
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------- site config
SITE = "RSC Buses"
LEGAL = "Ronan Byrne Bus Hire"
DOMAIN = "https://rscbuses.ie"
EMAIL = "office@rscbuses.ie"
# TODO: no phone number was supplied in the client brief. Fill it in here and
# every phone CTA across the site switches on automatically.
PHONE = ""            # e.g. "087 123 4567"
PHONE_E164 = ""       # e.g. "+353871234567"
TOWN = "Aughrim"
COUNTY = "Co. Wicklow"
YEARS = "10"
DRIVERS = "7"

AREAS = ["Wicklow", "Dublin", "Kildare", "Carlow", "Wexford", "Kilkenny",
         "Laois", "Offaly", "Meath", "Louth", "Westmeath", "Longford"]
TOWNS = ["Aughrim", "Arklow", "Wicklow Town", "Bray", "Greystones", "Rathdrum",
         "Baltinglass", "Blessington", "Gorey", "Carlow Town", "Naas",
         "Dublin City", "Dublin Airport"]

SERVICES = [
    ("school-transport", "School transport",
     "Reliable daily school runs and school outings across Wicklow and the wider Leinster area.",
     "bus"),
    ("airport-transfers", "Airport transfers",
     "Early starts and late landings covered. Group transfers to and from Dublin Airport and the ferry ports.",
     "plane"),
    ("golf-trips", "Golf trips",
     "Clubs, societies and away days driven door to door, with room for the bags and the banter.",
     "flag"),
    ("weddings", "Weddings",
     "Guest shuttles between the church, the venue and the hotel so nobody has to worry about lifts home.",
     "rings"),
    ("sporting-events", "Sporting events",
     "Club and school teams, supporters and away trips, on time for throw-in or kick-off.",
     "ball"),
    ("concerts-and-nights-out", "Concerts and nights out",
     "Groups to gigs, festivals and events, with a driver waiting to bring everyone home safely.",
     "music"),
    ("stag-and-hen-parties", "Stag and hen parties",
     "Full-day and weekend group travel, planned around your itinerary.",
     "party"),
    ("private-group-travel", "Private group travel",
     "Corporate days out, family occasions, club outings and local runs of every size.",
     "users"),
]

ICONS = {
"bus": '<path d="M4 16V6a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v10"/><path d="M4 11h16"/><circle cx="8" cy="18" r="2"/><circle cx="16" cy="18" r="2"/>',
"plane": '<path d="M17.8 19.2 16 11l3.5-3.5a2.1 2.1 0 0 0-3-3L13 8 4.8 6.2a1 1 0 0 0-1 1.6L8 11l-2 3H3l2 3 3 2 1-3 3-2 3.2 4.2a1 1 0 0 0 1.6-1z"/>',
"flag": '<path d="M4 22V4"/><path d="M4 5h11l-1.5 3L15 11H4z"/>',
"rings": '<circle cx="9" cy="15" r="5"/><circle cx="15" cy="9" r="5"/>',
"ball": '<circle cx="12" cy="12" r="9"/><path d="M12 3v6l5 3-2 6M12 9 7 12l2 6"/>',
"music": '<path d="M9 18V6l10-2v12"/><circle cx="6" cy="18" r="3"/><circle cx="16" cy="16" r="3"/>',
"party": '<path d="M3 21l5-13 8 8-13 5z"/><path d="M14 4v3M18 8h3M17.5 3.5 19 2M19 11l2 1"/>',
"users": '<path d="M16 20v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="3.5"/><path d="M22 20v-2a4 4 0 0 0-3-3.9"/><path d="M16 3.6a4 4 0 0 1 0 7"/>',
"shield": '<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="m9 12 2 2 4-4"/>',
"clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.5 2"/>',
"map": '<path d="M12 21s7-6.2 7-11a7 7 0 1 0-14 0c0 4.8 7 11 7 11z"/><circle cx="12" cy="10" r="2.6"/>',
"heart": '<path d="M12 20s-7-4.4-7-9.4A4.1 4.1 0 0 1 12 8a4.1 4.1 0 0 1 7 2.6C19 15.6 12 20 12 20z"/>',
"phone": '<path d="M5 3h4l2 5-2.5 1.5a12 12 0 0 0 6 6L16 13l5 2v4a2 2 0 0 1-2.2 2A17 17 0 0 1 3 5.2 2 2 0 0 1 5 3z"/>',
"mail": '<rect x="3" y="5" width="18" height="14" rx="2.5"/><path d="m3.5 7 8.5 6 8.5-6"/>',
}

def icon(name, cls=""):
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" '
            'stroke-linecap="round" stroke-linejoin="round" class="%s" aria-hidden="true">%s</svg>'
            % (cls, ICONS[name]))

LOGO = '''<svg viewBox="0 0 250 60" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="RSC Buses">
  <rect x="2" y="12" width="52" height="30" rx="8" fill="%(bus)s"/>
  <rect x="8" y="18" width="16" height="11" rx="3" fill="%(win)s"/>
  <rect x="28" y="18" width="19" height="11" rx="3" fill="%(win)s"/>
  <circle cx="15" cy="45" r="6" fill="%(wheel)s"/><circle cx="41" cy="45" r="6" fill="%(wheel)s"/>
  <text x="66" y="31" font-family="Manrope,Inter,sans-serif" font-weight="800" font-size="25" fill="%(t1)s" letter-spacing="-0.5">RSC</text>
  <text x="120" y="31" font-family="Manrope,Inter,sans-serif" font-weight="800" font-size="25" fill="%(t2)s" letter-spacing="-0.5">Buses</text>
  <text x="66" y="47" font-family="Inter,sans-serif" font-weight="600" font-size="10.5" fill="%(t3)s" letter-spacing="1.1">RONAN BYRNE BUS HIRE</text>
</svg>'''

LOGO_LIGHT = LOGO % {"bus": "#14314f", "win": "#e3ecf5", "wheel": "#0c2038",
                     "t1": "#14314f", "t2": "#c07c05", "t3": "#7c8a99"}
LOGO_DARK = LOGO % {"bus": "#f5a524", "win": "#0c2038", "wheel": "#e3ecf5",
                    "t1": "#ffffff", "t2": "#f5a524", "t3": "#9db6cd"}

NAV = [("/", "Home"), ("/services/", "Services"), ("/golf-trips/", "Golf trips"),
       ("/areas/", "Areas covered"), ("/about/", "About"), ("/faqs/", "FAQs"),
       ("/contact/", "Contact")]

# ------------------------------------------------------------------ shell
def phone_link(label=None, cls="btn btn-amber"):
    """Phone CTAs only render once PHONE is filled in above."""
    if not PHONE:
        return ('<a class="%s" href="/contact/">%s</a>'
                % (cls, label or "Get a quote"))
    return ('<a class="%s" href="tel:%s">%s</a>'
            % (cls, PHONE_E164 or PHONE.replace(" ", ""), label or ("Call " + PHONE)))

def topbar():
    right = ('<div><a href="tel:%s">Call %s</a></div>' % (PHONE_E164 or PHONE.replace(" ", ""), PHONE)
             if PHONE else '<div><a href="mailto:%s">%s</a></div>' % (EMAIL, EMAIL))
    return ('<div class="topbar"><div class="wrap">'
            '<div>Family-run coach and bus hire, %s, %s &middot; Covering all of Leinster</div>'
            '%s</div></div>' % (TOWN, COUNTY, right))

def header(path):
    links = "".join('<a href="%s"%s>%s</a>' % (h, ' class="on"' if h == path else "", t)
                    for h, t in NAV)
    mob = "".join('<a href="%s">%s</a>' % (h, t) for h, t in NAV)
    return """%s
<header class="nav">
  <div class="wrap">
    <a href="/" class="brand" aria-label="%s home">%s</a>
    <nav class="navlinks">%s</nav>
    <div class="nav-cta">%s</div>
    <button class="burger" aria-label="Menu" aria-expanded="false"><span></span><span></span><span></span></button>
  </div>
</header>
<div class="mobile-menu">%s</div>""" % (topbar(), SITE, LOGO_LIGHT, links,
                                        phone_link("Get a quote", "btn btn-navy"), mob)

def cta(title="Need a bus for your group?",
        text="Tell us the date, the numbers and where you are going. We will come back to you with a price, usually the same day."):
    return """<section class="cta">
  <div class="wrap">
    <h2>%s</h2>
    <p>%s</p>
    <div class="cta-actions">
      <a class="btn btn-amber" href="/contact/">Get a quote</a>
      <a class="btn btn-ghost" href="mailto:%s">Email %s</a>
    </div>
  </div>
</section>""" % (title, text, EMAIL, EMAIL)

def footer():
    svc = "".join('<li><a href="/services/#%s">%s</a></li>' % (s[0], s[1]) for s in SERVICES[:6])
    nav = "".join('<li><a href="%s">%s</a></li>' % (h, t) for h, t in NAV[1:])
    contact = '<li><a href="mailto:%s">%s</a></li>' % (EMAIL, EMAIL)
    if PHONE:
        contact = '<li><a href="tel:%s">%s</a></li>' % (PHONE_E164 or PHONE.replace(" ", ""), PHONE) + contact
    return """<footer class="site">
  <div class="wrap">
    <div class="cols">
      <div class="fbrand">
        <div class="brand">%s</div>
        <p>%s, trading as %s. Family-run bus and coach hire based in %s, %s, serving groups across Leinster for over %s years.</p>
      </div>
      <div><h4>Services</h4><ul>%s</ul></div>
      <div><h4>Site</h4><ul>%s</ul></div>
      <div><h4>Contact</h4><ul>%s<li>%s, %s</li></ul></div>
    </div>
    <div class="legal">
      <div>&copy; <span data-year></span> %s. All rights reserved.</div>
      <div>Website by <a href="https://squaretwo.ie" rel="noopener">SquareTwo</a></div>
    </div>
  </div>
</footer>""" % (LOGO_DARK, SITE, LEGAL, TOWN, COUNTY, YEARS, svc, nav, contact, TOWN, COUNTY, SITE)

BASE_LD = """{
  "@context":"https://schema.org","@type":"MotorVehicleDealership","@id":"%(d)s/#business",
  "name":"%(site)s","alternateName":"%(legal)s","url":"%(d)s/",
  "email":"%(email)s","priceRange":"$$",
  "description":"Family-run bus and coach hire based in %(town)s, %(county)s. School transport, airport transfers, golf trips, weddings, sporting events and private group travel across Leinster.",
  "address":{"@type":"PostalAddress","addressLocality":"%(town)s","addressRegion":"%(county)s","addressCountry":"IE"},
  "areaServed":[%(areas)s]
}"""

def base_ld():
    ld = BASE_LD % {"d": DOMAIN, "site": SITE, "legal": LEGAL, "email": EMAIL,
                    "town": TOWN, "county": COUNTY,
                    "areas": ",".join('"%s"' % a for a in AREAS)}
    if PHONE_E164:
        ld = ld.replace('"email"', '"telephone":"%s","email"' % PHONE_E164)
    # MotorVehicleDealership is wrong for hire; use the transport type instead.
    return ld.replace("MotorVehicleDealership", "LocalBusiness")

def page(path, title, desc, body, extra_ld="", nav_path=None):
    url = DOMAIN + ("/" if path == "index.html" else "/" + path.rsplit("/", 1)[0] + "/")
    html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>%(title)s</title>
<meta name="description" content="%(desc)s">
<meta name="robots" content="index, follow">
<link rel="canonical" href="%(url)s">
<meta property="og:title" content="%(title)s">
<meta property="og:description" content="%(desc)s">
<meta property="og:url" content="%(url)s">
<meta property="og:type" content="website">
<meta property="og:locale" content="en_IE">
<link rel="icon" type="image/svg+xml" href="/assets/favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/style.css">
<script type="application/ld+json">%(ld)s</script>
%(extra)s</head>
<body>
%(header)s
%(body)s
%(footer)s
<script src="/assets/site.js"></script>
</body>
</html>
""" % {"title": title, "desc": desc, "url": url, "ld": base_ld(),
       "extra": extra_ld, "header": header(nav_path or ("/" if path == "index.html"
                                                        else "/" + path.rsplit("/", 1)[0] + "/")),
       "body": body, "footer": footer()}
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote", path)

# ------------------------------------------------------------------ pieces
HERO_ART = """<svg class="hero-art" viewBox="0 0 760 340" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <defs>
    <linearGradient id="body" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#ffffff" stop-opacity=".97"/>
      <stop offset="1" stop-color="#cfe0ef" stop-opacity=".95"/>
    </linearGradient>
    <linearGradient id="glass" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#7fb6e2"/><stop offset="1" stop-color="#2b7bbd"/>
    </linearGradient>
  </defs>
  <ellipse cx="380" cy="300" rx="330" ry="20" fill="#0a1b30" opacity=".45"/>
  <path d="M92 96h500a52 52 0 0 1 52 52v106a14 14 0 0 1-14 14H78a14 14 0 0 1-14-14V138a42 42 0 0 1 28-42z" fill="url(#body)"/>
  <path d="M600 112a44 44 0 0 1 40 44v22h-58v-66z" fill="url(#glass)" opacity=".95"/>
  <g fill="url(#glass)">
    <rect x="96" y="126" width="74" height="52" rx="9"/>
    <rect x="182" y="126" width="74" height="52" rx="9"/>
    <rect x="268" y="126" width="74" height="52" rx="9"/>
    <rect x="354" y="126" width="74" height="52" rx="9"/>
    <rect x="440" y="126" width="74" height="52" rx="9"/>
  </g>
  <rect x="64" y="196" width="580" height="16" fill="#f5a524"/>
  <rect x="64" y="216" width="580" height="7" fill="#14314f" opacity=".35"/>
  <rect x="524" y="126" width="52" height="88" rx="9" fill="#cfe0ef" opacity=".9"/>
  <circle cx="184" cy="268" r="42" fill="#0a1b30"/><circle cx="184" cy="268" r="19" fill="#cfe0ef"/>
  <circle cx="512" cy="268" r="42" fill="#0a1b30"/><circle cx="512" cy="268" r="19" fill="#cfe0ef"/>
  <rect x="636" y="188" width="16" height="20" rx="6" fill="#f5a524"/>
</svg>"""

def trustband():
    items = [("shield", "Fully Garda vetted drivers"),
             ("clock", "Punctual, %s years on the road" % YEARS),
             ("map", "All of Leinster covered"),
             ("heart", "Family-run, not a call centre")]
    return ('<div class="trustband"><div class="wrap">%s</div></div>'
            % "".join("<span>%s%s</span>" % (icon(i), t) for i, t in items))

def service_cards(limit=None, link_prefix="/services/#"):
    out = []
    for slug, name, blurb, ic in (SERVICES[:limit] if limit else SERVICES):
        out.append("""<a class="card" href="%s%s">
      <div class="ico">%s</div>
      <h3>%s</h3><p>%s</p><span class="more">Read more</span>
    </a>""" % (link_prefix, slug, icon(ic), name, blurb))
    return '<div class="grid g4">%s</div>' % "".join(out)

FAQS = [
 ("What areas do you cover?",
  "We are based in %s, %s and cover all of Leinster as standard, including Dublin, Kildare, Carlow, Wexford, Kilkenny and the midlands. We travel further afield too when we have availability on your dates, so it is always worth asking." % (TOWN, COUNTY)),
 ("How do I book?",
  "There is no online booking system, and that is deliberate. Every job is quoted properly rather than by a form. Email %s or use the enquiry form with your date, group size, pick-up point and destination, and we will confirm availability and price, usually the same day." % EMAIL),
 ("What size groups can you take?",
  "We run a fleet with %s drivers, so we can look after everything from a small private group to a full coach load, and multiple vehicles for larger events. Tell us your numbers and we will match the right vehicle." % DRIVERS),
 ("Are your drivers vetted?",
  "Yes. Every driver is fully Garda vetted, which matters most for our school work but applies right across the business. All licences and documentation are kept up to date."),
 ("Are the buses maintained and insured?",
  "Yes. Our vehicles are serviced and checked regularly, and all required documentation is current. We are happy to provide details to schools, clubs and companies who need them for their own records."),
 ("Do you do school transport?",
  "We do. Daily school runs, school tours and one-off outings are a core part of what we do, with vetted drivers and a fleet that is checked regularly."),
 ("Can you do early morning airport runs?",
  "Yes. Early departures and late arrivals into Dublin Airport are routine for us. Give us the flight time and we will build the pick-up around it."),
 ("Do you run golf trips?",
  "Yes, and it is a growing part of the business. We look after societies, clubs and groups travelling to courses around the country, with space for clubs and bags and a driver for the day."),
 ("How far in advance should I book?",
  "The sooner the better for weekends, bank holidays and big event dates, which go early. Midweek work can often be arranged at shorter notice. Ask us either way."),
 ("Do you carry stag and hen parties?",
  "We do, provided the group is respectful of the vehicle and the driver. Tell us the plan and the numbers and we will quote it."),
]

def faq_block(items):
    return ('<div class="faq">%s</div>'
            % "".join('<details%s><summary>%s</summary><div class="a">%s</div></details>'
                      % (" open" if i == 0 else "", q, a) for i, (q, a) in enumerate(items)))

def faq_ld(items):
    q = ",".join('{"@type":"Question","name":"%s","acceptedAnswer":{"@type":"Answer","text":"%s"}}'
                 % (a.replace('"', "&quot;"), b.replace('"', "&quot;")) for a, b in items)
    return ('<script type="application/ld+json">{"@context":"https://schema.org",'
            '"@type":"FAQPage","mainEntity":[%s]}</script>\n' % q)

def ph(label, cls="ph"):
    return '<div class="%s"><span>%s</span></div>' % (cls, label)

# ------------------------------------------------------------------ pages
def build_home():
    body = """<section class="hero">
  %(art)s
  <div class="wrap"><div class="hero-inner"><div class="hero-copy">
    <h1>Bus and coach hire in <em>Wicklow</em>, across all of Leinster</h1>
    <p>%(legal)s is a family-run transport business based in %(town)s, %(county)s. School runs, airport transfers, golf trips, weddings and group travel, driven by people you can actually get hold of.</p>
    <div class="hero-actions">
      <a class="btn btn-amber" href="/contact/">Get a quote</a>
      <a class="btn btn-ghost" href="/services/">See our services</a>
    </div>
  </div></div></div>
</section>
%(trust)s

<section class="sec">
  <div class="wrap">
    <div class="sec-head center">
      <div class="eyebrow">What we do</div>
      <h2>Group travel, sorted properly</h2>
      <p class="lede" style="margin:10px auto 0">From the daily school run to a full weekend away, we carry groups of every size across Leinster and beyond.</p>
    </div>
    %(services)s
  </div>
</section>

<section class="sec tint">
  <div class="wrap split">
    <div>
      <div class="eyebrow">Why %(site)s</div>
      <h2>A local operator, not a booking platform</h2>
      <p class="lede" style="margin-top:12px">Ronan Byrne set the business up after years driving for other local transport companies, and it is still run day to day by Ronan and his wife Sorica. When you ring or email, you are talking to the people who own the buses.</p>
      <ul>
        <li>Over %(years)s years serving Wicklow and the surrounding counties</li>
        <li>%(drivers)s drivers, all fully Garda vetted</li>
        <li>Vehicles checked regularly with all documentation up to date</li>
        <li>Every job quoted individually, no rigid online booking system</li>
        <li>Repeat customers who come back year after year</li>
      </ul>
      <div style="margin-top:26px"><a class="btn btn-navy" href="/about/">More about us</a></div>
    </div>
    <div>%(photo)s</div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="stats">
      <div class="stat"><b>%(years)s+</b><span>Years on the road</span></div>
      <div class="stat"><b>%(drivers)s</b><span>Vetted drivers</span></div>
      <div class="stat"><b>12</b><span>Leinster counties covered</span></div>
      <div class="stat"><b>100%%</b><span>Family run</span></div>
    </div>
  </div>
</section>

<section class="sec tint">
  <div class="wrap split">
    <div>%(photo2)s</div>
    <div>
      <div class="eyebrow">Growing fast</div>
      <h2>Golf trips and society away days</h2>
      <p class="lede" style="margin-top:12px">Golf work is becoming a bigger part of what we do. We take societies, clubs and groups to courses around the country, with room for the clubs and a driver on hand for the day so nobody has to think about who is driving home.</p>
      <div style="margin-top:24px"><a class="btn btn-amber" href="/golf-trips/">Plan a golf trip</a></div>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="sec-head center">
      <div class="eyebrow">Areas covered</div>
      <h2>Based in %(town)s, covering all of Leinster</h2>
      <p class="lede" style="margin:10px auto 0">We travel further afield too, subject to availability on your dates. If you are outside the list, ask anyway.</p>
    </div>
    <div class="pills" style="justify-content:center">%(pills)s</div>
    <div style="text-align:center;margin-top:28px"><a class="btn btn-line" href="/areas/">See areas covered</a></div>
  </div>
</section>

<section class="sec tint">
  <div class="wrap">
    <div class="sec-head center"><div class="eyebrow">Questions</div><h2>Common questions</h2></div>
    %(faq)s
    <div style="text-align:center;margin-top:26px"><a class="btn btn-line" href="/faqs/">All FAQs</a></div>
  </div>
</section>

%(cta)s""" % {
    "art": HERO_ART, "trust": trustband(), "services": service_cards(8),
    "site": SITE, "legal": LEGAL, "town": TOWN, "county": COUNTY,
    "years": YEARS, "drivers": DRIVERS,
    "photo": ph("Photo: the fleet"), "photo2": ph("Photo: golf group boarding"),
    "pills": "".join("<span>%s</span>" % a for a in AREAS),
    "faq": faq_block(FAQS[:5]), "cta": cta()}
    page("index.html",
         "Bus &amp; Coach Hire Wicklow | School, Airport &amp; Golf Trips | %s" % SITE,
         "Family-run bus and coach hire in %s, %s. School transport, Dublin Airport transfers, golf trips, weddings and private group travel across Leinster. Garda vetted drivers. Get a quote." % (TOWN, COUNTY),
         body, extra_ld=faq_ld(FAQS[:5]))

SERVICE_DETAIL = {
"school-transport": ["Daily school runs on contract or on an agreed schedule",
  "School tours, matches, swimming and activity days",
  "Garda vetted drivers and up to date documentation available on request",
  "Consistent drivers so the school and the children know who is collecting them"],
"airport-transfers": ["Dublin Airport as standard, plus Rosslare and Dublin ferry ports",
  "Early morning departures and late night pick-ups",
  "Pick-up built around your flight time, not a fixed timetable",
  "Room for luggage for the full group"],
"golf-trips": ["Society outings, club trips and corporate golf days",
  "Courses anywhere in Ireland, single day or overnight",
  "Space for clubs, bags and trolleys",
  "Driver on hand for the day so nobody is watching the clock"],
"weddings": ["Guest shuttles between church, venue and hotel",
  "Multiple runs across the evening so nobody is stranded",
  "Timings agreed in advance with you or your planner",
  "Extra vehicles for larger guest lists"],
"sporting-events": ["Club and school teams to matches and away fixtures",
  "Supporters' buses to county and national games",
  "Early starts and long days are no problem",
  "Regular contract work for clubs across the season"],
"concerts-and-nights-out": ["Groups to gigs, festivals and shows",
  "Pick-up and return on the same night",
  "A driver waiting so everyone gets home safely",
  "Popular for work nights out and birthday groups"],
"stag-and-hen-parties": ["Full day and weekend itineraries",
  "Multiple stops built into the plan",
  "Airport and ferry connections for groups travelling on",
  "Quoted per group once we know the plan"],
"private-group-travel": ["Corporate days out and staff transport",
  "Family occasions, anniversaries and funerals",
  "Club outings, active retirement groups and community trips",
  "Local runs of any size"],
}

def build_services():
    blocks = []
    for i, (slug, name, blurb, ic) in enumerate(SERVICES):
        pts = "".join("<li>%s</li>" % p for p in SERVICE_DETAIL[slug])
        photo = ph("Photo: %s" % name.lower())
        left = """<div>
        <div class="eyebrow">Service</div>
        <h2>%s</h2>
        <p class="lede" style="margin-top:12px">%s</p>
        <ul>%s</ul>
        <div style="margin-top:24px"><a class="btn btn-navy" href="/contact/?service=%s">Enquire about %s</a></div>
      </div>""" % (name, blurb, pts, slug, name.lower())
        cols = (left + "<div>%s</div>" % photo) if i % 2 == 0 else ("<div>%s</div>" % photo + left)
        blocks.append('<section class="sec%s" id="%s"><div class="wrap split">%s</div></section>'
                      % (" tint" if i % 2 else "", slug, cols))
    body = """<section class="phead"><div class="wrap">
    <div class="crumb"><a href="/">Home</a> / Services</div>
    <h1>Our services</h1>
    <p>Whatever the group and whatever the occasion, we will get everyone there together and on time. Based in %s, covering all of Leinster.</p>
  </div></section>%s
%s""" % (TOWN, trustband(), "".join(blocks)) + cta()
    page("services/index.html",
         "Bus Hire Services | School, Airport, Golf, Weddings | %s" % SITE,
         "School transport, Dublin Airport transfers, golf trips, weddings, sporting events, concerts, stag and hen parties and private group travel from %s, %s." % (TOWN, COUNTY),
         body)

def build_golf():
    body = """<section class="phead"><div class="wrap">
    <div class="crumb"><a href="/">Home</a> / Golf trips</div>
    <h1>Golf trips and society outings</h1>
    <p>Clubs, societies and corporate groups driven door to door, anywhere in Ireland. Room for the clubs, a driver for the day and nobody drawing the short straw.</p>
  </div></section>%(trust)s

<section class="sec"><div class="wrap split">
  <div>
    <div class="eyebrow">Why travel together</div>
    <h2>The day starts when you get on the bus</h2>
    <p class="lede" style="margin-top:12px">Golf work is one of the fastest growing parts of our business, and it is easy to see why. One pick-up point, everyone arrives together, the bags travel with you, and there is no argument about who is staying off the pints.</p>
    <ul>
      <li>Society outings, club away days and corporate golf</li>
      <li>Courses anywhere in Ireland, single day or overnight</li>
      <li>Luggage and club space built in</li>
      <li>Driver available across the day for course, hotel and dinner runs</li>
      <li>Pick-ups from one point or several along the route</li>
    </ul>
  </div>
  <div>%(p1)s</div>
</div></section>

<section class="sec tint"><div class="wrap">
  <div class="sec-head center"><div class="eyebrow">How it works</div><h2>Three steps and it is booked</h2></div>
  <div class="grid g3">
    <div class="card"><div class="ico">%(i1)s</div><h3>1. Tell us the plan</h3><p>Date, course, group size and where everyone is coming from. A rough plan is enough to start.</p></div>
    <div class="card"><div class="ico">%(i2)s</div><h3>2. We price it</h3><p>We check availability and come back with a price, usually the same day. No deposit taken until you are happy.</p></div>
    <div class="card"><div class="ico">%(i3)s</div><h3>3. We do the driving</h3><p>We confirm timings the week before and collect on the day. You just show up with the clubs.</p></div>
  </div>
</div></section>

<section class="sec"><div class="wrap split">
  <div>%(p2)s</div>
  <div>
    <div class="eyebrow">Where we go</div>
    <h2>Wicklow courses and the rest of the country</h2>
    <p class="lede" style="margin-top:12px">We are on the doorstep of some of the best golf in the country, and we are just as happy taking a group the length of Ireland for a weekend. Tell us the course and we will work out the timings.</p>
    <div class="pills">%(pills)s</div>
  </div>
</div></section>
%(cta)s""" % {"trust": trustband(), "p1": ph("Photo: group at the course"),
              "p2": ph("Photo: coach with clubs loading"),
              "i1": icon("flag"), "i2": icon("mail"), "i3": icon("bus"),
              "pills": "".join("<span>%s</span>" % a for a in AREAS),
              "cta": cta("Planning a society outing?",
                         "Send us the date and the numbers and we will price it for you, usually the same day.")}
    page("golf-trips/index.html",
         "Golf Trip Bus Hire Ireland | Society &amp; Club Outings | %s" % SITE,
         "Bus and coach hire for golf societies, clubs and corporate golf days. Courses anywhere in Ireland, club and luggage space, driver for the day. Based in %s, %s." % (TOWN, COUNTY),
         body)

def build_about():
    body = """<section class="phead"><div class="wrap">
    <div class="crumb"><a href="/">Home</a> / About</div>
    <h1>About %(site)s</h1>
    <p>%(legal)s is a family-run transport business based in %(town)s, %(county)s, serving local communities and customers across the surrounding areas for over %(years)s years.</p>
  </div></section>%(trust)s

<section class="sec"><div class="wrap split">
  <div class="prose">
    <div class="eyebrow">Our story</div>
    <h2 style="margin-top:0">Built on the road, not in an office</h2>
    <p>The business was founded by Ronan Byrne after years of experience driving for local transport companies. It was built on a passion for reliable service, customer care and community connections.</p>
    <p>With extensive knowledge of the local area and a commitment to providing safe and dependable transport, Ronan decided to establish his own company to offer a more personal and professional service.</p>
    <p>Today the business is proudly run by Ronan alongside his wife Sorica, making it a true family operation dedicated to delivering friendly, trustworthy and flexible transport solutions.</p>
  </div>
  <div>%(p1)s</div>
</div></section>

<section class="sec tint"><div class="wrap">
  <div class="sec-head center"><div class="eyebrow">What you can count on</div><h2>The bits that actually matter</h2></div>
  <div class="grid g3">
    <div class="card"><div class="ico">%(i1)s</div><h3>Garda vetted drivers</h3><p>All %(drivers)s of our drivers, Ronan included, are fully Garda vetted with documentation kept up to date.</p></div>
    <div class="card"><div class="ico">%(i2)s</div><h3>Well kept vehicles</h3><p>Our buses are checked and serviced regularly. Paperwork is available for schools, clubs and companies who need it.</p></div>
    <div class="card"><div class="ico">%(i3)s</div><h3>Punctuality</h3><p>A strong reputation for punctuality, comfort and customer service, with many customers returning time and time again.</p></div>
  </div>
</div></section>

<section class="sec"><div class="wrap split">
  <div>%(p2)s</div>
  <div>
    <div class="eyebrow">The team</div>
    <h2>Seven drivers, one family business</h2>
    <p class="lede" style="margin-top:12px">Ronan drives and runs the operation. Sorica looks after the office, the quotes and the bookings, so when you email you get a straight answer from someone who knows what is on the road that week.</p>
    <p class="lede" style="margin-top:14px">Whether it is a local journey or a special occasion, we are committed to getting passengers to their destination safely, comfortably and on time.</p>
    <div style="margin-top:24px"><a class="btn btn-navy" href="/contact/">Talk to us</a></div>
  </div>
</div></section>
%(cta)s""" % {"site": SITE, "legal": LEGAL, "town": TOWN, "county": COUNTY, "years": YEARS,
              "drivers": DRIVERS, "trust": trustband(),
              "p1": ph("Photo: Ronan with the bus"), "p2": ph("Photo: Ronan and Sorica"),
              "i1": icon("shield"), "i2": icon("bus"), "i3": icon("clock"),
              "cta": cta()}
    page("about/index.html",
         "About Us | Family-Run Bus Hire in %s, %s | %s" % (TOWN, COUNTY, SITE),
         "%s is a family-run transport business in %s, %s, on the road for over %s years. Run by Ronan and Sorica Byrne with %s Garda vetted drivers." % (LEGAL, TOWN, COUNTY, YEARS, DRIVERS),
         body)

def build_areas():
    cards = "".join("""<div class="card"><div class="ico">%s</div><h3>%s</h3>
      <p>Group travel, school transport, airport runs and private hire throughout %s and the surrounding area.</p></div>"""
      % (icon("map"), a, a) for a in AREAS)
    body = """<section class="phead"><div class="wrap">
    <div class="crumb"><a href="/">Home</a> / Areas covered</div>
    <h1>Areas we cover</h1>
    <p>We are based in %(town)s, %(county)s and cover all of Leinster as standard, with travel further afield when we have availability on your dates.</p>
  </div></section>%(trust)s

<section class="sec"><div class="wrap">
  <div class="sec-head"><div class="eyebrow">Counties</div><h2>All of Leinster, and further on request</h2>
  <p class="lede">If your pick-up or destination is not listed, ask anyway. We regularly travel outside the province for golf trips, weddings and multi-day group travel.</p></div>
  <div class="grid g4">%(cards)s</div>
</div></section>

<section class="sec tint"><div class="wrap">
  <div class="sec-head center"><div class="eyebrow">Towns and pick-up points</div><h2>Regular routes and collection points</h2></div>
  <div class="pills" style="justify-content:center">%(towns)s</div>
  <div class="note" style="max-width:720px;margin:30px auto 0">Multiple pick-up points along a route are no problem and are common on golf trips, matches and wedding shuttles. Tell us where everyone is coming from and we will build the run around it.</div>
</div></section>
%(cta)s""" % {"town": TOWN, "county": COUNTY, "trust": trustband(), "cards": cards,
              "towns": "".join("<span>%s</span>" % t for t in TOWNS), "cta": cta()}
    page("areas/index.html",
         "Areas Covered | Bus Hire Across Leinster | %s" % SITE,
         "Bus and coach hire from %s, %s covering Wicklow, Dublin, Kildare, Carlow, Wexford, Kilkenny and the rest of Leinster, with longer trips on request." % (TOWN, COUNTY),
         body)

def build_faqs():
    body = """<section class="phead"><div class="wrap">
    <div class="crumb"><a href="/">Home</a> / FAQs</div>
    <h1>Frequently asked questions</h1>
    <p>The things we get asked most. If your question is not here, email %s and we will answer it.</p>
  </div></section>%s

<section class="sec"><div class="wrap" style="max-width:900px">%s</div></section>
%s""" % (EMAIL, trustband(), faq_block(FAQS), cta())
    page("faqs/index.html",
         "FAQs | Bus &amp; Coach Hire Questions | %s" % SITE,
         "Answers on areas covered, booking, group sizes, Garda vetting, school transport, airport runs and golf trips with %s." % SITE,
         body, extra_ld=faq_ld(FAQS))

def build_contact():
    opts = "".join('<option value="%s">%s</option>' % (n, n) for _, n, _, _ in SERVICES)
    phone_card = ""
    if PHONE:
        phone_card = """<div class="ccard"><h3>Phone</h3><p>Ronan is often driving, so if there is no answer leave a message or drop us an email and we will come straight back.</p>
        <p style="margin-top:8px"><a href="tel:%s">%s</a></p></div>""" % (PHONE_E164 or PHONE.replace(" ", ""), PHONE)
    body = """<section class="phead"><div class="wrap">
    <div class="crumb"><a href="/">Home</a> / Contact</div>
    <h1>Get a quote</h1>
    <p>Tell us the date, the group size and where you are going. We will confirm availability and price, usually the same day.</p>
  </div></section>%(trust)s

<section class="sec"><div class="wrap contact-grid">
  <form class="enq" novalidate>
    <div class="two">
      <div class="row"><label for="f-name">Your name</label><input id="f-name" name="name" type="text" autocomplete="name" required></div>
      <div class="row"><label for="f-phone">Phone</label><input id="f-phone" name="phone" type="tel" autocomplete="tel"></div>
    </div>
    <div class="row"><label for="f-email">Email</label><input id="f-email" name="email" type="email" autocomplete="email" required></div>
    <div class="two">
      <div class="row"><label for="f-service">What do you need?</label>
        <select id="f-service" name="service"><option value="">Please choose</option>%(opts)s<option value="Something else">Something else</option></select></div>
      <div class="row"><label for="f-date">Date needed</label><input id="f-date" name="date" type="date"></div>
    </div>
    <div class="two">
      <div class="row"><label for="f-pax">Number of passengers</label><input id="f-pax" name="passengers" type="number" min="1" inputmode="numeric"></div>
      <div class="row"><label for="f-pickup">Pick-up point</label><input id="f-pickup" name="pickup" type="text"></div>
    </div>
    <div class="row"><label for="f-dest">Destination</label><input id="f-dest" name="destination" type="text"></div>
    <div class="row"><label for="f-msg">Anything else we should know</label><textarea id="f-msg" name="message" placeholder="Timings, return journey, extra stops, luggage, anything at all."></textarea></div>
    <button class="btn btn-amber" type="submit" style="width:100%%">Send enquiry</button>
    <p class="formnote">This opens your email app with the details filled in, addressed to %(email)s. We do not take online bookings, every job is quoted properly.</p>
  </form>

  <div class="contact-cards">
    %(phonecard)s
    <div class="ccard"><h3>Email</h3><p>The fastest way to reach us. Sorica looks after the office and replies to enquiries.</p>
      <p style="margin-top:8px"><a href="mailto:%(email)s">%(email)s</a></p></div>
    <div class="ccard"><h3>Based in</h3><p>%(town)s, %(county)s</p><p style="margin-top:6px">Covering all of Leinster, with travel further afield subject to availability.</p></div>
    <div class="ccard"><h3>What to include</h3>
      <p>Date, group size, pick-up point, destination and rough timings. The more you give us, the faster we can price it.</p></div>
    <div class="ccard"><h3>Schools, clubs and companies</h3>
      <p>We can supply vetting, insurance and vehicle documentation for your records. Just ask when you enquire.</p></div>
  </div>
</div></section>""" % {"trust": trustband(), "opts": opts, "email": EMAIL,
                       "town": TOWN, "county": COUNTY, "phonecard": phone_card}
    page("contact/index.html",
         "Contact &amp; Quotes | %s, %s %s" % (SITE, TOWN, COUNTY),
         "Get a quote for bus or coach hire from %s. Email %s with your date, group size and destination and we will come back to you, usually the same day." % (SITE, EMAIL),
         body)

def build_404():
    body = """<section class="phead"><div class="wrap">
    <h1>Page not found</h1>
    <p>That page does not exist, or it has moved. Try one of these instead.</p>
  </div></section>
<section class="sec"><div class="wrap">
  <div class="grid g3">
    <a class="card" href="/"><h3>Home</h3><p>Back to the start.</p></a>
    <a class="card" href="/services/"><h3>Services</h3><p>Everything we carry groups for.</p></a>
    <a class="card" href="/contact/"><h3>Get a quote</h3><p>Tell us what you need.</p></a>
  </div>
</div></section>"""
    page("404.html", "Page not found | %s" % SITE,
         "That page could not be found on the %s website." % SITE, body, nav_path="/")

PAGES_FOR_SITEMAP = [("/", "1.0"), ("/services/", "0.9"), ("/golf-trips/", "0.9"),
                     ("/areas/", "0.8"), ("/about/", "0.7"), ("/faqs/", "0.7"),
                     ("/contact/", "0.9")]

def build_meta():
    import datetime
    today = datetime.date.today().isoformat()
    urls = "".join("  <url><loc>%s%s</loc><lastmod>%s</lastmod><priority>%s</priority></url>\n"
                   % (DOMAIN, p, today, pr) for p, pr in PAGES_FOR_SITEMAP)
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n'
                '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n%s</urlset>\n' % urls)
    with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as f:
        f.write("User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % DOMAIN)
    with open(os.path.join(ROOT, "vercel.json"), "w", encoding="utf-8") as f:
        f.write('{\n  "$schema": "https://openapi.vercel.sh/vercel.json",\n'
                '  "trailingSlash": true,\n'
                '  "headers": [\n    {\n      "source": "/assets/(.*)",\n'
                '      "headers": [{ "key": "Cache-Control", "value": "public, max-age=0, must-revalidate" }]\n'
                '    }\n  ]\n}\n')
    print("wrote sitemap.xml, robots.txt, vercel.json")

if __name__ == "__main__":
    build_home(); build_services(); build_golf(); build_about()
    build_areas(); build_faqs(); build_contact(); build_404(); build_meta()
    print("\nDone. Open index.html in a browser or run: npx serve .")
