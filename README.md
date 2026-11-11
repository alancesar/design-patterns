# Design Patterns

A personal catalog of design patterns in wiki format, published at **https://designpatterns.alancesar.dev**.

Built with [Docusaurus](https://docusaurus.io). It uses the visual identity of [alancesar.dev](https://alancesar.dev): Catppuccin Latte/Mocha, a mauve accent and JetBrains Mono for code. Deployed on [Netlify](https://www.netlify.com).

## Content

The patterns are Markdown files in `docs/`, organized as domain → catalog → group → pattern (`docs/<domain>/<catalog>/<group>/<pattern>.md`). Each pattern has a description, the problems it solves, when to use it and when to avoid it, trade-offs, tags, a Mermaid diagram and related patterns. Many also have a code example. `sidebars.ts` defines the navigation, and `src/data/catalogs.json` feeds the catalog cards on the home page.

The site is bilingual. Portuguese (pt-BR) is the default locale, and English is served under `/en/`. English pages live in `i18n/en/docusaurus-plugin-content-docs/current/`, at the same paths as their counterparts under `docs/`, and English UI strings are in `i18n/en/` (`code.json`, `docusaurus-theme-classic/` and `docusaurus-plugin-content-docs/current.json`).

The examples share one scenario: a fictional Brazilian fintech with a digital account, Pix, boleto, cards, personal credit and fixed-income investments. Class names such as `Account`, `Money` and `LedgerEntry` are reused across pages, so an example in one catalog reads as part of the same system as the others.

### Adding new catalogs

New catalogs are added in both languages in the same PR: each page in `docs/` gets its English version in `i18n/en/docusaurus-plugin-content-docs/current/`, and `npm run build` must pass for both locales. A page without an English version falls back to the Portuguese content under `/en/`.

## Development

```bash
npm install
npm start          # local dev server at http://localhost:3000 (pt-BR only; add `-- --locale en` for English)
npm run build      # production build to build/ (fails on broken links)
npm run serve      # serves the build locally (needed to test search)
npm run typecheck
```
