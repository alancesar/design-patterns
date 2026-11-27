---
name: pattern-catalog
description: Adds a new design-patterns catalog to the Docusaurus site, in pt-BR and English (one page per pattern, the catalog page, sidebar, home cards and home page). Use when the user asks to add, import or document a catalog of patterns, or to review the structure of an existing catalog.
---

# Add a design-patterns catalog

The site has two locales: **pt-BR** (the default, served at `/`) and **English** (served at `/en/`). Every new catalog is published in both locales in the same PR. Follow the steps in order. Some steps need the user's decision: don't skip the questions in step 1.

The hierarchy is **domain → catalog → group → pattern**. In the examples below, `<dir>` is `<domain>/<catalog>`, for example `design/poeaa`.

## Where everything lives

| What | pt-BR | English |
| --- | --- | --- |
| Pattern page | `docs/<dir>/<group>/<slug>.md` | `i18n/en/docusaurus-plugin-content-docs/current/<dir>/<group>/<slug>.md` |
| Catalog page | `docs/<dir>/index.md` | `i18n/en/.../current/<dir>/index.md` |
| Domain page | `docs/<domain>/index.md` | `i18n/en/.../current/<domain>/index.md` |
| Home page (catalog table) | `docs/index.mdx` | `i18n/en/.../current/index.mdx` |
| Structure: groups, order, shared patterns | `sidebars.ts` (shared by both locales) | — |
| Home-page cards | `src/data/catalogs.json` | translated title in `i18n/en/code.json` (`catalogCards.title.<href>`), if the title isn't in English |
| Footer and navbar | `docusaurus.config.ts` | `i18n/en/docusaurus-theme-classic/footer.json` and `navbar.json` |
| Tags (label, permalink, description) | `docs/tags.yml` | `i18n/en/docusaurus-plugin-content-docs/current/tags.yml` |

Helper script: `.claude/skills/pattern-catalog/scripts/catalog.py`. Run it from the repository root with `python3 -I`. Subcommands:

- `validate <dir>`: checks files, frontmatter, sections, tags declared in both `tags.yml` files, the Java/Python/Go tab order, the shared diagram (it exists, is in English and is imported the same way in both locales), links, pt-BR/English parity, the sidebar and the home-page card.
- `index <dir>`: regenerates the catalog page tables in both locales from `sidebars.ts` and the patterns' frontmatter.

`sidebars.ts` is the source of truth for the structure, and the script reads it as JSON: keep the object valid JSON (double quotes, no trailing commas, no comments inside it).

## 1. Survey and decisions (with the user)

1. Read the source's index page (with WebFetch; if the session has no direct WebFetch, use the `web-fetch` agent) and list every pattern, with its name and URL, grouped the way the source groups them.
2. Pick the catalog's **domain** by its main focus:
   - `coding`: classes and objects.
   - `design`: domain modeling and the application's internal structure.
   - `architecture`: system and cloud architecture (architectural styles, distribution, integration, consistency, concurrency, and running on cloud and containers).
   - `ai`: systems built on LLMs and AI agents.
   - Create a new domain only with the user's approval.
3. Propose a **partition into groups** where each pattern is in exactly one group. Prefer the source's own groups. Group names in English; slugs in kebab-case.
4. Find **overlaps** with existing catalogs by comparing against the titles and `pattern_slug` in `docs/*/*/*/*.md` and against `sidebars.ts`. Classify each case:
   - **same pattern**: it becomes a shared link in the sidebar (★), and the existing file is revised;
   - **similar but distinct**: it becomes a new pattern, linked from "Related patterns".
5. Define the **tags**, which are multi-valued and span groups:
   - Reuse an existing set when it fits (see the `tags` of similar catalogs). The Well-Architected pillars (Reliability, Security, Cost Optimization, Operational Excellence, Performance Efficiency) fit architecture and service patterns; the GoF design goals fit code patterns.
   - If none fits, propose a new set of 5 to 7 tags, in English, with the expected distribution.
   - Every tag must exist in `docs/tags.yml` and in the English `tags.yml`. Because the site sets `onInlineTags: 'ignore'`, the build doesn't flag a missing tag: it just renders without a description.
6. Use **AskUserQuestion** to confirm the domain (if in doubt), the tags and any ambiguous overlaps. Recommend one option in each question.
7. For large catalogs, write a short plan (domain, groups, counts and overlaps) and get approval before creating files.

## 2. Setup (you, no subagents)

1. Create a branch from an up-to-date `main`. The PR goes straight to `main`; don't stack PRs on other branches.
2. Create `docs/<dir>/<group>/` and `i18n/en/docusaurus-plugin-content-docs/current/<dir>/<group>/` for each group.
3. Write the catalog page **header** in both locales. The `index` script fills in the rest later. Use an existing catalog page as the model (`docs/architecture/cloud-design-patterns/index.md` and its English version):
   - frontmatter with `title` and `sidebar_label`;
   - `# <Catalog name>`;
   - an introduction: the source (with a link), what each pattern page covers and what the tags represent;
   - if there are shared patterns, the note about ★ (copy the sentence from a catalog that already has it);
   - the line `Total: 0 padrões em 0 grupos. Etiquetas: <rótulo>.` (in English: `Total: 0 patterns in 0 groups. Tags: <label>.`). The script fixes the numbers;
   - last, the heading `## Grupos` (in English: `## Groups`), which marks the end of the header.
4. Add the catalog to **`sidebars.ts`**, inside its domain, following the format of the existing catalogs:
   - a catalog category with `key: "<slug>"`, a short `label` and `link: {"type": "doc", "id": "<dir>/index"}`;
   - one category per group, with `label` (the group name), `key: "<slug>-<group>"` and `collapsed: true`;
   - each new pattern is its document id: `"<dir>/<group>/<slug>"`;
   - each shared pattern is a link: `{"type": "link", "label": "<name in this source>", "href": "/<path of the original document>?catalog=<slug>", "className": "sidebar-shared", "key": "<slug>-<pattern-slug>"}`.
5. Add the **card** to `src/data/catalogs.json` (`domain`, `domainLabel`, `title`, `href: "/<dir>"`, `source`, `patterns` = the sidebar total, shared links included, and `groups`). If the `title` isn't in English, add `catalogCards.title./<dir>` to `i18n/en/code.json`.
6. Register the **new tags** in `docs/tags.yml` (pt-BR description) and in `i18n/en/docusaurus-plugin-content-docs/current/tags.yml` (English description), with the same `label` and `permalink` (`/<tag-in-kebab-case>`) and in the same alphabetical order.
7. Update the **domain page** (catalog list) and the **home page** (catalog table) in both locales. Update the footer in `docusaurus.config.ts` (catalogs and sources) and the English `footer.json`. A new domain also needs a navbar item (`domains` in `docusaurus.config.ts`), a domain page in both locales and an entry in the home page's domain list.

## 3. Content: one subagent PER GROUP, in both locales

- Launch **one `general-purpose` subagent per group**, all in the same message, in parallel, with **`model: "sonnet"`**.
  - Sonnet is enough for structured technical writing and fixed-format translation, and costs much less than Opus. Use Opus only if the user asks.
  - At most 20 subagents run at once. If there are more groups, launch the rest as the first ones finish.
  - Don't create one subagent per pattern: that blows through the usage limit.
  - If the user asks for a specific number of subagents, do as asked.
- Each subagent writes the pt-BR version of each pattern first and then the English one, saving each file as soon as it's done (if interrupted, it resumes from the files that already exist).
- Each subagent's prompt must include:
  - the repository path and the branch, and a ban on git commands that change state;
  - the group's pattern list: pt-BR path, English path, source URL, and whether it's NEW or EXISTING (with the existing file's real path);
  - a published pattern as a model, in both locales (e.g. `docs/architecture/cloud-design-patterns/resiliency/retry.md` and its English version; for code examples, `docs/coding/gof/behavioral/strategy.md`);
  - the allowed tags and the exact `category` value (the group name);
  - the list of valid link URLs (the existing pages plus the catalog's new ones).
- Rules the prompt must pass on:
  - Load WebFetch through `ToolSearch` (`select:WebFetch`) and read each pattern's page.
  - **Frontmatter**, identical in both locales: `title`, `pattern_slug`, `category`, `tags`, `source` and `sidebar_label` (quoted). `origin` and `also_in` when they apply. No `**Etiquetas:**` or `**Categoria:**` lines in the body: the site already shows the tags and the group.
  - **Sections** in pt-BR: Descrição, Problemas que resolve, Quando usar, Quando evitar, Trade-offs (a `| Ganho | Custo / Risco |` table and bold bullets), Diagrama, Exemplo (when the source has code or a scenario), Padrões relacionados and Referência. In English: Description, Problems it solves, When to use, When to avoid, Trade-offs (`| Benefit | Cost / Risk |`), Diagram, Example, Related patterns and Reference.
  - pt-BR text in Portuguese; pattern names, the category, tags and code identifiers stay in English. The English version is a faithful translation of the pt-BR one, adding and omitting nothing, with the same sections, links and code blocks.
  - **Mermaid diagram in English, single source**: save the ` ```mermaid ` block to `docs/_diagrams/<dir>/<group>/<slug>.mdx` (a second diagram on the same page goes to `<slug>-2.mdx`). Labels, participants, notes and `%%` comments in English, with no accents and no HTML; in a `flowchart`, labels with parentheses or punctuation go in double quotes. Both versions of the page import the same file right after the frontmatter (`import Diagram from '@site/docs/_diagrams/<dir>/<group>/<slug>.mdx';`) and render it with `<Diagram />` in the Diagrama/Diagram section. Never leave an inline `mermaid` block on the page. The frontmatter needs `mdx:` / `  format: mdx`.
  - **Internal links** are always the page's absolute URL, without `.md`: `/<domain>/<catalog>/<group>/<slug>`. Never relative links to `.md` files: Docusaurus can't resolve a `.md` link between a translated and an untranslated page. The same URL works in both locales, because Docusaurus adds `/en` on its own. Tags: `/tags/<tag-in-kebab-case>`.
  - **Code examples**: always in Java, Python and Go, in `<Tabs groupId="lang" queryString>` with one `<TabItem value="java|python|go" label="Java|Python|Go">` per language, in that order, each wrapping a code block with blank lines around it. The page needs `mdx:` / `  format: mdx` in its frontmatter (every pattern page already has it, because of the imported diagram); `Tabs` and `TabItem` are global, with no import. All three versions show the same scenario, values and output, each one idiomatic (in Go: interfaces, composition and `error` returns, with a one-line comment when the pattern takes a different shape). Every snippet must compile and run (Python compatible with 3.9). SQL blocks shared by all languages stay outside the tabs. Identifiers and structure are the same in both locales; translate only comments and user-facing strings. Model: `docs/coding/gof/behavioral/strategy.md`.
  - **Fintech scenario**: the Example and any diagram showing a concrete implementation use the site's fictional Brazilian fintech (digital account, Pix, boleto, cards, personal credit, fixed income) and reuse the class names from other pages (`Account`, `Money`, `LedgerEntry`, `PixCharge`, `LoanContract`, `Card`). Diagrams that show only the pattern's roles stay generic. Money is never a float (use `Money` or integer cents), a reversal is a new ledger entry, and rates, limits and fees are illustrative.
  - **EXISTING patterns**:
    - edit the real file in both locales, revising it against the new source, without rewriting it from scratch;
    - don't change `title`, `pattern_slug`, `category` or `tags`;
    - add `also_in:` with `- <dir>/<group>` before `source:`, in both locales;
    - add the source link under "Referência" / "Reference".
  - Edit only the group's own files.
  - Final answer: one `ok: <path>` line per file, plus a summary of the revision for existing ones.
- While the agents run, report progress in one line per finished group.
- If the usage limit is hit, resume the interrupted agents with `SendMessage` instead of creating new ones. They should reread their own files and finish what's missing.

## 4. Indexes, validation and build

```bash
python3 -I .claude/skills/pattern-catalog/scripts/catalog.py index <dir>
python3 -I .claude/skills/pattern-catalog/scripts/catalog.py validate <dir>
npm run build
```

- `index` builds the per-group tables (summary = the first sentence of each pattern's Descrição/Description) and the by-tag section, and fixes the `Total` line.
- `validate` checks, among other things, that the English version has the same frontmatter, links, number of headings and number of code blocks as the pt-BR one, and that the English text has no accents. It also warns when the translation's length falls outside 0.8–1.25x the original, a sign of a missing passage: open the file and check.
- The build generates both locales and fails on broken links (`onBrokenLinks: 'throw'`).
- Fix the errors (yourself, or by resuming the group's subagent) until everything passes. If an existing file was revised, also run `index` and `validate` on the catalog that owns it.

## 5. Wrap-up

- Update the root `README.md` if it mentions the catalogs.
- Commit only the site's files. The versioned skills live in `.claude/skills/`, but the rest of `.claude/` (`settings.local.json`, `launch.json` and other local skills) stays local through `.git/info/exclude`: check in `git status` that none of it got in.
- Commit following the history's style (`git log`): one commit for the new catalog and another for revisions to existing catalogs, if any.
- Open the PR against `main`.
- Report to the user:
  - what was created and revised, in both locales;
  - the results of `validate` and the build;
  - that no person has read the content yet, so a quick review of `/<dir>` and `/en/<dir>` is worth it.
