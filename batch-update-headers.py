#!/usr/bin/env python3
"""Batch-update all article HTML files with the new two-row header."""

import os
import re

BLOG_DIR = os.path.expanduser("~/projects/non-toxic-homes/blog")

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

# The old header pattern - various forms
# Pattern 1: standard with nav links on separate lines
OLD_PATTERN_1 = r'''  <header>\s*<div class="container">\s*<a href="/" class="logo">temple<span>keep</span></a>\s*<nav>\s*<a href="/">Home</a>.*?</nav>\s*<button class="hamburger" aria-label="Toggle menu"><span></span><span></span><span></span></button>\s*</div>\s*</header>'''

# Pattern 2: all nav links on one line
OLD_PATTERN_2 = r'''  <header>\s*<div class="container">\s*<a href="/" class="logo">temple<span>keep</span></a>\s*<nav>\s*<a href="/">Home</a><a.*?</nav>\s*<button class="hamburger" aria-label="Toggle menu"><span></span><span></span><span></span></button>\s*</div>\s*</header>'''

# Pattern 3: links with some whitespace
OLD_PATTERN_3 = r'''  <header>\s*<div class="container">\s*<a href="/" class="logo">temple<span>keep</span></a>\s*<nav>.*?</nav>\s*<button class="hamburger" aria-label="Toggle menu"><span></span><span></span><span></span></button>\s*</div>\s*</header>'''

def update_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Try each pattern
    new_content = re.sub(OLD_PATTERN_1, NEW_HEADER, content, count=1, flags=re.DOTALL)
    
    if new_content != content:
        # Also add the script before </body> if not present
        if JS_SCRIPT.strip() not in new_content:
            new_content = new_content.replace('</body>', f'{JS_SCRIPT}\n</body>')
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True, "updated"
    
    new_content = re.sub(OLD_PATTERN_2, NEW_HEADER, content, count=1, flags=re.DOTALL)
    if new_content != content:
        if JS_SCRIPT.strip() not in new_content:
            new_content = new_content.replace('</body>', f'{JS_SCRIPT}\n</body>')
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True, "updated"
    
    new_content = re.sub(OLD_PATTERN_3, NEW_HEADER, content, count=1, flags=re.DOTALL)
    if new_content != content:
        if JS_SCRIPT.strip() not in new_content:
            new_content = new_content.replace('</body>', f'{JS_SCRIPT}\n</body>')
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True, "updated"
    
    return False, "no match"

# Walk the blog directory
updated = 0
no_match = 0
for root, dirs, files in os.walk(BLOG_DIR):
    for fname in files:
        if fname.endswith('.html'):
            fpath = os.path.join(root, fname)
            success, status = update_file(fpath)
            if success:
                updated += 1
                print(f"  ✓ {os.path.relpath(fpath, BLOG_DIR)}")
            else:
                no_match += 1
                print(f"  ✗ {os.path.relpath(fpath, BLOG_DIR)} - {status}")

print(f"\nDone: {updated} updated, {no_match} no match")