#!/usr/bin/env python3
"""Tools for the design-patterns catalog (a Docusaurus site in pt-BR and English).

Subcommands (run from the repository root):
  validate <dir>   Validates a catalog in both locales: files, frontmatter, sections,
                   tags declared in tags.yml, Java/Python/Go tabs, Mermaid, links,
                   pt-BR/en parity, sidebar and home-page cards.
  index <dir>      Regenerates the catalog page tables (pt-BR and en) from sidebars.ts
                   and the patterns' frontmatter. Keeps the hand-written header
                   (frontmatter, title and introduction) and updates the "Total" line.

<dir> is the catalog as <domain>/<catalog> (e.g. architecture/microservices).

Source of truth for the structure (groups, order and shared patterns): sidebars.ts,
whose object must stay valid JSON. Standard library only.
"""
import json
import os
import re
import sys

PT = "docs"
EN = "i18n/en/docusaurus-plugin-content-docs/current"
SIDEBARS = "sidebars.ts"
CARDS = "src/data/catalogs.json"
TAG_FILE = "tags.yml"  # in PT and in EN
TAB_ORDER = ["java", "python", "go"]  # TypeScript/C# may follow as a 4th tab

LANGS = {
    PT: {
        "groups": "## Grupos", "by_tag": "## Por etiqueta",
        "cols": ("Padrão", "Resumo", "Etiquetas", "Origem"),
        "total": "Total: {n} padrões em {g} grupos.",
        "total_re": r"^Total: \d+ padrões em \d+ grupos\.",
        "desc": "## Descrição",
        "sections": ["## Descrição", "## Problemas que resolve", "## Quando usar", "## Quando evitar",
                     "## Trade-offs", "## Diagrama", "## Padrões relacionados", "## Referência"],
    },
    EN: {
        "groups": "## Groups", "by_tag": "## By tag",
        "cols": ("Pattern", "Summary", "Tags", "Origin"),
        "total": "Total: {n} patterns in {g} groups.",
        "total_re": r"^Total: \d+ patterns in \d+ groups\.",
        "desc": "## Description",
        "sections": ["## Description", "## Problems it solves", "## When to use", "## When to avoid",
                     "## Trade-offs", "## Diagram", "## Related patterns", "## Reference"],
    },
}
ACCENTS = re.compile(r"[ãõçáéíóúâêôàÃÕÇÁÉÍÓÚÂÊÔÀ]")
DIAGRAM_IMPORT = re.compile(r"^import (\w+) from '@site/docs/_diagrams/(.+?)\.mdx';$", re.M)


# ---------------------------------------------------------------- helpers
def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def split_fm(text):
    m = re.match(r"^---\n(.*?)\n---\n?", text, re.S)
    return (m.group(1), text[m.end():]) if m else ("", text)


def fm_field(text, key):
    m = re.search(rf"^{key}:\s*(.+)$", split_fm(text)[0], re.M)
    return m.group(1).strip().strip('"') if m else None


def fm_list(text, key):
    m = re.search(rf"^{key}:\s*\n((?:\s+-\s+.*\n?)+)", split_fm(text)[0] + "\n", re.M)
    return re.findall(r"^\s+-\s+(.+?)\s*$", m.group(1), re.M) if m else []


def tag_href(tag):
    return "/tags/" + re.sub(r"[^a-z0-9]+", "-", tag.lower()).strip("-")


def doc_file(root, url):
    """'/coding/gof/creational/builder' -> existing file under root, or None."""
    p = url.strip("/")
    for cand in (f"{root}/{p}.md", f"{root}/{p}.mdx", f"{root}/{p}/index.md", f"{root}/{p}/index.mdx"):
        if os.path.exists(cand):
            return cand
    if p == "" and os.path.exists(f"{root}/index.mdx"):
        return f"{root}/index.mdx"
    return None


def summary(root, url):
    f = doc_file(root, url)
    if not f:
        return None
    body = split_fm(read(f))[1]
    if LANGS[root]["desc"] not in body:
        return None
    para = body.split(LANGS[root]["desc"], 1)[1].strip().split("\n\n")[0].replace("\n", " ")
    para = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", para)  # links become plain text, as in the original tables
    m = re.match(r"(.+?[.!?])(\s|$)", para)
    return (m.group(1) if m else para).replace("|", "/")


def declared_tags(root):
    path = f"{root}/{TAG_FILE}"
    return set(re.findall(r'^"(.+)":\s*$', read(path), re.M)) if os.path.exists(path) else set()


def tab_errors(f, t):
    """Each <Tabs> block must start with java, python and go, in that order."""
    out = []
    for block in re.findall(r"<Tabs\b.*?</Tabs>", t, re.S):
        values = re.findall(r'<TabItem value="([^"]+)"', block)
        if values[:3] != TAB_ORDER:
            out.append(f"{f}: tabs {values}, expected {TAB_ORDER} first")
    if "<Tabs" in t and not re.search(r"^mdx:\s*\n\s+format:\s*mdx\s*$", split_fm(t)[0], re.M):
        out.append(f"{f}: uses <Tabs> but the frontmatter lacks 'mdx: format: mdx'")
    return out


def load_sidebar():
    m = re.search(r"=\s*(\{.*\});\s*\n\s*export", read(SIDEBARS), re.S)
    if not m:
        sys.exit(f"{SIDEBARS}: sidebar object not found")
    try:
        return json.loads(m.group(1))
    except json.JSONDecodeError as e:
        sys.exit(f"{SIDEBARS}: the object must be valid JSON ({e})")


def catalog_entry(d):
    """Sidebar category of catalog d ('<domain>/<catalog>')."""
    for dom in load_sidebar()["catalog"]:
        if not isinstance(dom, dict):
            continue
        for cat in dom.get("items", []):
            if cat.get("link", {}).get("id") == f"{d}/index":
                return cat
    sys.exit(f"{d}: catalog not found in {SIDEBARS} (link.id = '{d}/index')")


def catalog_items(d):
    """[(group_slug, group_name, [item])], item = {url, title, shared, doc}."""
    cat = catalog_entry(d)
    out = []
    for g in cat["items"]:
        gslug = g["key"][len(cat["key"]) + 1:] if g["key"].startswith(cat["key"] + "-") else g["key"]
        items = []
        for it in g["items"]:
            if isinstance(it, str):
                f = doc_file(PT, "/" + it)
                title = fm_field(read(f), "title") if f else it
                items.append({"url": "/" + it, "title": title, "shared": False, "doc": it})
            else:
                url = it["href"].split("?")[0]
                items.append({"url": url, "title": it["label"], "shared": True, "doc": url.strip("/")})
        out.append((gslug, g["label"], items))
    return out


# ---------------------------------------------------------------- index
def render_index(d, root):
    L = LANGS[root]
    path = f"{root}/{d}/index.md"
    if not os.path.exists(path):
        sys.exit(f"{path}: write the header first (frontmatter, title, introduction and Total line)")
    current = read(path)
    if L["groups"] not in current:
        sys.exit(f"{path}: missing the '{L['groups']}' section that marks the end of the header")
    head = current.split("\n" + L["groups"], 1)[0].rstrip() + "\n"
    groups = catalog_items(d)
    n = sum(len(i) for _, _, i in groups)
    head, k = re.subn(L["total_re"], L["total"].format(n=n, g=len(groups)), head, count=1, flags=re.M)
    if not k:
        sys.exit(f"{path}: missing the 'Total' line in the header")

    texts = {}
    for _, _, items in groups:
        for it in items:
            f = doc_file(root, it["url"]) or doc_file(PT, it["url"])
            texts[it["url"]] = read(f) if f else ""
    has_origin = any(fm_field(t, "origin") for t in texts.values() if t)
    known = re.findall(r"^### (.+?) \(\d+\)$", current.split(L["by_tag"], 1)[1], re.M) if L["by_tag"] in current else []
    by_tag = {t: [] for t in known}

    out = [head, L["groups"], ""]
    out += [f"- [{name}](#{slug}) ({len(items)})" for slug, name, items in groups] + [""]
    c = L["cols"]
    for slug, name, items in groups:
        out += [f"## {name} ({len(items)}) {{#{slug}}}", ""]
        out.append(f"| {c[0]} | {c[1]} | {c[2]} |" + (f" {c[3]} |" if has_origin else ""))
        out.append("| --- | --- | --- |" + (" --- |" if has_origin else ""))
        for it in items:
            t = texts[it["url"]]
            tags = fm_list(t, "tags")
            for x in tags:
                by_tag.setdefault(x, []).append((it["title"], it["url"]))
            s = summary(root, it["url"]) or summary(PT, it["url"]) or "—"
            row = f"| [{it['title']}]({it['url']}){' ★' if it['shared'] else ''} | {s} | " \
                  f"{' '.join(f'[`{x}`]({tag_href(x)})' for x in tags) or '—'} |"
            if has_origin:
                row += f" {fm_field(t, 'origin') or '—'} |"
            out.append(row)
        out.append("")
    out += [L["by_tag"], ""]
    for tag, items in by_tag.items():
        if items:
            out += [f"### {tag} ({len(items)})", "", ", ".join(f"[{a}]({b})" for a, b in items), ""]
    write(path, "\n".join(out).rstrip() + "\n")
    print(f"{path} generated")


def cmd_index(d):
    for root in (PT, EN):
        render_index(d, root)


# ---------------------------------------------------------------- validate
def cmd_validate(d):
    errs, warns = [], []
    groups = catalog_items(d)
    total = sum(len(i) for _, _, i in groups)
    sidebar_docs = {it["doc"] for _, _, items in groups for it in items if not it["shared"]}

    tagsets = {root: declared_tags(root) for root in (PT, EN)}
    for root in (PT, EN):
        if not os.path.exists(f"{root}/{d}/index.md"):
            errs.append(f"{root}/{d}/index.md: does not exist")

    for gslug, gname, items in groups:
        for it in items:
            if it["shared"]:
                real = doc_file(PT, it["url"])
                if not real:
                    errs.append(f"sidebar {d}/{gslug}: shared pattern points to {it['url']}, which does not exist")
                elif f"{d}/{gslug}" not in fm_list(read(real), "also_in"):
                    errs.append(f"{real}: missing also_in '{d}/{gslug}'")
                continue
            for root in (PT, EN):
                f = doc_file(root, it["url"])
                if not f:
                    errs.append(f"{root}{it['url']}.md: does not exist")
                    continue
                t = read(f)
                if fm_field(t, "category") != gname:
                    errs.append(f"{f}: category != '{gname}'")
                for key in ("title", "pattern_slug", "source", "sidebar_label"):
                    if not fm_field(t, key):
                        errs.append(f"{f}: missing '{key}' in the frontmatter")
                if not fm_list(t, "tags"):
                    errs.append(f"{f}: missing 'tags' in the frontmatter")
                for tag in fm_list(t, "tags"):
                    if tag not in tagsets[root]:
                        errs.append(f"{f}: tag '{tag}' is not in {root}/{TAG_FILE}")
                errs += tab_errors(f, t)
                for s in LANGS[root]["sections"]:
                    if not re.search("^" + re.escape(s) + r"\s*$", t, re.M):
                        errs.append(f"{f}: missing section '{s}'")
                # Diagrams: one shared English file per diagram, in docs/_diagrams/,
                # imported by both versions of the page. No inline mermaid blocks.
                if "```mermaid" in t:
                    errs.append(f"{f}: inline mermaid block (move it to docs/_diagrams/ and import it)")
                diagrams = DIAGRAM_IMPORT.findall(t)
                if not diagrams:
                    errs.append(f"{f}: does not import a diagram from docs/_diagrams/")
                if diagrams and not re.search(r"^mdx:\s*\n\s+format:\s*mdx\s*$", split_fm(t)[0], re.M):
                    errs.append(f"{f}: imports a diagram but the frontmatter lacks 'mdx: format: mdx'")
                for name, path in diagrams:
                    if f"<{name} />" not in t:
                        errs.append(f"{f}: imports {name} but does not use <{name} />")
                    part = f"{PT}/_diagrams/{path}.mdx"
                    if not os.path.exists(part):
                        errs.append(f"{f}: diagram {part} does not exist")
                    else:
                        pt_text = read(part)
                        if "```mermaid" not in pt_text:
                            errs.append(f"{part}: missing mermaid block")
                        if ACCENTS.search(pt_text):
                            errs.append(f"{part}: accented characters (the diagram must be in English)")

            pt_f, en_f = doc_file(PT, it["url"]), doc_file(EN, it["url"])
            if pt_f and en_f:
                pt, en = read(pt_f), read(en_f)
                if split_fm(pt)[0] != split_fm(en)[0]:
                    errs.append(f"{en_f}: frontmatter differs from pt-BR")
                links = lambda t: sorted(re.findall(r"\]\(([^)\s]+)\)", t))
                if links(pt) != links(en):
                    errs.append(f"{en_f}: links differ from pt-BR {sorted(set(links(pt)) ^ set(links(en)))}")
                heads = lambda t: len(re.findall(r"^#+ ", t, re.M))
                if heads(pt) != heads(en):
                    errs.append(f"{en_f}: {heads(en)} headings, pt-BR has {heads(pt)}")
                if DIAGRAM_IMPORT.findall(pt) != DIAGRAM_IMPORT.findall(en):
                    errs.append(f"{en_f}: imports different diagrams from pt-BR")
                if pt.count("```") != en.count("```"):
                    errs.append(f"{en_f}: number of code blocks differs from pt-BR")
                ratio = len(en.split()) / max(1, len(pt.split()))
                if not 0.8 <= ratio <= 1.25:
                    warns.append(f"{en_f}: length {ratio:.2f}x the pt-BR (missing or extra passage?)")
                body = re.sub(r"\]\([^)]*\)|https?://\S+", "", split_fm(en)[1])
                if ACCENTS.search(body):
                    errs.append(f"{en_f}: accented characters (Portuguese in the English text?)")

    # files missing from the sidebar, and internal links
    for root in (PT, EN):
        for f in sorted(p for p in (os.path.join(r, x) for r, _, fs in os.walk(f"{root}/{d}") for x in fs)
                        if p.endswith(".md")):
            rel = f[len(root) + 1:-3]
            if not rel.endswith("/index") and rel not in sidebar_docs:
                errs.append(f"{f}: not in {SIDEBARS}")
            for link in re.findall(r"\]\(([^)\s#]+)(?:#[^)]*)?\)", read(f)):
                if link.endswith(".md") or link.endswith(".mdx"):
                    errs.append(f"{f}: relative link '{link}' (use the page's absolute URL)")
                elif link.startswith("/") and not link.startswith("/tags/") and not doc_file(PT, link):
                    errs.append(f"{f}: broken link '{link}'")

    # home-page card
    cards = [c for c in json.loads(read(CARDS))["catalogs"] if c["href"] == f"/{d}"]
    if not cards:
        errs.append(f"{CARDS}: missing the card for /{d}")
    elif (cards[0]["patterns"], cards[0]["groups"]) != (total, len(groups)):
        errs.append(f"{CARDS}: card for /{d} says {cards[0]['patterns']} patterns/{cards[0]['groups']} groups; "
                    f"the sidebar has {total}/{len(groups)}")

    print(f"{d}: {total} patterns in {len(groups)} groups")
    for w in warns:
        print("warning:", w)
    print("\n".join(errs) if errs else "OK, no errors")
    return 1 if errs else 0


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] not in ("validate", "index"):
        print(__doc__)
        sys.exit(2)
    target = sys.argv[2].strip("/")
    sys.exit((cmd_validate if sys.argv[1] == "validate" else cmd_index)(target) or 0)
