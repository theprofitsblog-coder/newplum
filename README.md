# ProFlow Plumbing - Lead Generation Website

A nationwide plumbing lead-generation website with 2,854 static pages covering 24 states and 2,827 cities.

## Overview

This is a templated static site built to rank locally across thousands of cities and convert visitors into phone calls. The site uses a build system that generates all pages from CSV data + Jinja2 templates.

## Project Structure

```
├── build.py              # Main build script
├── content.py            # Content variation engine (intros, H1s, FAQs)
├── templates/            # Jinja2 HTML templates
│   ├── base.html         # Shared layout (header, footer, mobile CTA)
│   ├── index.html        # Homepage
│   ├── state.html        # State hub pages (×24)
│   └── city.html         # City landing pages (×2,827)
├── static/
│   └── css/style.css     # All styles (mobile-first)
├── data/
│   ├── state_hub_data.csv           # 24 states
│   ├── city_hub_data_with_zips.csv  # 2,827 cities with zip codes
│   └── zip_data_skipped_needs_lookup.csv  # 1,057 unresolved zips
└── output/               # Generated static site (ready to deploy)
```

## Quick Start

### Requirements
- Python 3.8+
- Jinja2 (`pip install jinja2`)

### Build the site
```bash
cd site
pip install jinja2
python3 build.py
```

### Deploy
The `output/` folder is a complete static site. Upload it to any static host:
- Netlify
- Cloudflare Pages
- Vercel
- AWS S3 + CloudFront
- GitHub Pages

### Configure for production
Before building for production, update `BASE_URL` in `build.py`:
```python
BASE_URL = 'https://yourdomain.com'
```

Then rebuild:
```bash
python3 build.py
```

## Site Stats

| Metric | Value |
|---|---|
| Total pages | 2,854 |
| States covered | 24 |
| Cities covered | 2,827 |
| Avg page size | ~11 KB |
| Total site size | ~34 MB |
| Build time | <1 second |

## Anti-Doorway-Page Measures

To comply with Google's scaled content policies, every city page has genuinely varied content:
- **12 unique H1 structures** rotate per city
- **20 unique intro paragraph templates** with regional context
- **6 regional FAQ sets** (northeast, southeast, midwest, southwest, mountain, pacific)
- Hash-based selection ensures consistent per-city variants without obvious repetition

## Schema Markup

- **Plumber/LocalBusiness** schema with `areaServed` (service-area business pattern)
- **FAQPage** schema on every city page
- **BreadcrumbList** schema for navigation
- No fabricated ratings, reviews, or addresses

## Phone Number

All pages use: **+1 (831) 532-6042**

## Rollout Plan

Per Google best practices, deploy in tranches rather than all at once:
1. **Tranche 1:** Homepage + 24 state hubs + top 3 states (NJ, MA, PA)
2. **Tranche 2+:** Remaining states, 3-5 per batch, spaced out

Monitor Google Search Console between tranches for any indexing issues.
