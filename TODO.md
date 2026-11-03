# Translation TODO

English translation of the site (pt-BR is the default locale). English pages live in
`i18n/en/docusaurus-plugin-content-docs/current/`, mirroring the paths under `docs/`;
untranslated pages fall back to the Portuguese content under `/en/`.

Progress: **307 of 307** (complete) pattern pages translated.

## Catalogs

| Status | Domain | Catalog | Path | Patterns | Groups | Pending groups |
| --- | --- | --- | --- | --- | --- | --- |
| ✅ Done | Coding | Design Patterns (GoF and classics) | `coding/gof` | 28/28 | 3 | — |
| ✅ Done | AI | AI Agent Orchestration Patterns | `ai/agent-orchestration` | 6/6 | 2 | — |
| ✅ Done | AI | Agentic AI Design Patterns | `ai/agentic-ai` | 9/9 | 3 | — |
| ✅ Done | Application | Domain-Driven Design | `application/ddd` | 41/41 | 6 | — |
| ✅ Done | Cloud | Cloud Design Patterns | `cloud/cloud-design-patterns` | 44/44 | 8 | — |
| ✅ Done | Architecture | Enterprise Integration Patterns | `architecture/eip` | 56/56 | 7 | — |
| ✅ Done | Architecture | Patterns of Distributed Systems | `architecture/distributed-systems` | 29/29 | 5 | — |
| ✅ Done | Application | Patterns of Enterprise Application Architecture | `application/poeaa` | 51/51 | 10 | — |
| ✅ Done | Architecture | Microservices Patterns | `architecture/microservices` | 43/43 | 13 | — |

## Other pages

| Status | Page | Path |
| --- | --- | --- |
| ✅ Done | Home page | `index.mdx` |
| ✅ Done | Coding domain page | `coding/index.md` |
| ✅ Done | Application domain page | `application/index.md` |
| ✅ Done | Architecture domain page | `architecture/index.md` |
| ✅ Done | Cloud domain page | `cloud/index.md` |
| ✅ Done | AI domain page | `ai/index.md` |

## UI strings

- ✅ Navbar, footer, and home-page catalog cards (`i18n/en/code.json`, `i18n/en/docusaurus-theme-classic/`).
- ✅ Sidebar labels (`i18n/en/docusaurus-plugin-content-docs/current.json`; already in English).

## Adding new catalogs

New catalogs are added in both languages in the same PR: each page in `docs/` gets its English version in `i18n/en/docusaurus-plugin-content-docs/current/`, and `npm run build` must pass for both locales.
