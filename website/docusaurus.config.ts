import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

const config: Config = {
  title: 'Iris Agent',
  tagline: 'The self-improving AI agent',
  favicon: 'img/favicon.ico',

  url: 'https://iris-agent.Metaxis Research.com',
  baseUrl: '/docs/',

  organizationName: 'Metaxis Research',
  projectName: 'iris-agent',

  onBrokenLinks: 'warn',

  markdown: {
    hooks: {
      onBrokenMarkdownLinks: 'warn',
    },
  },

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  themes: [
    [
      require.resolve('@easyops-cn/docusaurus-search-local'),
      /** @type {import("@easyops-cn/docusaurus-search-local").PluginOptions} */
      ({
        hashed: true,
        language: ['en'],
        indexBlog: false,
        docsRouteBasePath: '/',
        highlightSearchTermsOnTargetPage: true,
      }),
    ],
  ],

  presets: [
    [
      'classic',
      {
        docs: {
          routeBasePath: '/',  // Docs at the root of /docs/
          sidebarPath: './sidebars.ts',
          editUrl: 'https://github.com/Metaxis Research/iris-agent/edit/main/website/',
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    image: 'img/iris-agent-banner.png',
    colorMode: {
      defaultMode: 'dark',
      respectPrefersColorScheme: true,
    },
    navbar: {
      title: 'Iris Agent',
      logo: {
        alt: 'Iris Agent',
        src: 'img/logo.png',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'docs',
          position: 'left',
          label: 'Docs',
        },
        {
          href: 'https://iris-agent.Metaxis Research.com',
          label: 'Home',
          position: 'right',
        },
        {
          href: 'https://github.com/Metaxis Research/iris-agent',
          label: 'GitHub',
          position: 'right',
        },
        {
          href: 'https://discord.gg/Metaxis Research',
          label: 'Discord',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Docs',
          items: [
            { label: 'Getting Started', to: '/getting-started/quickstart' },
            { label: 'User Guide', to: '/user-guide/cli' },
            { label: 'Developer Guide', to: '/developer-guide/architecture' },
            { label: 'Reference', to: '/reference/cli-commands' },
          ],
        },
        {
          title: 'Community',
          items: [
            { label: 'Discord', href: 'https://discord.gg/Metaxis Research' },
            { label: 'GitHub Discussions', href: 'https://github.com/Metaxis Research/iris-agent/discussions' },
            { label: 'Skills Hub', href: 'https://agentskills.io' },
          ],
        },
        {
          title: 'More',
          items: [
            { label: 'GitHub', href: 'https://github.com/Metaxis Research/iris-agent' },
            { label: 'Metaxis Research', href: 'https://Metaxis Research.com' },
          ],
        },
      ],
      copyright: `Built by <a href="https://Metaxis Research.com">Metaxis Research</a> · MIT License · ${new Date().getFullYear()}`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
      additionalLanguages: ['bash', 'yaml', 'json', 'python', 'toml'],
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
