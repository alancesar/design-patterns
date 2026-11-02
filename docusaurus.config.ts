import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';
import {catppuccinLatte, catppuccinMocha} from './src/prism/catppuccin';

const domains = [
  {slug: 'coding', label: 'Coding'},
  {slug: 'application', label: 'Application'},
  {slug: 'architecture', label: 'Architecture'},
  {slug: 'cloud', label: 'Cloud'},
];

const config: Config = {
  title: 'Design Patterns',
  tagline: 'Catálogo pessoal de design patterns, por domínio e catálogo.',
  favicon: 'img/logo.svg',

  url: 'https://designpatterns.alancesar.org',
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
    locales: ['pt-BR'],
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
        // every search-result breadcrumb ("Cloud › Cloud › Azure …").
        ...domains.map((d) => ({to: `/${d.slug}`, label: d.label, position: 'left' as const, activeBaseRegex: '^$'})),
        {to: '/tags', label: 'Etiquetas', position: 'left'},
        {href: 'https://alancesar.dev', label: 'alancesar.dev', position: 'right'},
        {href: 'https://github.com/alancesar/designpatterns', label: 'GitHub', position: 'right'},
      ],
    },
    footer: {
      links: [
        {
          title: 'Catálogos',
          items: [
            {label: 'GoF', to: '/coding/gof'},
            {label: 'PoEAA', to: '/application/poeaa'},
            {label: 'Domain-Driven Design', to: '/application/ddd'},
            {label: 'Microservices', to: '/architecture/microservices'},
            {label: 'Cloud Design Patterns', to: '/cloud/azure'},
          ],
        },
        {
          title: 'Fontes',
          items: [
            {label: 'Design Patterns Cheat Sheet', href: 'https://iretha.github.io/design-patterns/cheat-sheet'},
            {label: 'Catalog of PoEAA', href: 'https://martinfowler.com/eaaCatalog/'},
            {label: 'DDD Reference', href: 'https://www.domainlanguage.com/ddd/reference/'},
            {label: 'microservices.io', href: 'https://microservices.io/patterns/'},
            {label: 'Azure Architecture Center', href: 'https://learn.microsoft.com/en-us/azure/architecture/patterns/'},
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
      copyright: `© ${new Date().getFullYear()} Alan Cesar. Feito com Docusaurus.`,
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
