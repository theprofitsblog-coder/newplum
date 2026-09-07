#!/usr/bin/env python3
"""
ProFlow Plumbing - Static Site Builder
Reads CSV data and generates all static HTML pages using Jinja2 templates.
"""

import csv
import os
import sys
import time
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from content import (
    STATE_NAMES, get_h1, get_intro, get_faqs, slugify
)

# === CONFIG ===
DATA_DIR = Path(__file__).parent.parent / 'data'
TEMPLATE_DIR = Path(__file__).parent / 'templates'
OUTPUT_DIR = Path(__file__).parent / 'output'
BASE_URL = ''  # Set to your domain when deploying, e.g. 'https://example.com'

# === LOAD DATA ===
def load_state_data():
    """Load state hub data from CSV."""
    states = []
    with open(DATA_DIR / 'state_hub_data.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            states.append({
                'code': row['state'],
                'name': STATE_NAMES.get(row['state'], row['state']),
                'city_count': int(row['city_count']),
                'zip_count': int(row['zip_count'])
            })
    return states

def load_city_data():
    """Load city hub data from CSV."""
    cities = []
    with open(DATA_DIR / 'city_hub_data_with_zips.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            zip_codes = [z.strip() for z in row['zip_codes'].split(';') if z.strip()]
            slug = slugify(row['city'])
            # Handle slug collision with state hub index.html
            if slug == 'index':
                slug = 'index-city'
            cities.append({
                'state': row['state'],
                'city': row['city'],
                'slug': slug,
                'zip_count': int(row['zip_count']),
                'zip_codes': zip_codes
            })
    return cities

# === BUILD FUNCTIONS ===
def build_homepage(env, states):
    """Generate the homepage."""
    template = env.get_template('index.html')
    total_cities = sum(s['city_count'] for s in states)
    
    html = template.render(
        page_title='ProFlow Plumbing - Licensed Plumbers in 24 States',
        meta_description=f'Fast, reliable plumbing services across {len(states)} states and {total_cities} cities. Licensed plumbers ready for leaks, clogs, water heaters, and emergencies.',
        canonical_url=f'{BASE_URL}/',
        base_url=BASE_URL,
        states=states,
        states_list=[s['name'] for s in states],
        total_cities=total_cities,
        total_states=len(states)
    )
    
    out_path = OUTPUT_DIR / 'index.html'
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html)
    return 1

def build_state_pages(env, states, cities_by_state):
    """Generate all 24 state hub pages."""
    template = env.get_template('state.html')
    count = 0
    
    for state in states:
        code = state['code']
        state_slug = code.lower()
        cities = cities_by_state.get(code, [])
        city_names = [f"{c['city']}, {code}" for c in cities]
        
        html = template.render(
            page_title=f'Plumbing Services in {state["name"]} - ProFlow Plumbing',
            meta_description=f'Licensed plumbers serving {state["city_count"]} cities across {state["name"]}. Find a local plumber near you.',
            canonical_url=f'{BASE_URL}/plumbing/{state_slug}/',
            base_url=BASE_URL,
            state_name=state['name'],
            state_code=code,
            city_count=state['city_count'],
            cities=[{'name': c['city'], 'slug': c['slug']} for c in cities],
            city_names=city_names
        )
        
        out_path = OUTPUT_DIR / 'plumbing' / state_slug / 'index.html'
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(html)
        count += 1
    
    return count

def build_city_pages(env, cities, states_lookup):
    """Generate all 2,827 city pages."""
    template = env.get_template('city.html')
    count = 0
    errors = []
    
    for city_data in cities:
        try:
            state_code = city_data['state']
            city_name = city_data['city']
            state_slug = state_code.lower()
            city_slug = city_data['slug']
            state_name = STATE_NAMES.get(state_code, state_code)
            state_city_count = states_lookup.get(state_code, {}).get('city_count', 0)
            
            h1 = get_h1(city_name, state_code)
            intro = get_intro(city_name, state_code)
            faqs = get_faqs(city_name, state_code, state_city_count)
            
            html = template.render(
                page_title=f'{h1} - ProFlow Plumbing',
                meta_description=f'Need a plumber in {city_name}, {state_name}? We connect you with licensed local plumbers for leaks, clogs, water heaters, and emergencies. Call (831) 532-6042.',
                canonical_url=f'{BASE_URL}/plumbing/{state_slug}/{city_slug}/',
                base_url=BASE_URL,
                h1_text=h1,
                intro_text=intro,
                city_name=city_name,
                state_code=state_code,
                state_name=state_name,
                city_slug=city_slug,
                zip_codes=city_data['zip_codes'],
                faqs=faqs
            )
            
            out_path = OUTPUT_DIR / 'plumbing' / state_slug / f'{city_slug}.html'
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(html)
            count += 1
            
        except Exception as e:
            errors.append(f"Error building {city_data.get('city', '?')}, {city_data.get('state', '?')}: {e}")
    
    if errors:
        print(f"\n⚠️  {len(errors)} errors:")
        for err in errors[:10]:
            print(f"  - {err}")
        if len(errors) > 10:
            print(f"  ... and {len(errors) - 10} more")
    
    return count, errors

def build_static_pages(env):
    """Build About and Disclosure pages."""
    # About page
    about_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>About ProFlow Plumbing</title>
  <meta name="description" content="Learn about ProFlow Plumbing and our nationwide plumbing service network.">
  <link rel="stylesheet" href="{BASE_URL}/static/css/style.css">
</head>
<body>
  <header class="site-header">
    <a href="{BASE_URL}/" class="logo">ProFlow<span>Plumbing</span></a>
    <a href="tel:+18315326042" class="header-phone">
      <svg viewBox="0 0 24 24"><path d="M6.62 10.79a15.05 15.05 0 006.59 6.59l2.2-2.2a1 1 0 011.01-.24 11.36 11.36 0 003.58.57 1 1 0 011 1V20a1 1 0 01-1 1A17 17 0 013 4a1 1 0 011-1h3.5a1 1 0 011 1 11.36 11.36 0 00.57 3.58 1 1 0 01-.24 1.01l-2.2 2.2z"/></svg>
      (831) 532-6042
    </a>
    <nav><ul>
      <li><a href="{BASE_URL}/">Home</a></li>
      <li><a href="{BASE_URL}/#services">Services</a></li>
      <li><a href="{BASE_URL}/#areas">Service Areas</a></li>
      <li><a href="{BASE_URL}/about/">About</a></li>
    </ul></nav>
  </header>
  <div class="container">
    <h1 class="section-title">About ProFlow Plumbing</h1>
    <p class="page-intro">ProFlow Plumbing connects homeowners across 24 states with licensed, insured plumbing professionals. Whether you have a leaky faucet, a broken water heater, or a plumbing emergency, we help you find the right local plumber for the job.</p>
    <p class="page-intro">Our network covers {2827} cities and thousands of zip codes. Every plumber we work with holds proper state licensing and carries insurance. We believe in straightforward service and upfront pricing.</p>
    <p class="page-intro">We are a service-area business. That means we come to you. There is no storefront to visit. We dispatch licensed plumbers directly to your home when you need them.</p>
    <div class="cta-block">
      <h2>Need a Plumber?</h2>
      <p>Call us and we will connect you with a licensed plumber in your area.</p>
      <a href="tel:+18315326042" class="cta-btn">Call (831) 532-6042</a>
    </div>
  </div>
  <footer class="site-footer">
    <div class="footer-links">
      <a href="{BASE_URL}/">Home</a>
      <a href="{BASE_URL}/about/">About</a>
      <a href="{BASE_URL}/affiliate-disclosure/">Disclosure</a>
    </div>
    <p>ProFlow Plumbing &mdash; Licensed and insured plumbing services across 24 states.</p>
    <p style="margin-top:0.5rem;">Phone: <a href="tel:+18315326042">(831) 532-6042</a></p>
    <p style="margin-top:0.5rem;">&copy; 2025 ProFlow Plumbing. All rights reserved.</p>
  </footer>
  <div class="mobile-cta">
    <a href="tel:+18315326042">Call Now &mdash; (831) 532-6042</a>
  </div>
</body>
</html>"""

    # Affiliate disclosure page
    disclosure_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Disclosure - ProFlow Plumbing</title>
  <meta name="description" content="Business disclosure and affiliate information for ProFlow Plumbing.">
  <link rel="stylesheet" href="{BASE_URL}/static/css/style.css">
</head>
<body>
  <header class="site-header">
    <a href="{BASE_URL}/" class="logo">ProFlow<span>Plumbing</span></a>
    <a href="tel:+18315326042" class="header-phone">
      <svg viewBox="0 0 24 24"><path d="M6.62 10.79a15.05 15.05 0 006.59 6.59l2.2-2.2a1 1 0 011.01-.24 11.36 11.36 0 003.58.57 1 1 0 011 1V20a1 1 0 01-1 1A17 17 0 013 4a1 1 0 011-1h3.5a1 1 0 011 1 11.36 11.36 0 00.57 3.58 1 1 0 01-.24 1.01l-2.2 2.2z"/></svg>
      (831) 532-6042
    </a>
    <nav><ul>
      <li><a href="{BASE_URL}/">Home</a></li>
      <li><a href="{BASE_URL}/#services">Services</a></li>
      <li><a href="{BASE_URL}/#areas">Service Areas</a></li>
      <li><a href="{BASE_URL}/about/">About</a></li>
    </ul></nav>
  </header>
  <div class="container">
    <h1 class="section-title">Business Disclosure</h1>
    <p class="page-intro">ProFlow Plumbing is a lead generation service that connects homeowners with local plumbing professionals. We may receive compensation when a homeowner is connected with a plumber through our service.</p>
    <p class="page-intro">We do not perform plumbing work directly. All plumbing services are provided by independent, licensed plumbing professionals in our network. Each plumber is responsible for their own work, pricing, and warranties.</p>
    <p class="page-intro">We strive to provide accurate information about plumbing services and common plumbing issues. However, we recommend getting a clear estimate from any plumber before authorizing work.</p>
  </div>
  <footer class="site-footer">
    <div class="footer-links">
      <a href="{BASE_URL}/">Home</a>
      <a href="{BASE_URL}/about/">About</a>
      <a href="{BASE_URL}/affiliate-disclosure/">Disclosure</a>
    </div>
    <p>ProFlow Plumbing &mdash; Licensed and insured plumbing services across 24 states.</p>
    <p style="margin-top:0.5rem;">Phone: <a href="tel:+18315326042">(831) 532-6042</a></p>
    <p style="margin-top:0.5rem;">&copy; 2025 ProFlow Plumbing. All rights reserved.</p>
  </footer>
  <div class="mobile-cta">
    <a href="tel:+18315326042">Call Now &mdash; (831) 532-6042</a>
  </div>
</body>
</html>"""

    about_path = OUTPUT_DIR / 'about' / 'index.html'
    about_path.parent.mkdir(parents=True, exist_ok=True)
    about_path.write_text(about_html)

    disc_path = OUTPUT_DIR / 'affiliate-disclosure' / 'index.html'
    disc_path.parent.mkdir(parents=True, exist_ok=True)
    disc_path.write_text(disclosure_html)
    
    return 2

def build_sitemap(states, cities):
    """Generate XML sitemap."""
    urls = [f'{BASE_URL}/']
    
    for state in states:
        urls.append(f'{BASE_URL}/plumbing/{state["code"].lower()}/')
    
    for city in cities:
        urls.append(f'{BASE_URL}/plumbing/{city["state"].lower()}/{city["slug"]}/')
    
    urls.append(f'{BASE_URL}/about/')
    urls.append(f'{BASE_URL}/affiliate-disclosure/')
    
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for url in urls:
        xml += f'  <url><loc>{url}</loc></url>\n'
    xml += '</urlset>\n'
    
    sitemap_path = OUTPUT_DIR / 'sitemap.xml'
    sitemap_path.write_text(xml)
    return len(urls)

def copy_static():
    """Copy static assets to output directory."""
    import shutil
    static_src = Path(__file__).parent / 'static'
    static_dst = OUTPUT_DIR / 'static'
    if static_dst.exists():
        shutil.rmtree(static_dst)
    shutil.copytree(static_src, static_dst)

# === MAIN ===
def main():
    start = time.time()
    print("=" * 60)
    print("ProFlow Plumbing - Static Site Builder")
    print("=" * 60)
    
    # Setup
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)))
    env.globals['BASE_URL'] = BASE_URL
    
    # Load data
    print("\n📂 Loading data...")
    states = load_state_data()
    cities = load_city_data()
    print(f"   {len(states)} states, {len(cities)} cities loaded")
    
    # Group cities by state
    cities_by_state = {}
    for city in cities:
        state = city['state']
        if state not in cities_by_state:
            cities_by_state[state] = []
        cities_by_state[state].append(city)
    
    states_lookup = {s['code']: s for s in states}
    
    # Build pages
    print("\n🔨 Building pages...")
    
    print("   Homepage...", end=' ')
    n = build_homepage(env, states)
    print(f"{n} page")
    
    print("   State pages...", end=' ')
    n = build_state_pages(env, states, cities_by_state)
    print(f"{n} pages")
    
    print("   City pages...", end=' ')
    n, errors = build_city_pages(env, cities, states_lookup)
    print(f"{n} pages")
    
    print("   Static pages...", end=' ')
    n = build_static_pages(env)
    print(f"{n} pages")
    
    print("   Sitemap...", end=' ')
    n = build_sitemap(states, cities)
    print(f"{n} URLs")
    
    print("   Static assets...", end=' ')
    copy_static()
    print("copied")
    
    # Summary
    elapsed = time.time() - start
    total_files = sum(1 for _ in OUTPUT_DIR.rglob('*.html'))
    print(f"\n✅ Build complete in {elapsed:.1f}s")
    print(f"   Total HTML files: {total_files}")
    print(f"   Output directory: {OUTPUT_DIR}")
    
    if errors:
        print(f"\n⚠️  {len(errors)} pages had errors")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
