import { getCollection } from 'astro:content';

export async function GET() {
  const reviews = await getCollection('reviews');
  const siteUrl = 'https://tech-review-blog.vercel.app';

  const basePages = [
    '',
    'specs',
    'about',
    'privacy',
    'contact',
    'en',
    'ja',
  ];

  const reviewUrls = reviews.map((post) => {
    if (post.slug.startsWith('en/')) {
      return `en/reviews/${post.slug.replace('en/', '')}`;
    }
    if (post.slug.startsWith('ja/')) {
      return `ja/reviews/${post.slug.replace('ja/', '')}`;
    }
    return `reviews/${post.slug}`;
  });

  const allPages = [...basePages, ...reviewUrls];

  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  ${allPages
    .map(
      (page) => `
    <url>
      <loc>${siteUrl}/${page}</loc>
      <lastmod>${new Date().toISOString().split('T')[0]}</lastmod>
      <changefreq>daily</changefreq>
      <priority>${page === '' || page === 'en' || page === 'ja' ? '1.0' : '0.8'}</priority>
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
