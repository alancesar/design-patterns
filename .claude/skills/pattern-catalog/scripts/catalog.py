#!/usr/bin/env python3
"""Ferramentas do acervo de design patterns (site Docusaurus em pt-BR e inglês).

Subcomandos (rode a partir da raiz do repositório):
  validate <dir>   Valida um catálogo nos dois idiomas: arquivos, frontmatter, seções,
                   Mermaid, links, paridade pt-BR/en, sidebar e cards da home.
  index <dir>      Regenera as tabelas das páginas de catálogo (pt-BR e en) a partir do
                   sidebars.ts e do frontmatter dos padrões. Preserva o cabeçalho escrito
                   à mão (frontmatter, título e introdução) e atualiza a linha "Total".

<dir> é o catálogo no formato <domínio>/<catálogo> (ex.: architecture/microservices).

Fonte da verdade da estrutura (grupos, ordem e padrões compartilhados): sidebars.ts,
que precisa continuar com o objeto em JSON válido. Somente biblioteca padrão.
"""
import json
import os
import re
import sys

PT = "docs"
EN = "i18n/en/docusaurus-plugin-content-docs/current"
SIDEBARS = "sidebars.ts"
CARDS = "src/data/catalogs.json"

LANGS = {
    PT: {
        "groups": "## Grupos", "by_tag": "## Por etiqueta",
        "cols": ("Padrão", "Resumo", "Etiquetas", "Origem"),
        "total": "Total: {n} padrões em {g} grupos.",
        "total_re": r"^Total: \d+ padrões em \d+ grupos\.",
        "desc": "## Descrição",
        "sections": ["## Descrição", "## Problemas que resolve", "## Quando usar", "### Quando evitar",
                     "## Trade-offs", "## Diagrama", "## Padrões relacionados", "## Referência"],
    },
    EN: {
        "groups": "## Groups", "by_tag": "## By tag",
        "cols": ("Pattern", "Summary", "Tags", "Origin"),
        "total": "Total: {n} patterns in {g} groups.",
        "total_re": r"^Total: \d+ patterns in \d+ groups\.",
        "desc": "## Description",
        "sections": ["## Description", "## Problems it solves", "## When to use", "### When to avoid",
                     "## Trade-offs", "## Diagram", "## Related patterns", "## Reference"],
    },
}
ACCENTS = re.compile(r"[ãõçáéíóúâêôàÃÕÇÁÉÍÓÚÂÊÔÀ]")


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
    para = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", para)  # links viram texto, como nas tabelas originais
    m = re.match(r"(.+?[.!?])(\s|$)", para)
    return (m.group(1) if m else para).replace("|", "/")


def load_sidebar():
    m = re.search(r"=\s*(\{.*\});\s*\n\s*export", read(SIDEBARS), re.S)
    if not m:
        sys.exit(f"{SIDEBARS}: objeto do sidebar não encontrado")
    try:
        return json.loads(m.group(1))
    except json.JSONDecodeError as e:
        sys.exit(f"{SIDEBARS}: o objeto precisa ser JSON válido ({e})")


def catalog_entry(d):
    """Sidebar category of catalog d ('<domínio>/<catálogo>')."""
    for dom in load_sidebar()["catalog"]:
        if not isinstance(dom, dict):
            continue
        for cat in dom.get("items", []):
            if cat.get("link", {}).get("id") == f"{d}/index":
                return cat
    sys.exit(f"{d}: catálogo não encontrado no {SIDEBARS} (link.id = '{d}/index')")


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
        sys.exit(f"{path}: escreva antes o cabeçalho (frontmatter, título, introdução e linha Total)")
    current = read(path)
    if L["groups"] not in current:
        sys.exit(f"{path}: falta a seção '{L['groups']}' que marca o fim do cabeçalho")
    head = current.split("\n" + L["groups"], 1)[0].rstrip() + "\n"
    groups = catalog_items(d)
    n = sum(len(i) for _, _, i in groups)
    head, k = re.subn(L["total_re"], L["total"].format(n=n, g=len(groups)), head, count=1, flags=re.M)
    if not k:
        sys.exit(f"{path}: falta a linha 'Total' no cabeçalho")

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
    print(f"{path} gerado")


def cmd_index(d):
    for root in (PT, EN):
        render_index(d, root)


# ---------------------------------------------------------------- validate
def cmd_validate(d):
    errs, warns = [], []
    groups = catalog_items(d)
    total = sum(len(i) for _, _, i in groups)
    sidebar_docs = {it["doc"] for _, _, items in groups for it in items if not it["shared"]}

    for root in (PT, EN):
        if not os.path.exists(f"{root}/{d}/index.md"):
            errs.append(f"{root}/{d}/index.md: não existe")

    for gslug, gname, items in groups:
        for it in items:
            if it["shared"]:
                real = doc_file(PT, it["url"])
                if not real:
                    errs.append(f"sidebar {d}/{gslug}: padrão compartilhado aponta para {it['url']}, que não existe")
                elif f"{d}/{gslug}" not in fm_list(read(real), "also_in"):
                    errs.append(f"{real}: falta also_in '{d}/{gslug}'")
                continue
            for root in (PT, EN):
                f = doc_file(root, it["url"])
                if not f:
                    errs.append(f"{root}{it['url']}.md: não existe")
                    continue
                t = read(f)
                if fm_field(t, "category") != gname:
                    errs.append(f"{f}: category != '{gname}'")
                for key in ("title", "pattern_slug", "source", "sidebar_label"):
                    if not fm_field(t, key):
                        errs.append(f"{f}: falta '{key}' no frontmatter")
                if not fm_list(t, "tags"):
                    errs.append(f"{f}: falta 'tags' no frontmatter")
                for s in LANGS[root]["sections"]:
                    if not re.search("^" + re.escape(s) + r"\s*$", t, re.M):
                        errs.append(f"{f}: falta seção '{s}'")
                if "```mermaid" not in t:
                    errs.append(f"{f}: falta bloco mermaid")

            pt_f, en_f = doc_file(PT, it["url"]), doc_file(EN, it["url"])
            if pt_f and en_f:
                pt, en = read(pt_f), read(en_f)
                if split_fm(pt)[0] != split_fm(en)[0]:
                    errs.append(f"{en_f}: frontmatter diferente do pt-BR")
                links = lambda t: sorted(re.findall(r"\]\(([^)\s]+)\)", t))
                if links(pt) != links(en):
                    errs.append(f"{en_f}: links diferentes do pt-BR {sorted(set(links(pt)) ^ set(links(en)))}")
                heads = lambda t: len(re.findall(r"^#+ ", t, re.M))
                if heads(pt) != heads(en):
                    errs.append(f"{en_f}: {heads(en)} títulos, pt-BR tem {heads(pt)}")
                if pt.count("```") != en.count("```"):
                    errs.append(f"{en_f}: número de blocos de código diferente do pt-BR")
                ratio = len(en.split()) / max(1, len(pt.split()))
                if not 0.8 <= ratio <= 1.25:
                    warns.append(f"{en_f}: tamanho {ratio:.2f}x o pt-BR (trecho faltando ou sobrando?)")
                body = re.sub(r"\]\([^)]*\)|https?://\S+", "", split_fm(en)[1])
                if ACCENTS.search(body):
                    errs.append(f"{en_f}: caracteres acentuados (português no texto em inglês?)")

    # arquivos fora do sidebar e links internos
    for root in (PT, EN):
        for f in sorted(p for p in (os.path.join(r, x) for r, _, fs in os.walk(f"{root}/{d}") for x in fs)
                        if p.endswith(".md")):
            rel = f[len(root) + 1:-3]
            if not rel.endswith("/index") and rel not in sidebar_docs:
                errs.append(f"{f}: não está no {SIDEBARS}")
            for link in re.findall(r"\]\(([^)\s#]+)(?:#[^)]*)?\)", read(f)):
                if link.endswith(".md") or link.endswith(".mdx"):
                    errs.append(f"{f}: link relativo '{link}' (use a URL absoluta da página)")
                elif link.startswith("/") and not link.startswith("/tags/") and not doc_file(PT, link):
                    errs.append(f"{f}: link quebrado '{link}'")

    # card da home
    cards = [c for c in json.loads(read(CARDS))["catalogs"] if c["href"] == f"/{d}"]
    if not cards:
        errs.append(f"{CARDS}: falta o card de /{d}")
    elif (cards[0]["patterns"], cards[0]["groups"]) != (total, len(groups)):
        errs.append(f"{CARDS}: card de /{d} diz {cards[0]['patterns']} padrões/{cards[0]['groups']} grupos; "
                    f"o sidebar tem {total}/{len(groups)}")

    print(f"{d}: {total} padrões em {len(groups)} grupos")
    for w in warns:
        print("aviso:", w)
    print("\n".join(errs) if errs else "OK, nenhum erro")
    return 1 if errs else 0


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] not in ("validate", "index"):
        print(__doc__)
        sys.exit(2)
    target = sys.argv[2].strip("/")
    sys.exit((cmd_validate if sys.argv[1] == "validate" else cmd_index)(target) or 0)
