import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';
import {catppuccinLatte, catppuccinMocha} from './src/prism/catppuccin';

const domains = [
  {slug: 'coding', label: 'Coding'},
  {slug: 'design', label: 'Design'},
  {slug: 'architecture', label: 'Architecture'},
  {slug: 'ai', label: 'AI'},
];

// Docusaurus sets this before loading the config for each locale (build and start).
const locale = process.env.DOCUSAURUS_CURRENT_LOCALE === 'en' ? 'en' : 'pt-BR';
const year = new Date().getFullYear();

const TAGLINE = {
  'pt-BR': 'Catálogo pessoal de design patterns, por domínio e catálogo.',
  en: 'A personal catalog of design patterns, by domain and catalog.',
};

// Kept here (not in i18n/en/.../footer.json) so the year stays dynamic in both locales.
// If `write-translations` adds a "copyright" key back to the English footer.json, delete it.
const COPYRIGHT = {
  'pt-BR': `Resumos escritos por Alan Cesar. Os padrões pertencem aos seus autores originais; veja o link da fonte em cada página.<br/>© ${year} Alan Cesar. Conteúdo sob <a href="https://creativecommons.org/licenses/by/4.0/deed.pt-br" target="_blank" rel="noopener noreferrer">CC BY 4.0</a>, código sob MIT. Feito com Docusaurus.`,
  en: `Summaries written by Alan Cesar. The patterns belong to their original authors; see the source link on each page.<br/>© ${year} Alan Cesar. Content under <a href="https://creativecommons.org/licenses/by/4.0/" target="_blank" rel="noopener noreferrer">CC BY 4.0</a>, code under MIT. Built with Docusaurus.`,
};

const config: Config = {
  title: 'Design Patterns',
  tagline: TAGLINE[locale],
  favicon: 'img/logo.svg',

  url: 'https://designpatterns.alancesar.dev',
  baseUrl: '/',
  trailingSlash: false,

  onBrokenLinks: 'throw',
  onBrokenAnchors: 'warn',

  future: {
    v4: true,
    faster: true,
  },

  i18n: {
    defaultLocale: 'pt-BR',
    locales: ['pt-BR', 'en'],
    localeConfigs: {
      'pt-BR': {label: 'Português', htmlLang: 'pt-BR'},
      en: {label: 'English', htmlLang: 'en'},
    },
  },

  markdown: {
    format: 'detect',
    mermaid: true,
    hooks: {
      onBrokenMarkdownLinks: 'throw',
    },
  },

  themes: [
    '@docusaurus/theme-mermaid',
    [
      require.resolve('@easyops-cn/docusaurus-search-local'),
      {
        hashed: true,
        indexBlog: false,
        docsRouteBasePath: '/',
        language: ['pt', 'en'],
        highlightSearchTermsOnTargetPage: true,
        explicitSearchResultPath: true,
      },
    ],
  ],

  presets: [
    [
      'classic',
      {
        docs: {
          routeBasePath: '/',
          sidebarPath: './sidebars.ts',
          onInlineTags: 'ignore',
          showLastUpdateTime: false,
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
        sitemap: {
          changefreq: 'weekly',
          priority: 0.5,
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    docs: {
      sidebar: {
        hideable: true,
        autoCollapseCategories: false,
      },
    },
    colorMode: {
      respectPrefersColorScheme: true,
    },
    navbar: {
      title: 'Design Patterns',
      logo: {alt: 'Design Patterns', src: 'img/logo.svg'},
      items: [
        // activeBaseRegex never matches: an "active" navbar item would be prefixed to
        // every search-result breadcrumb ("Cloud › Cloud › Cloud Design Patterns …").
        ...domains.map((d) => ({to: `/${d.slug}`, label: d.label, position: 'left' as const, activeBaseRegex: '^$'})),
        {to: '/tags', label: 'Etiquetas', position: 'left'},
        {type: 'localeDropdown', position: 'right'},
        {href: 'https://alancesar.dev', label: 'alancesar.dev', position: 'right'},
        {href: 'https://github.com/alancesar/design-patterns', label: 'GitHub', position: 'right'},
      ],
    },
    footer: {
      links: [
        {
          title: 'Catálogos',
          items: [
            {label: 'GoF', to: '/coding/gof'},
            {label: 'PoEAA', to: '/design/poeaa'},
            {label: 'Domain-Driven Design', to: '/design/ddd'},
            {label: 'Enterprise Integration Patterns', to: '/architecture/eip'},
            {label: 'Microservices', to: '/architecture/microservices'},
            {label: 'Patterns of Distributed Systems', to: '/architecture/distributed-systems'},
            {label: 'Cloud Design Patterns', to: '/architecture/cloud-design-patterns'},
            {label: 'AI Agent Design Patterns', to: '/ai/agent-patterns'},
          ],
        },
        {
          title: 'Fontes',
          items: [
            {label: 'Design Patterns Cheat Sheet', href: 'https://iretha.github.io/design-patterns/cheat-sheet'},
            {label: 'Catalog of PoEAA', href: 'https://martinfowler.com/eaaCatalog/'},
            {label: 'DDD Reference', href: 'https://www.domainlanguage.com/ddd/reference/'},
            {label: 'Enterprise Integration Patterns', href: 'https://www.enterpriseintegrationpatterns.com/patterns/messaging/'},
            {label: 'microservices.io', href: 'https://microservices.io/patterns/'},
            {label: 'Patterns of Distributed Systems', href: 'https://martinfowler.com/articles/patterns-of-distributed-systems/'},
            {label: 'Azure Architecture Center', href: 'https://learn.microsoft.com/en-us/azure/architecture/patterns/'},
            {label: 'Azure Architecture Center (AI agents)', href: 'https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns'},
            {label: 'Google Cloud Architecture Center', href: 'https://docs.cloud.google.com/architecture/choose-design-pattern-agentic-ai-system'},
          ],
        },
        {
          title: 'Alan Cesar',
          items: [
            {label: 'alancesar.dev', href: 'https://alancesar.dev'},
            {label: 'GitHub', href: 'https://github.com/alancesar'},
            {label: 'LinkedIn', href: 'https://www.linkedin.com/in/alancesar/'},
          ],
        },
      ],
      copyright: COPYRIGHT[locale],
    },
    prism: {
      theme: catppuccinLatte,
      darkTheme: catppuccinMocha,
      additionalLanguages: ['bash', 'java', 'csharp', 'sql'],
    },
    mermaid: {
      theme: {light: 'neutral', dark: 'dark'},
      options: {
        fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif',
      },
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
