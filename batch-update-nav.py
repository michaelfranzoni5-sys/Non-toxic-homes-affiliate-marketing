#!/usr/bin/env python3
"""Batch-update all article headers with dropdown nav."""
import os, re

PROJECT = os.path.expanduser("~/projects/non-toxic-homes")

DROPDOWN_NAV = '''      <nav class="header-nav">
        <a href="/">Home</a>
        <a href="/guides.html">All Guides</a>
        <span class="nav-item">
          <a href="/blog/water-filters/">Water ▾</a>
          <div class="nav-dropdown">
            <a href="/blog/water-filters/best-water-filters-2026.html">Best Water Filters 2026</a>
            <a href="/blog/water-filters/best-countertop-reverse-osmosis.html">Countertop RO Systems</a>
            <a href="/blog/water-filters/pfas-water-filters.html">PFAS Water Filters</a>
            <a href="/blog/water-filters/best-under-sink-water-filter.html">Best Under-Sink Filters</a>
            <a href="/blog/water-filters/waterdrop-d4-review.html">Waterdrop D4 Review</a>
          </div>
        </span>
        <span class="nav-item">
          <a href="/blog/air-purifiers/">Air ▾</a>
          <div class="nav-dropdown">
            <a href="/blog/air-purifiers/best-air-purifiers-allergies-2026.html">Best Air Purifiers for Allergies</a>
            <a href="/blog/air-purifiers/budget-air-purifiers-under-200.html">Budget Air Purifiers</a>
            <a href="/blog/air-purifiers/levoit-core-300-review.html">Levoit Core 300 Review</a>
            <a href="/blog/air-purifiers/best-hepa-air-purifiers-under-500.html">Best HEPA Under $500</a>
            <a href="/blog/air-purifiers/winix-5500-2-review.html">Winix 5500-2 Review</a>
          </div>
        </span>
        <span class="nav-item">
          <a href="/blog/cookware/">Cookware ▾</a>
          <div class="nav-dropdown">
            <a href="/blog/cookware/best-non-toxic-cookware-2026.html">Best Non-Toxic Cookware</a>
            <a href="/blog/cookware/ceramic-vs-stainless-steel-cookware.html">Ceramic vs Stainless Steel</a>
            <a href="/blog/cookware/best-non-toxic-pans-2026.html">Best Non-Toxic Pans</a>
            <a href="/blog/cookware/best-non-toxic-water-bottles.html">Best Water Bottles</a>
          </div>
        </span>
        <span class="nav-item">
          <a href="/blog/sleep/">Sleep ▾</a>
          <div class="nav-dropdown">
            <a href="/blog/sleep/best-organic-mattresses-2026.html">Best Organic Mattresses</a>
            <a href="/blog/sleep/best-non-toxic-pillows-2026.html">Best Pillows</a>
            <a href="/blog/sleep/best-non-toxic-bed-sheets-2026.html">Best Bed Sheets</a>
          </div>
        </span>
        <span class="nav-item">
          <a href="/blog/cleaning/">Cleaning ▾</a>
          <div class="nav-dropdown">
            <a href="/blog/cleaning/best-non-toxic-cleaning-products-2026.html">Best Cleaning Products</a>
            <a href="/blog/cleaning/branch-basics-review.html">Branch Basics Review</a>
            <a href="/blog/cleaning/best-non-toxic-laundry-detergent-2026.html">Best Laundry Detergent</a>
          </div>
        </span>
        <span class="nav-item">
          <a href="/blog/supplements/">Supplements ▾</a>
          <div class="nav-dropdown">
            <a href="/blog/supplements/best-supplements-for-longevity.html">Best Longevity Supplements</a>
            <a href="/blog/supplements/best-magnesium-supplement.html">Best Magnesium</a>
            <a href="/blog/supplements/best-omega-3-supplements-2026.html">Best Omega-3</a>
            <a href="/blog/supplements/vitamin-d-guide.html">Vitamin D Guide</a>
          </div>
        </span>
      </nav>'''

# Old patterns to match in article headers
OLD_NAV = re.compile(
    r'<nav class="header-nav">\s*<a href="/">Home</a>\s*<a href="/guides.html">All Guides</a>\s*(?:<a href="[^"]*">[^<]*</a>\s*)+</nav>',
    re.DOTALL
)

# Also match the plain nav with no dropdowns
OLD_NAV2 = re.compile(
    r'<nav class="header-nav">.*?</nav>',
    re.DOTALL
)

# Also match the inline style version in guides.html
OLD_NAV_GUIDES = re.compile(
    r'<nav class="header-nav">\s*<a href="/">Home</a>\s*<a href="/guides.html">All Guides</a>\s*<a href="[^"]*">[^<]*</a>\s*<a href="[^"]*">[^<]*</a>\s*<a href="[^"]*">[^<]*</a>\s*<a href="[^"]*">[^<]*</a>\s*<a href="[^"]*">[^<]*</a>\s*<a href="[^"]*">[^<]*</a>\s*</nav>',
    re.DOTALL
)

count = 0
for root, dirs, files in os.walk(os.path.join(PROJECT, 'blog')):
    for fname in files:
        if fname.endswith('.html'):
            fpath = os.path.join(root, fname)
            with open(fpath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Skip if already has dropdown nav
            if 'nav-item' in content:
                continue
            
            new_content = OLD_NAV.sub(DROPDOWN_NAV, content)
            if new_content == content:
                new_content = OLD_NAV2.sub(DROPDOWN_NAV, content, count=1)
            
            if new_content != content:
                with open(fpath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                count += 1
                print(f"  ✓ {os.path.relpath(fpath, PROJECT)}")
            else:
                print(f"  ✗ {os.path.relpath(fpath, PROJECT)}")

print(f"\nDone: {count} files updated")