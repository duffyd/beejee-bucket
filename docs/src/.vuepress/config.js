const { config } = require("vuepress-theme-hope");

module.exports = config({
  title: 'BeeJee Bucket',
  description: 'Filing my study notes',
  host: process.env.DEBUG ? '0.0.0.0' : 'localhost',
  themeConfig: {
    nav: [
      {
        text: 'Tags',
        link: '/tag/'
      }
    ],
    sidebar: 'auto',
    sidebarDepth: 2,
    sitemap: false,
    hostname: 'bj.kokorice.org',
  },
  plugins: [
    '@vuepress/plugin-back-to-top',
    '@vuepress/plugin-medium-zoom',
    'fulltext-search'
  ]
});
