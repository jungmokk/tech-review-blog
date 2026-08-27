import type { CollectionEntry } from 'astro:content';
import devices from '../data/smartphones.json';

/**
 * 기기 출시일(release_date: "YYYY-MM" / "YYYY-MM-DD" 또는 release_year) 기준 타임스탬프 계산
 */
export function getDeviceReleaseTimestamp(slug: string, fallbackDate?: string): number {
  const pureSlug = slug.replace(/^(en|ja)\//, '');
  const dev = (devices as any[]).find((d: any) => d.id === pureSlug);

  if (dev?.release_date) {
    const parts = String(dev.release_date).split('-');
    const year = parseInt(parts[0], 10);
    const month = parts[1] ? parseInt(parts[1], 10) - 1 : 0;
    const day = parts[2] ? parseInt(parts[2], 10) : 1;
    if (!isNaN(year)) {
      return new Date(year, month, day).getTime();
    }
  }

  if (dev?.release_year) {
    const year = parseInt(String(dev.release_year), 10);
    if (!isNaN(year)) {
      return new Date(year, 0, 1).getTime();
    }
  }

  if (fallbackDate) {
    const fallbackTime = new Date(fallbackDate).getTime();
    if (!isNaN(fallbackTime)) {
      return fallbackTime;
    }
  }

  return new Date('2000-01-01').getTime();
}

/**
 * 기기 출시 시점(최신 출시순) 기준으로 리뷰를 내림차순 정렬
 * 1순위: 기기 실제 출시일 (최신순)
 * 2순위: 리뷰 발행일 (최신순)
 */
export function sortReviewsByDeviceRelease(reviews: CollectionEntry<'reviews'>[]): CollectionEntry<'reviews'>[] {
  return [...reviews].sort((a, b) => {
    const tsA = getDeviceReleaseTimestamp(a.slug, a.data.date);
    const tsB = getDeviceReleaseTimestamp(b.slug, b.data.date);
    if (tsB !== tsA) {
      return tsB - tsA;
    }
    const postTimeA = new Date(a.data.date || '').getTime() || 0;
    const postTimeB = new Date(b.data.date || '').getTime() || 0;
    return postTimeB - postTimeA;
  });
}
