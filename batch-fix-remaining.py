#!/usr/bin/env python3
"""Fix remaining edge cases: index pages + old-style articles."""

import os
import re

PROJECT = os.path.expanduser("~/projects/non-toxic-homes")

NEW_HEADER = '''  <header>
    <div class="header-top">
      <div class="header-top-left">
        <span class="search-icon">🔍</span>
        <input type="text" class="search-input" placeholder="Search Temple Keep..." onkeydown="if(event.key==='Enter'){var q=this.value.trim();if(q)window.location='https://www.google.com/search?q=site:templekeep.com+'+encodeURIComponent(q)}">
      </div>
      <a href="/" class="header-logo">temple<span>keep</span></a>
      <div class="header-utils">
        <a href="/about.html">About</a>
      </div>
      <button class="hamburger" aria-label="Toggle menu"><span></span><span></span><span></span></button>
    </div>
    <div class="header-bottom">
      <nav class="header-nav">
        <a href="/">Home</a>
        <a href="/guides.html">All Guides</a>
        <a href="/blog/water-filters/">Water</a>
        <a href="/blog/air-purifiers/">Air</a>
        <a href="/blog/cookware/">Cookware</a>
        <a href="/blog/sleep/">Sleep</a>
        <a href="/blog/cleaning/">Cleaning</a>
        <a href="/blog/supplements/">Supplements</a>
      </nav>
    </div>
    <div class="header-nav-mobile">
      <a href="/">Home</a>
      <a href="/guides.html">All Guides</a>
      <a href="/blog/water-filters/">Water</a>
      <a href="/blog/air-purifiers/">Air</a>
      <a href="/blog/cookware/">Cookware</a>
      <a href="/blog/sleep/">Sleep</a>
      <a href="/blog/cleaning/">Cleaning</a>
      <a href="/blog/supplements/">Supplements</a>
      <a href="/about.html">About</a>
    </div>
  </header>'''

JS_SCRIPT = '''<script>
(function(){var b=document.querySelector(".hamburger"),n=document.querySelector(".header-nav-mobile");b&&b.addEventListener("click",function(){b.classList.toggle("active");n.classList.toggle("mobile-open")})})();
</script>'''

# Pattern for compact all-in-one-line headers
COMPACT_HEADER = re.compile(
    r'<header>.*?<div class="container">\s*<a href="/" class="logo">temple<span>keep</span></a>\s*<nav><a href="/">Home</a>.*?</nav>\s*<button class="hamburger" aria-label="Toggle menu"><span></span><span></span><span></span></button>\s*</div></header>',
    re.DOTALL
)

index_files = [
    "blog/water-filters/index.html",
    "blog/air-purifiers/index.html",
    "blog/cookware/index.html",
    "blog/sleep/index.html",
    "blog/supplements/index.html",
]

# Old-style articles with no header at all (just inline styles + container)
old_files = [
    "blog/supplements/best-magnesium-supplement.html",
    "blog/supplements/vitamin-d-guide.html",
]

count = 0

# Fix index pages
for rel in index_files:
    fpath = os.path.join(PROJECT, rel)
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix indentation: the opening <header> is on same line as <body>
    # and closing </header> is before <main>
    new_content = COMPACT_HEADER.sub(NEW_HEADER, content)
    
    if new_content != content:
        if JS_SCRIPT.strip() not in new_content:
            new_content = new_content.replace('</body>', f'{JS_SCRIPT}\n</body>')
        # Also make sure there's a line break before <main>
        new_content = new_content.replace('<main', '\n  <main')
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"  ✓ {rel}")
        count += 1
    else:
        print(f"  ✗ {rel} - no match")

# Fix old-style articles - these have NO header at all, just <body><div class="container">
# Need to add the header + link to style.css
for rel in old_files:
    fpath = os.path.join(PROJECT, rel)
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove the inline <style> block entirely
    content = re.sub(r'<style>.*?</style>', '', content, count=1, flags=re.DOTALL)
    
    # Add link to style.css after the font preconnect
    content = content.replace(
        '<link rel="preconnect" href="https://fonts.googleapis.com">',
        '<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="stylesheet" href="/assets/css/style.css">'
    )
    
    # Replace <div class="container"> at start of body with header + article-wrap
    content = content.replace(
        '<body>\n<div class="container">',
        f'<body>\n{NEW_HEADER}\n\n  <div class="article-wrap">\n    <article>'
    )
    
    # Close the article/article-wrap properly before </body>
    # Find the closing container
    content = content.replace('</div>\n\n</body>', '</div>\n    </article>\n  </div>\n\n</body>')
    
    if JS_SCRIPT.strip() not in content:
        content = content.replace('</body>', f'{JS_SCRIPT}\n</body>')
    
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  ✓ {rel} (full conversion)")
    count += 1

print(f"\nDone: {count} files updated")