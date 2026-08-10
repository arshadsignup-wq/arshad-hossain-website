#!/usr/bin/env python3
"""Injector + linter for arshadhossain.com.

Not a static site generator. It never owns page content — only the block
between <!-- SEO:START --> and <!-- SEO:END --> in each <head>, plus
sitemap.xml. Delete this script and every page still renders correctly.

    python3 tools/build.py           write the head blocks + sitemap.xml
    python3 tools/build.py --check   verify only; non-zero exit if stale
    python3 tools/build.py --lint    run the linter alone

Run it after adding a page to tools/pages.py, or after moving anything.
"""
import io, os, re, sys, json, html, glob, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
os.chdir(ROOT)

from pages import PAGES, SITE, AUTHOR, IDENTITY, SAME_AS  # noqa: E402

START, END = "<!-- SEO:START -->", "<!-- SEO:END -->"
PERSON_ID = f"{SITE}/#arshad"
WEBSITE_ID = f"{SITE}/#website"


# ----------------------------------------------------------------- helpers
def read(p):
    return io.open(p, encoding="utf-8").read()


def write(p, s):
    io.open(p, "w", encoding="utf-8").write(s)


def url_for(path):
    """index.html -> /, cases/x/index.html -> /cases/x/"""
    d = os.path.dirname(path)
    return f"{SITE}/" + (f"{d}/" if d else "")


def git_mtime(path):
    try:
        out = subprocess.run(["git", "log", "-1", "--format=%cs", "--", path],
                             capture_output=True, text=True).stdout.strip()
        return out or None
    except Exception:
        return None


def esc(s):
    return html.escape(s, quote=True)


# ------------------------------------------------------------------ schema
def person_stub():
    return {"@type": "Person", "@id": PERSON_ID, "name": AUTHOR, "url": f"{SITE}/about/"}


def breadcrumbs(meta, path):
    trail = meta.get("crumbs") or []
    if not trail:
        return None
    items = []
    for i, (label, rel) in enumerate(trail, 1):
        items.append({"@type": "ListItem", "position": i, "name": label,
                      "item": f"{SITE}/{rel}"})
    items.append({"@type": "ListItem", "position": len(items) + 1,
                  "name": meta["title"].split(" · ")[0].split(" &middot; ")[0]})
    return {"@type": "BreadcrumbList",
            "@id": url_for(path) + "#breadcrumb", "itemListElement": items}


def faq_nodes(html_src, u):
    """Build FAQPage from the *visible* markup, so schema can never drift
    from what a reader sees. Expects <section class="faq"> with h3/p pairs."""
    sec = re.search(r'<section class="faq">(.*?)</section>', html_src, re.S)
    if not sec:
        return None
    qa = re.findall(r'<h3[^>]*>(.*?)</h3>\s*(.*?)(?=<h3|\Z)', sec.group(1), re.S)
    items = []
    for q, a in qa:
        q = re.sub(r'<[^>]+>', '', q).strip()
        a = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', a)).strip()
        if q and a:
            items.append({"@type": "Question", "name": html.unescape(q),
                          "acceptedAnswer": {"@type": "Answer", "text": html.unescape(a)}})
    if not items:
        return None
    return {"@type": "FAQPage", "@id": u + "#faq", "mainEntity": items}


def full_person():
    return {"@type": "Person", "@id": PERSON_ID, "name": AUTHOR,
            "url": f"{SITE}/about/",
            "jobTitle": "Independent Meta Ads and SEO Specialist",
            "description": IDENTITY,
            "address": {"@type": "PostalAddress",
                        "addressLocality": "Dhaka", "addressCountry": "BD"},
            "alumniOf": {"@type": "CollegeOrUniversity", "name": "BRAC University",
                         "address": {"@type": "PostalAddress",
                                     "addressLocality": "Dhaka", "addressCountry": "BD"}},
            "knowsAbout": ["Meta Ads", "Facebook Ads", "Instagram Ads",
                           "Click-to-Messenger Ads", "Conversions API",
                           "Search engine optimization", "Local SEO",
                           "Lead generation", "E-commerce advertising"],
            "knowsLanguage": ["en", "bn"],
            "sameAs": SAME_AS,
            "makesOffer": [{"@id": f"{SITE}/services/meta-ads-management/#service"},
                           {"@id": f"{SITE}/services/messenger-ads/#service"},
                           {"@id": f"{SITE}/services/seo/#service"}]}


def schema_for(path, meta, html_src=""):
    u = url_for(path)
    nodes = []
    kind = meta["kind"]

    if kind == "home":
        nodes.append({"@type": "WebSite", "@id": WEBSITE_ID, "url": f"{SITE}/",
                      "name": f"{AUTHOR} · Meta Ads & SEO",
                      "inLanguage": "en",
                      "publisher": {"@id": PERSON_ID}})
        nodes.append({"@type": "WebPage", "@id": u + "#page", "url": u,
                      "name": meta["title"], "description": meta["desc"],
                      "isPartOf": {"@id": WEBSITE_ID},
                      "about": {"@id": PERSON_ID}})
        nodes.append(person_stub())
    elif kind == "about":
        # The one page that defines the entity in full.
        nodes.append({"@type": "ProfilePage", "@id": u + "#page", "url": u,
                      "name": meta["title"], "description": meta["desc"],
                      "isPartOf": {"@id": WEBSITE_ID},
                      "mainEntity": {"@id": PERSON_ID}})
        nodes.append(full_person())
    elif kind == "service":
        nodes.append({"@type": "Service", "@id": u + "#service",
                      "name": meta.get("service_name", meta["title"]),
                      "serviceType": meta.get("service_type", "Digital marketing"),
                      "description": meta["desc"],
                      "provider": {"@id": PERSON_ID},
                      "areaServed": [{"@type": "Country", "name": n} for n in
                                     ("United States", "Canada", "Singapore", "Bangladesh")],
                      "url": u})
        nodes.append({"@type": "WebPage", "@id": u + "#page", "url": u,
                      "name": meta["title"], "description": meta["desc"],
                      "isPartOf": {"@id": WEBSITE_ID}})
        nodes.append(person_stub())
    elif kind == "dataset":
        # Dataset is a legitimate fit here and one of the few types with a
        # genuine independent discovery surface. CC-BY invites republication
        # *with attribution*, which is the off-site link pattern we want.
        nodes.append({"@type": "Dataset", "@id": u + "#dataset",
                      "name": meta["dataset_name"],
                      "description": meta["desc"],
                      "url": u,
                      "creator": {"@id": PERSON_ID},
                      "license": "https://creativecommons.org/licenses/by/4.0/",
                      "isAccessibleForFree": True,
                      "temporalCoverage": meta["coverage"],
                      "spatialCoverage": [{"@type": "Place", "name": n}
                                          for n in meta["places"]],
                      "measurementTechnique": meta["technique"],
                      "variableMeasured": [
                          {"@type": "PropertyValue", "name": v[0], "value": v[1],
                           "unitText": "USD", "description": v[2]}
                          for v in meta["variables"]]})
        nodes.append({"@type": "Article", "@id": u + "#article",
                      "headline": meta["title"], "description": meta["desc"],
                      "inLanguage": "en",
                      "image": SITE + meta.get("image", "/og-default.png"),
                      "author": {"@id": PERSON_ID},
                      "publisher": {"@id": PERSON_ID},
                      "isPartOf": {"@id": WEBSITE_ID},
                      "dateModified": meta.get("modified"),
                      "mainEntityOfPage": u})
        nodes.append(person_stub())
    elif kind == "post":
        nodes.append({"@type": "BlogPosting", "@id": u + "#post",
                      "headline": meta["title"], "description": meta["desc"],
                      "datePublished": meta["published"],
                      "dateModified": meta.get("modified", meta["published"]),
                      "inLanguage": "en",
                      "image": SITE + meta.get("image", "/og-default.png"),
                      "author": {"@id": PERSON_ID},
                      "publisher": {"@id": PERSON_ID},
                      "isPartOf": {"@id": WEBSITE_ID},
                      "mainEntityOfPage": u})
        nodes.append(person_stub())
    elif kind == "case":
        nodes.append({"@type": "Article", "@id": u + "#article",
                      "headline": meta["title"], "description": meta["desc"],
                      "inLanguage": "en",
                      "image": SITE + meta.get("image", "/og-default.png"),
                      "author": {"@id": PERSON_ID},
                      "publisher": {"@id": PERSON_ID},
                      "isPartOf": {"@id": WEBSITE_ID},
                      "mainEntityOfPage": u})
        nodes.append(person_stub())
    else:
        nodes.append({"@type": "WebPage", "@id": u + "#page", "url": u,
                      "name": meta["title"], "description": meta["desc"],
                      "isPartOf": {"@id": WEBSITE_ID}})
        nodes.append(person_stub())

    bc = breadcrumbs(meta, path)
    if bc:
        nodes.append(bc)
    faq = faq_nodes(html_src, u)
    if faq:
        nodes.append(faq)
    return {"@context": "https://schema.org", "@graph": nodes}


# ------------------------------------------------------------------- block
def head_block(path, meta, html_src=""):
    u = url_for(path)
    img = SITE + meta.get("image", "/og-default.png")
    og_type = "article" if meta["kind"] in ("post", "case") else "website"
    L = [START,
         f'<title>{esc(meta["title"])}</title>',
         f'<meta name="description" content="{esc(meta["desc"])}">']
    if meta.get("noindex"):
        # No canonical on a noindex page — 404.html lives at the root, so a
        # self-referential canonical would point every missing URL at the homepage.
        L.append('<meta name="robots" content="noindex, follow">')
    else:
        L.append(f'<link rel="canonical" href="{u}">')
    L += [f'<meta property="og:type" content="{og_type}">',
          f'<meta property="og:url" content="{u}">',
          f'<meta property="og:title" content="{esc(meta["title"])}">',
          f'<meta property="og:description" content="{esc(meta["desc"])}">',
          f'<meta property="og:image" content="{img}">',
          '<meta property="og:image:width" content="1200">',
          '<meta property="og:image:height" content="630">',
          '<meta property="og:site_name" content="Arshad Hossain">',
          '<meta property="og:locale" content="en_US">']
    if meta["kind"] == "post":
        L.append(f'<meta property="article:published_time" content="{meta["published"]}">')
        L.append(f'<meta property="article:modified_time" content="{meta.get("modified", meta["published"])}">')
    L += ['<meta name="twitter:card" content="summary_large_image">',
          f'<meta name="twitter:title" content="{esc(meta["title"])}">',
          f'<meta name="twitter:description" content="{esc(meta["desc"])}">',
          f'<meta name="twitter:image" content="{img}">',
          f'<meta name="author" content="{AUTHOR}">',
          '<meta name="theme-color" content="#0b0b0c">',
          '<link rel="icon" href="/favicon.ico" sizes="any">',
          '<link rel="icon" href="/favicon-32.png" type="image/png">',
          '<link rel="apple-touch-icon" href="/apple-touch-icon.png">',
          '<link rel="manifest" href="/site.webmanifest">',
          '<script type="application/ld+json">',
          json.dumps(schema_for(path, meta, html_src), indent=1, ensure_ascii=False),
          '</script>',
          END]
    return "\n".join(L)


def inject(path, meta, check=False):
    s = read(path)
    block = head_block(path, meta, s)

    if START in s and END in s:
        cur = s[s.index(START): s.index(END) + len(END)]
        if cur == block:
            return False
        if check:
            return True
        s = s.replace(cur, block)
    else:
        if check:
            return True
        # strip the hand-written tags the block now owns
        for pat in (r'[ \t]*<title>.*?</title>\n?',
                    r'[ \t]*<meta name="description"[^>]*>\n?',
                    r'[ \t]*<link rel="canonical"[^>]*>\n?',
                    r'[ \t]*<meta name="robots"[^>]*>\n?',
                    r'[ \t]*<script type="application/ld\+json">.*?</script>\n?'):
            s = re.sub(pat, '', s, flags=re.S)
        s = s.replace("</head>", block + "\n</head>", 1)
    write(path, s)
    return True


# ----------------------------------------------------------------- sitemap
def sitemap():
    rows = []
    for path, meta in PAGES.items():
        if meta.get("noindex") or not os.path.exists(path):
            continue
        last = meta.get("modified") or git_mtime(path)
        rows.append((url_for(path), last, meta["kind"]))
    prio = {"home": "1.0", "hub": "0.8", "case": "0.7", "post": "0.7",
            "form": "0.6", "project": "0.5"}
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u, last, kind in sorted(rows):
        out.append("  <url>")
        out.append(f"    <loc>{u}</loc>")
        if last:
            out.append(f"    <lastmod>{last}</lastmod>")
        out.append(f"    <priority>{prio.get(kind,'0.5')}</priority>")
        out.append("  </url>")
    out.append("</urlset>")
    return "\n".join(out) + "\n"


# ------------------------------------------------------------------ linter
def lint():
    problems = []
    seen_title, seen_desc = {}, {}
    all_pages = sorted(glob.glob("**/*.html", recursive=True))

    for p in all_pages:
        s = read(p)
        rel = p

        if rel not in PAGES:
            problems.append(f"{rel}: not in tools/pages.py manifest")
            continue

        # structure
        h1 = len(re.findall(r'<h1[\s>]', s))
        if h1 != 1:
            problems.append(f"{rel}: {h1} <h1> elements (want exactly 1)")
        if s.count("<main>") != 1 and PAGES[rel]["kind"] != "util":
            problems.append(f"{rel}: {s.count('<main>')} <main> landmarks")
        hs = [int(m.group(1)) for m in re.finditer(r'<h([1-6])[\s>]', s)]
        if any(hs[i + 1] - hs[i] > 1 for i in range(len(hs) - 1)):
            problems.append(f"{rel}: heading level skip")

        o, c = s.count("<div"), s.count("</div>")
        if o != c:
            problems.append(f"{rel}: unbalanced divs {o}/{c}")

        if b"\xc3\x82" in io.open(p, "rb").read():
            problems.append(f"{rel}: mojibake (double-encoded UTF-8)")

        # duplicates + lengths (skip noindex pages — they never appear in a SERP)
        t = PAGES[rel]["title"]; d = PAGES[rel]["desc"]
        if t in seen_title:
            problems.append(f"{rel}: duplicate title, also {seen_title[t]}")
        seen_title[t] = rel
        if d in seen_desc:
            problems.append(f"{rel}: duplicate description, also {seen_desc[d]}")
        seen_desc[d] = rel
        if not PAGES[rel].get("noindex"):
            if len(t) > 62:
                problems.append(f"{rel}: title {len(t)} chars (>62)")
            if not 110 <= len(d) <= 165:
                problems.append(f"{rel}: description {len(d)} chars (want 110-165)")

        # links + assets
        base = os.path.dirname(p)
        for attr, v in re.findall(r'\b(href|src)="([^"]*)"', s):
            if re.match(r'^(https?:|mailto:|#|data:|/)', v) or not v:
                continue
            v = v.split("#", 1)[0].split("?", 1)[0]   # fragment is not part of the path
            if not v:
                continue
            t_ = os.path.normpath(os.path.join(base, v)) if base else os.path.normpath(v)
            if not (os.path.isfile(t_) or
                    (os.path.isdir(t_) and os.path.isfile(os.path.join(t_, "index.html")))):
                problems.append(f"{rel}: broken {attr} -> {v}")

        for m in re.finditer(r'<img[^>]*>', s):
            tag = m.group(0)
            src = re.search(r'src="([^"]+)"', tag)
            if not src:
                continue
            if 'width=' not in tag or 'height=' not in tag:
                problems.append(f"{rel}: <img {src.group(1)}> missing width/height")
            f = os.path.normpath(os.path.join(base, src.group(1))) if base else src.group(1)
            if os.path.isfile(f) and os.path.getsize(f) > 300_000:
                problems.append(f"{rel}: {src.group(1)} is {os.path.getsize(f)//1024}KB (>300KB)")

    # manifest entries with no file
    for rel in PAGES:
        if not os.path.exists(rel):
            problems.append(f"{rel}: in manifest but file missing")

    # orphaned images
    used = set()
    for p in all_pages:
        base = os.path.dirname(p)
        for v in re.findall(r'src="([^"]+\.(?:png|jpe?g|webp|svg))"', read(p)):
            used.add(os.path.normpath(os.path.join(base, v)) if base else v)
    for img in glob.glob("**/*.png", recursive=True) + glob.glob("**/*.jpg", recursive=True) \
            + glob.glob("**/*.jpeg", recursive=True):
        if img.startswith((".git", "tools")):
            continue
        if os.path.normpath(img) not in used and os.path.basename(img) not in (
                "og-default.png", "favicon-32.png", "icon-512.png", "apple-touch-icon.png"):
            problems.append(f"ORPHAN image: {img} ({os.path.getsize(img)//1024}KB)")

    return problems


# -------------------------------------------------------------------- main
def main():
    check = "--check" in sys.argv
    only_lint = "--lint" in sys.argv

    changed = []
    if not only_lint:
        for path, meta in PAGES.items():
            if not os.path.exists(path):
                print(f"  ! manifest lists missing file: {path}")
                continue
            if inject(path, meta, check=check):
                changed.append(path)

        sm = sitemap()
        if not os.path.exists("sitemap.xml") or read("sitemap.xml") != sm:
            changed.append("sitemap.xml")
            if not check:
                write("sitemap.xml", sm)

    problems = lint()

    if check:
        if changed:
            print(f"STALE: {len(changed)} file(s) need `python3 tools/build.py`")
            for c in changed[:10]:
                print(f"  {c}")
        if problems:
            print(f"LINT: {len(problems)} problem(s)")
            for p in problems:
                print(f"  {p}")
        if changed or problems:
            sys.exit(1)
        print("OK — head blocks current, sitemap current, lint clean")
        return

    print(f"  injected/updated: {len(changed)} file(s)")
    if problems:
        print(f"\n  LINT — {len(problems)} problem(s):")
        for p in problems:
            print(f"    {p}")
    else:
        print("  lint: clean")


if __name__ == "__main__":
    main()
