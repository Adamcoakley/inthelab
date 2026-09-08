# inthelab

Hands-on AWS training built around learning by doing - and occasionally by breaking things first.

This site introduces AWS concepts through practical labs where problems appear naturally. Learners see something fail, understand *why* it failed, and then use the appropriate AWS service or configuration to fix it.

The course starts with cloud and networking fundamentals and gradually builds toward a resilient, production-shaped AWS architecture.

**Live site:** [inthelab.ie](https://inthelab.ie) (coming soon!)

## Tech stack

- **[Astro](https://astro.build)** — static site framework
- **Markdown + frontmatter** — lab content and quiz data
- **CSS** — custom styling with light and dark themes
- **Vanilla JavaScript** — quizzes, theme switching, and learner personalisation
- **[Cloudflare Pages](https://pages.cloudflare.com)** — hosting, CDN, HTTPS, and continuous deployment

The site is fully static with no backend or database. Learner-specific settings are stored locally in the browser.

## Running locally

You'll need **Node.js 18 or newer**.

Clone the repository and install the dependencies:

```bash
npm install
````

Start the development server:

```bash
npm run dev
```

Then open the local address shown in the terminal, usually:

```text
http://localhost:4321
```

To create a production build:

```bash
npm run build
```

To preview the production build locally:

```bash
npm run preview
```