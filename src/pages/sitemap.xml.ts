import { getCollection } from 'astro:content';

export async function GET() {
  const reviews = await getCollection('reviews');
  const siteUrl = 'https://tech-review-blog.vercel.app';

  const pages = [
    '',
    'specs',
    ...reviews.map((post) => `reviews/${post.slug}`),
  ];

  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  ${pages
    .map(
      (page) => `
    <url>
      <loc>${siteUrl}/${page}</loc>
      <lastmod>${new Date().toISOString().split('T')[0]}</lastmod>
      <changefreq>daily</changefreq>
      <priority>${page === '' ? '1.0' : '0.8'}</priority>
    </url>
  `
    )
    .join('')}
</urlset>`;

  return new Response(xml, {
    headers: {
      'Content-Type': 'application/xml',
    },
  });
}
