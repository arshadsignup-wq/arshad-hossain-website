# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A static personal marketing portfolio site for Arshad Hossain (Meta Ads / SEO freelancer). Hand-written HTML, no build step, no package.json, no dependencies, no test suite.

- Preview: `python3 -m http.server` from the repo root. Use HTTP rather than `file://` — the Google Fonts links and `form.js` behave normally either way, but HTTP matches production.
- No git remote and no deploy config — changes are local-only until one is added.

## Mid-redesign: two stylesheets

The site is **partway through a redesign** and this is the single most important thing to know before editing.

| Stylesheet | Used by | Status |
| --- | --- | --- |
| `style-v2.css` | `index.html`, `blog.html`, `blog/*.html`, `contact.html`, `free-audit.html` | Current design. All new work goes here. |
| `style.css` | `case-studies.html`, `projects.html`, `cases/*.html`, `projects/*.html` (17 files) | Legacy. Light theme, centred layout. Not yet migrated. |

The v2 design is dark end-to-end, left-aligned on a grid, and pairs **Inter Tight** (display) with **JetBrains Mono** (nav, labels, buttons, metadata). The legacy pages are light-themed and centred, so the two halves of the site currently look nothing alike. Migrating the remaining 17 pages to `style-v2.css` is the outstanding work.

Design references the owner chose: [sunnypatel.net](https://www.sunnypatel.net/) for visuals, [khalidfarhan.com](https://khalidfarhan.com/) for structure and section patterns (the dashed services grid, stacked article rows, and centred insights block are all modelled on it).

## Structure

| Path | Role |
| --- | --- |
| `index.html` | Homepage. Sections in order: hero → services → work → testimonials → background → blog → insights → contact. |
| `blog.html` + `blog/*.html` | Blog index and three long-form posts. |
| `free-audit.html` | Primary conversion page. The "Get a free audit" CTA everywhere points here. |
| `contact.html` | General enquiries. |
| `form.js` | Shared Formspree AJAX handler for all three forms. |
| `case-studies.html`, `cases/*.html` | Case study index + 11 detail pages, with screenshots alongside. |
| `projects.html`, `projects/*.html` | Side projects index + 4 detail pages. |
| `meta case/`, `seo case/` | Original screenshot sources. **Unreferenced** — live copies are in `cases/`. |

Images in `cases/` and `projects/` are referenced with bare filenames from pages in the same folder, and folder-prefixed from root pages.

## Forms

All three forms POST to Formspree. There is **no email address anywhere on the site** — this is deliberate, the owner wants everything to go through a form. Don't reintroduce a `mailto:`.

| Form | Endpoint |
| --- | --- |
| `free-audit.html` | `https://formspree.io/f/xppazedk` |
| `contact.html` and the homepage contact block | `https://formspree.io/f/xwlekjoj` |

Each form keeps a real `action` and `method="POST"`, so it still works with JavaScript disabled. `form.js` intercepts submit, POSTs via `fetch`, and writes into the `.form-status` element so people stay on the page. Every form carries a `_gotcha` honeypot (Formspree's convention) inside `.hp`, and a `_subject` hidden field.

The service checkboxes on the audit form all share `name="services"`, so Formspree receives repeated keys.

## Conventions

- **Nav and footer are duplicated in every HTML file** — no includes. A change to either must be applied across all of them, and the v2 and legacy pages have different footer markup.
- **Path depth** is the most common breakage. Root pages link `contact.html`; `blog/`, `cases/`, and `projects/` pages link `../contact.html` and `../style-v2.css`.
- **Design tokens** are custom properties at the top of `style-v2.css`. Note there are two vermillions: `--accent` (`#e0673f`) for text and accents on dark, and `--accent-deep` (`#c44020`, the original brand value) only behind white button text. The original hex fails contrast as text on near-black — don't swap them.
- **SEO vs Meta Ads colour coding** persists: the `seo` modifier class switches a card from vermillion to green.
- **Case numbering** (`01`–`11`) is a global sequence shared between `case-studies.html` and the homepage's featured subset, which is deliberately out of order. Adding a case means updating both.
- **No scroll-reveal animation.** An earlier build faded sections in on scroll and left blank screens at normal scrolling speed. It was removed on purpose — don't add it back.
- Responsive breakpoints in `style-v2.css` are at 1000px and 720px.
- Special characters are written as HTML entities rather than literal UTF-8.

## Content rules

Every metric on this site comes from a real client account. **Never invent or round a number.** Blog posts each carry a "Where these numbers come from" callout naming the account and linking the case study with the screenshots — keep that pattern.

Blog posts are written for E-E-A-T: visible author byline with credentials, published and updated dates, `BlogPosting` JSON-LD with author `sameAs` links, inline citations to authoritative sources, a sources list, and an author box. Cited URLs were verified to resolve at time of writing; re-check before adding new ones.

Tone throughout is plain-spoken and specific — short declarative sentences, numbers over adjectives, no agency jargon. The posts deliberately include what didn't work.

A vendored `copywriting` skill is checked in at `.agents/skills/copywriting/` (symlinked into `.claude/skills/`, pinned in `skills-lock.json`). Use it for hero, headline, CTA, and value-prop rewrites.
