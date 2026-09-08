import { defineConfig } from 'astro/config';

// Static site — outputs plain HTML/CSS/JS into ./dist, which Cloudflare Pages
// (or any static host) serves for free. No server, no database.
export default defineConfig({
  output: 'static',
  // If you later use a custom domain, set `site` to it, e.g. 'https://training.yourdomain.com'
  // For Cloudflare Pages on the default *.pages.dev subdomain, you can leave this as-is.
  site: 'https://inthelab.pages.dev',
});
