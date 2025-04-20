from playwright.sync_api import sync_playwright
from datetime import datetime
import os

from config import threads_users

def fetch_threads(username):
    url = f"https://www.threads.net/@{username}"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=60000)
        content = page.content()
        browser.close()
        return content

def generate_rss(username, html):
    now = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
    rss = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>Threads feed for @{username}</title>
    <link>https://www.threads.net/@{username}</link>
    <description>RSS feed for Threads user @{username}</description>
    <lastBuildDate>{now}</lastBuildDate>
    <item>
      <title>Sample post title from @{username}</title>
      <link>https://www.threads.net/@{username}/post/example</link>
      <guid>post-example</guid>
      <pubDate>{now}</pubDate>
    </item>
  </channel>
</rss>"""
    with open(f"{username}.xml", "w", encoding="utf-8") as f:
        f.write(rss)
    print(f"[OK] Generated RSS for @{username}")

for user in threads_users:
    print(f"Fetching @{user}...")
    try:
        html = fetch_threads(user)
        generate_rss(user, html)
    except Exception as e:
        print(f"[ERR] {e}")
