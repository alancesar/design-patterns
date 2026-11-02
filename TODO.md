# Translation TODO

English translation of the site (pt-BR is the default locale). English pages live in
`i18n/en/docusaurus-plugin-content-docs/current/`, mirroring the paths under `docs/`;
untranslated pages fall back to the Portuguese content under `/en/`.

Progress: **43 of 307** pattern pages translated.

## Catalogs

| Status | Domain | Catalog | Path | Patterns | Groups | Pending groups |
| --- | --- | --- | --- | --- | --- | --- |
| ✅ Done | Coding | Design Patterns (GoF and classics) | `coding/gof` | 28/28 | 3 | — |
| ✅ Done | AI | AI Agent Orchestration Patterns | `ai/agent-orchestration` | 6/6 | 2 | — |
| ✅ Done | AI | Agentic AI Design Patterns | `ai/agentic-ai` | 9/9 | 3 | — |
| ⬜ Pending | Application | Patterns of Enterprise Application Architecture | `application/poeaa` | 0/51 | 10 | `base`, `data-source-architectural`, `distribution`, `domain-logic`, `object-relational-behavioral`, `object-relational-metadata-mapping`, `object-relational-structural`, `offline-concurrency`, `session-state`, `web-presentation` |
| ⬜ Pending | Application | Domain-Driven Design | `application/ddd` | 0/41 | 6 | `building-blocks`, `context-mapping`, `distillation`, `large-scale-structure`, `model-in-practice`, `supple-design` |
| ⬜ Pending | Architecture | Microservices Patterns | `architecture/microservices` | 0/43 | 13 | `architectural-style`, `communication-styles`, `cross-cutting-concerns`, `deployment`, `external-api`, `observability`, `security`, `service-boundaries`, `service-collaboration`, `service-discovery`, `testing`, `transactional-messaging`, `ui-design` |
| ⬜ Pending | Architecture | Enterprise Integration Patterns | `architecture/eip` | 0/56 | 7 | `integration-styles`, `message-construction`, `message-routing`, `message-transformation`, `messaging-channels`, `messaging-endpoints`, `system-management` |
| ⬜ Pending | Architecture | Patterns of Distributed Systems | `architecture/distributed-systems` | 0/29 | 5 | `cluster-management`, `data-partitioning`, `data-replication`, `distributed-time`, `node-communication` |
| ⬜ Pending | Cloud | Cloud Design Patterns | `cloud/cloud-design-patterns` | 0/44 | 8 | `data-management`, `deployment-and-topology`, `distributed-coordination`, `gateways-and-edge`, `integration-and-modernization`, `messaging`, `resiliency`, `security-and-access` |

## Other pages

| Status | Page | Path |
| --- | --- | --- |
| ✅ Done | Home page | `index.mdx` |
| ✅ Done | Coding domain page | `coding/index.md` |
| ⬜ Pending | Application domain page | `application/index.md` |
| ⬜ Pending | Architecture domain page | `architecture/index.md` |
| ⬜ Pending | Cloud domain page | `cloud/index.md` |
| ✅ Done | AI domain page | `ai/index.md` |

## UI strings

- ✅ Navbar, footer, and home-page catalog cards (`i18n/en/code.json`, `i18n/en/docusaurus-theme-classic/`).
- ✅ Sidebar labels (`i18n/en/docusaurus-plugin-content-docs/current.json`; already in English).

## How to translate a catalog

1. One subagent per pattern group (Sonnet), writing to `i18n/en/docusaurus-plugin-content-docs/current/<same path>`.
2. Prose comes from `docs/<path>`; Mermaid blocks are copied verbatim from the `docs/english-mermaid-diagrams` branch (PR #1).
3. Keep frontmatter and every link URL unchanged; links are absolute doc URLs, so Docusaurus adds `/en` automatically.
4. Write the catalog `index.md` and its domain page, using each translated pattern's first Description sentence as its summary.
5. Verify with `npm run build` (both locales; broken links fail the build) and update this file.
