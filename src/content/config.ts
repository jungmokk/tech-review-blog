import { z, defineCollection } from 'astro:content';

const reviewsCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    date: z.string(),
    device: z.string(),
    score: z.number(),
    category: z.string().default('테크'),
    summary: z.string(),
    pros: z.array(z.string()).optional(),
    cons: z.array(z.string()).optional(),
  }),
});

export const collections = {
  reviews: reviewsCollection,
};
