# -*- coding: utf-8 -*-


import os, re, json
from datetime import date, timedelta

SITE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TEMPLATE_PATH = os.path.join(SITE_DIR, "blog", "post.html")
POSTS_DIR = os.path.join(SITE_DIR, "blog", "posts")
DATA_DIR = os.path.join(SITE_DIR, "data")
SITEMAP_PATH = os.path.join(SITE_DIR, "sitemap.xml")

def ensure_dir(p): os.makedirs(p, exist_ok=True)

def slugify(s: str) -> str:
    s = s.lower().strip()
    s = re.sub(r"[^a-z0-9\s-]", "", s)
    s = re.sub(r"\s+", "-", s)
    s = re.sub(r"-{2,}", "-", s)
    return s[:80].strip("-") or "post"

def load_template():
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        return f.read()

def html_paragraphs(lines):
    # Convert list of lines into <p> blocks
    out = []
    for ln in lines:
        ln = ln.strip()
        if not ln:
            continue
        if ln.startswith("## "):
            out.append(f"<h2 style='margin:18px 0 8px; font-size:20px;'>{escape_html(ln[3:])}</h2>")
        elif ln.startswith("- "):
            # collect bullet lists simply
            out.append(f"<ul style='margin:10px 0 10px 18px;'><li>{escape_html(ln[2:])}</li></ul>")
        else:
            out.append(f"<p style='margin:10px 0;'>{escape_html(ln)}</p>")
    return "\n".join(out)

def escape_html(s: str) -> str:
    return (s.replace("&","&amp;")
             .replace("<","&lt;")
             .replace(">","&gt;")
             .replace('"',"&quot;")
             .replace("'","&#039;"))

def make_posts():
    # 30 topics (KDP practical, evergreen, safe)
    topics = [
        ("Publishing", "A simple keyword workflow that beats guessing"),
        ("Publishing", "How to choose categories without overthinking"),
        ("Publishing", "Paperback pricing: a practical way to pick a number"),
        ("Publishing", "KU vs non-KU: how to decide for low-ticket books"),
        ("Publishing", "How to build a series that the algorithm understands"),
        ("Publishing", "What ‘low content’ actually means and how to avoid it"),
        ("Workflow", "A 60-minute weekly routine to publish consistently"),
        ("Workflow", "Your upload checklist: reduce mistakes to near zero"),
        ("Workflow", "File naming rules that save hours later"),
        ("Workflow", "Batching: the only way to scale without burning out"),
        ("Design", "Cover basics that improve clicks (without fancy art)"),
        ("Design", "Spine and trim size: what to decide first"),
        ("Design", "Typography rules for workbook-style interiors"),
        ("Design", "How to keep a clean, readable layout for printing"),
        ("Quality", "Proofing strategy: catch 90% of issues fast"),
        ("Quality", "How to make answer keys feel ‘premium’"),
        ("Quality", "Why explanations at the end can boost perceived value"),
        ("Quality", "The simplest way to reduce negative reviews"),
        ("Marketing", "Product description formula that doesn’t sound spammy"),
        ("Marketing", "Keywords vs description: what each is actually for"),
        ("Marketing", "How to write a subtitle that helps ranking"),
        ("Marketing", "A lightweight ‘brand’ for authors with many books"),
        ("Math Workbooks", "How to structure a practice pack that feels complete"),
        ("Math Workbooks", "Daily warm-ups: format that readers actually use"),
        ("Math Workbooks", "Practice tests vs worksheets: which sells better"),
        ("Math Workbooks", "Grade-level clarity: reduce returns and confusion"),
        ("Ops", "Tracking titles: a spreadsheet structure that works"),
        ("Ops", "When to update a book vs publish a new edition"),
        ("Ops", "How to reuse content ethically: versioning + differentiation"),
        ("Ops", "A 90-day plan to reach 100+ listings without chaos"),
    ]

    # Generate dates: last 30 days ending today
    today = date.today()
    dates = [(today - timedelta(days=i)).isoformat() for i in range(len(topics))]
    dates.reverse()  # older first

    return [
        {
            "category": cat,
            "title": title,
            "date": dates[i],
        }
        for i, (cat, title) in enumerate(topics)
    ]

def write_post_html(template, post, slug):
    # Simple, original content blocks
    title = post["title"]
    cat = post["category"]
    d = post["date"]

    # Short description for meta tags
    meta_desc = f"{title}. Practical KDP publishing notes you can apply today."

    # Content body
    lines = [
        f"Here’s a practical approach to: {title.lower()}. This is written for people publishing consistently (even if each book only earns a few dollars at first).",
        "## Why this matters",
        "Small improvements compound. If you publish weekly, tiny optimizations in keywords, structure, and packaging become real money over time.",
        "## A simple method you can use today",
    ]

    # Category-specific advice
    if cat == "Publishing":
        lines += [
            "- Write down your book’s ‘buyer intent’ in one sentence (who buys it and why).",
            "- Pick 2–3 core phrases, then expand into 7 keyword phrases (no repetition).",
            "- Make title/subtitle match what people search, not what you wish they search.",
            "Keep it boring and accurate. Accuracy beats creativity for search traffic.",
        ]
    elif cat == "Workflow":
        lines += [
            "- Use a fixed weekly schedule: draft → format → export → upload pack → publish.",
            "- Create a checklist and never skip it (most mistakes are repeat mistakes).",
            "- Batch similar books together so you don’t context-switch all day.",
            "If your week is busy, do fewer titles—but keep the cadence.",
        ]
    elif cat == "Design":
        lines += [
            "- Use large, high-contrast title text. Mobile thumbnail readability matters.",
            "- Avoid clutter around the title area (no shapes crossing the text).",
            "- Keep margins and spacing consistent so the interior looks professional.",
            "Design is not about being fancy—it's about being clear.",
        ]
    elif cat == "Quality":
        lines += [
            "- Proof the first 10 pages and last 10 pages carefully (most issues show up there).",
            "- Make answer keys easy to locate and scan (consistent formatting).",
            "- If you include explanations, group them at the end to keep the practice flow clean.",
            "Fewer errors = fewer refunds = better long-term ranking.",
        ]
    elif cat == "Marketing":
        lines += [
            "- Start description with: who it’s for + what’s inside + how to use it.",
            "- Use short bullets for contents (readers skim).",
            "- Don’t keyword-stuff. Write for humans first.",
            "A clear description reduces bad-fit buyers and improves conversion.",
        ]
    elif cat == "Math Workbooks":
        lines += [
            "- Give structure: sections, mini-tests, and a final review.",
            "- Put explanations at the end (keeps students from peeking too early).",
            "- Make difficulty progression obvious (easy → medium → challenge).",
            "People buy confidence. Make the progression feel achievable.",
        ]
    else:  # Ops
        lines += [
            "- Track every title, keywords, categories, and update date in one sheet.",
            "- Use version numbers for interiors and covers to avoid uploading wrong files.",
            "- If a book is too similar to another, differentiate format (tests vs warm-ups vs quizzes).",
            "Operations is what lets you scale without headaches.",
        ]

    lines += [
        "## Quick takeaway",
        "Pick one improvement, apply it across your next 10 books, and measure. Repeat. That’s how ‘a few dollars’ turns into consistent daily income.",
    ]

    content_html = html_paragraphs(lines)

    html = (template
        .replace("{{TITLE}}", escape_html(title))
        .replace("{{DESCRIPTION}}", escape_html(meta_desc))
        .replace("{{CATEGORY}}", escape_html(cat))
        .replace("{{H1}}", escape_html(title))
        .replace("{{DATE}}", escape_html(d))
        .replace("{{CONTENT}}", content_html)
    )

    out_path = os.path.join(POSTS_DIR, f"{slug}.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)

    return out_path

def write_posts_json(posts_meta):
    ensure_dir(DATA_DIR)
    items = []
    for p in posts_meta:
        slug = slugify(p["title"])
        url = f"/blog/posts/{slug}.html"
        # Summary is short & safe
        summary = f"Practical notes: {p['title']}."
        items.append({
            "title": p["title"],
            "summary": summary,
            "url": url,
            "category": p["category"],
            "date": p["date"]
        })
    with open(os.path.join(DATA_DIR, "posts.json"), "w", encoding="utf-8") as f:
        json.dump({"posts": list(reversed(items))}, f, ensure_ascii=False, indent=2)
    # reverse so newest appears first on homepage/blog
    return items

def write_sitemap(posts_items):
    # Basic sitemap with root + key pages + all posts
    urls = [
        "/",
        "/blog/",
        "/pages/about.html",
        "/pages/contact.html",
        "/pages/privacy.html",
        "/pages/disclaimer.html",
        "/pages/terms.html",
    ] + [it["url"] for it in posts_items]

    xml = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        xml.append(f"  <url><loc>{u}</loc></url>")
    xml.append("</urlset>\n")

    with open(SITEMAP_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(xml))

def main():
    ensure_dir(POSTS_DIR)

    template = load_template()
    posts = make_posts()

    posts_items = []
    for p in posts:
        slug = slugify(p["title"])
        path = write_post_html(template, p, slug)
        posts_items.append({
            "url": f"/blog/posts/{slug}.html",
            "date": p["date"]
        })
        print("Wrote:", os.path.relpath(path, SITE_DIR))

    items = write_posts_json(posts)
    write_sitemap(items)

    print("\nDone.")
    print("Generated: data/posts.json")
    print("Generated: sitemap.xml")
    print("Generated posts in: blog/posts/")

if __name__ == "__main__":
    main()
