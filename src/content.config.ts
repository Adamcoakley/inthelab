import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

// Every lab is a Markdown file in src/content/labs/ with this frontmatter.
// Adding a lab = adding a new .md file that matches this shape.
const labs = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/labs' }),
  schema: z.object({
    number: z.number(),                 // lab number, e.g. 8
    title: z.string(),                  // "Launch your first EC2"
    phase: z.number(),                  // which of the 7 phases (1-7)
    type: z.enum(['lab', 'concept', 'challenge']),
    time: z.string().default('~30 min'),
    cost: z.string().default('~$0 if torn down'),
    buildsOn: z.string().optional(),    // "Lab 07"
    summary: z.string(),                // one line for the roadmap
    // recap questions live in frontmatter so the Quiz renders consistently
    questions: z.array(z.object({
      kind: z.enum(['recall', 'cause', 'predict']),
      q: z.string(),
      options: z.array(z.string()),
      correct: z.number(),              // index of the right option
      hint: z.string(),
      explain: z.string(),
    })).default([]),
    draft: z.boolean().default(false),
  }),
});

export const collections = { labs };
