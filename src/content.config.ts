import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

// Every lab is a Markdown file in src/content/labs/ with this frontmatter.
// Adding a lab = adding a new .md file that matches this shape.

const labs = defineCollection({
  loader: glob({
    pattern: '**/*.md',
    base: './src/content/labs',
  }),

  schema: z.object({
    // New roadmap structure:
    // phase = roadmap phase, e.g. 0
    // order = position inside that phase, e.g. 1
    //
    // Together these produce labels such as:
    // 0.1, 0.2, 1.1, 2.4, etc.
    phase: z.number(),
    order: z.number().optional(),

    // Temporary support for older labs that still use a single global number.
    // Once all labs have been migrated to phase + order,
    // this can be removed and order can become required.
    number: z.number().optional(),

    title: z.string(),

    type: z.enum([
      'lab',
      'concept',
      'challenge',
    ]),

    time: z.string().default('~30 min'),

    cost: z.string().default('~$0 if torn down'),

    buildsOn: z.string().optional(),

    // One-line description shown on the roadmap.
    summary: z.string(),

    // Recap questions live in frontmatter so Quiz renders consistently.
    questions: z.array(
      z.object({
        kind: z.enum([
          'recall',
          'cause',
          'predict',
        ]),

        q: z.string(),

        options: z.array(z.string()),

        // Zero-based index of the correct option.
        correct: z.number(),

        hint: z.string(),

        explain: z.string(),
      })
    ).default([]),

    draft: z.boolean().default(false),
  }),
});

export const collections = {
  labs,
};