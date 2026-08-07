# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

The personal site of Arshad Hossain — an independent Meta Ads and SEO specialist based in Dhaka, Bangladesh, working with clients in the US, Canada and Singapore. It exists to win inbound client enquiries via Google and via AI assistants.

Hand-written static HTML. **No build step, no package.json, no dependencies, no test suite.**

- Preview: `python3 -m http.server 8080` from the repo root, then `http://localhost:8080/`. Use HTTP, not `file://` — Formspree submissions send `Origin: null` from `file://` and get rejected.

## Deployment — pushing is publishing

**Live at `https://www.arshadhossain.com`, on Vercel, git-connected to `arshadsignup-wq/arshad-hossain-website`, auto-deploying from `main`.** There is no staging. A push to `main` is a production release.

- **Canonical host is `www`.** The apex 308-redirects to it. Every canonical, `og:url`, and JSON-LD URL must use `https://www.arshadhossain.com/`.
- `vercel.json` holds the redirect map, `trailingSlash: true`, and cache headers. **Any time a page is renamed or moved, add a 301 to `vercel.json` in the same commit.**

## URLs are directories

Every page is `<path>/index.html` and serves at a clean URL with no `.html`:

| File | URL |
| --- | --- |
| `index.html` | `/` |
| `cases/index.html` | `/cases/` |
| `cases/<slug>/index.html` | `/cases/<slug>/` |
| `blog/index.html`, `blog/<slug>/index.html` | `/blog/`, `/blog/<slug>/` |
| `projects/index.html`, `projects/<slug>/index.html` | `/projects/`, `/projects/<slug>/` |
| `contact/index.html`, `free-audit/index.html` | `/contact/`, `/free-audit/` |

Directory indexes were chosen over a host config (`cleanUrls`) so the URLs work on any static host, not just Vercel.

**Path depth is the most common breakage.** Root pages link `cases/`; depth-1 pages link `../cases/`; depth-2 pages link `../../cases/` and `../../style-v2.css`. Images in `cases/<slug>/` reference `../<file>.png`.

## Structure

| Path | Role |
| --- | --- |
| `style-v2.css` | The only stylesheet. Every page uses it. |
| `motion.js` | Scroll reveal, nav condense, stat count-ups, hero panel, testimonial slider. |
| `form.js` | Shared Formspree AJAX handler. |
| `404.html` | Served by Vercel on any unmatched path. |
| `cases/*.png`, `projects/*.png` | Screenshots, alongside the detail pages that use them. |
| `meta case/`, `seo case/` | Original screenshot sources. **Unreferenced** — live copies are in `cases/`. |

## Forms

All three POST to Formspree. **There is no email address anywhere on the site and that is deliberate** — everything goes through a form. Don't reintroduce a `mailto:`.

| Form | Endpoint |
| --- | --- |
| `free-audit/` | `https://formspree.io/f/xppazedk` |
| `contact/` and the homepage contact block | `https://formspree.io/f/xwlekjoj` |

Each keeps a real `action`/`method` so it works with JS off; `form.js` intercepts and writes into `.form-status`. Every form carries a `_gotcha` honeypot inside `.hp` and a `_subject` hidden field. The audit form's service checkboxes all share `name="services"`.

## Conventions

- **Nav and footer are duplicated in every HTML file** — no includes. A change to either must be applied everywhere, at the correct path depth.
- **Two vermillions.** `--accent` (`#e0673f`) for text and accents on dark; `--accent-deep` (`#c44020`, the original brand value) only behind white button text. The original fails contrast as text on near-black — don't swap them.
- **`.prose a` needs `:not(.btn)`.** `.prose a` outranks `.btn-primary` on specificity, so without the exclusion the CTA inside a post renders accent-on-accent and the label disappears.
- **Fonts: Geist (headings and display numbers) and Hanken Grotesk (everything else).** Only these two, site-wide.
- The `seo` modifier class switches a card or label from vermillion to green.
- **Case numbering is a global `01`–`12` sequence** shared between `/cases/` and the homepage's featured subset, which is deliberately out of order. Adding or merging a case means updating both.
- **No scroll-reveal without the `.js` gate.** Hidden states apply only under the `.js` class `motion.js` sets, with a 2s force-reveal backstop. An earlier build left blank screens at normal scrolling speed.
- Breakpoints: 1040px, 1000px, 980px, 720px.
- Special characters as HTML entities, not literal UTF-8.

## Content rules

**Every metric on this site comes from a real client account. Never invent or round a number.** No fabricated testimonials, no invented statistics, no made-up credentials. Blog posts carry a "Where these numbers come from" callout naming the account and linking the case study with the screenshots — keep that pattern.

Blog posts are written for E-E-A-T: visible byline with credentials, published and updated dates, `BlogPosting` JSON-LD, inline citations to authoritative sources, a sources list, and an author box. Verify cited URLs resolve before adding them.

Tone is plain-spoken and specific — short declarative sentences, numbers over adjectives, no agency jargon. Posts and case studies deliberately include what didn't work; that limitations section is what makes the rest credible.

A vendored `copywriting` skill lives at `.agents/skills/copywriting/` (symlinked into `.claude/skills/`, pinned in `skills-lock.json`).

## Known hazards

- **Regex-migrating these pages is dangerous.** A non-greedy `<div class="X">(.*?)</div>` silently truncates any page where that div contains nested divs. This corrupted four case studies (`lending`, `roofing`, `wardrobe-conversion`, `wardrobe-reel`) — their metrics grids nest inside `.case-body-text`. Always count nesting depth, and always check `<div` vs `</div>` counts per file afterwards.
- **`perl -pi` mangles UTF-8** unless the encoding layer is set; it double-encoded 11 separators in `cases/index.html` into `Â·`. Prefer Python with explicit `encoding="utf-8"` for any bulk edit.
- **zsh does not word-split unquoted variables** — `$FILES` passes as one argument. Use explicit filenames or arrays.
