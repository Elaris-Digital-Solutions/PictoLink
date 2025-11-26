import { searchPictogramsAPI } from './api';

export interface Pictogram {
  id: number;
  labels: {
    es: string;
    en: string;
  };
  image_urls: {
    svg_color: string;
    png_color: string;
    detail: string;
  };
}

export async function searchPictograms(query: string, lang: 'es' | 'en' = 'es'): Promise<Pictogram[]> {
  // Use the backend API for search
  return await searchPictogramsAPI(query);
}

export function getPictogramCategories(): string[] {
  return [
    'animal', 'food', 'person', 'family', 'emotion', 'action', 'object',
    'place', 'transport', 'nature', 'leisure', 'work', 'health', 'communication',
    'clothes', 'building facility', 'gastronomy', 'core vocabulary-object'
  ];
}

export async function getPictogramsByCategory(category: string, limit: number = 20): Promise<Pictogram[]> {
  try {
    const response = await fetch('/data/arasaac_catalog.jsonl');
    const text = await response.text();
    const lines = text.split('\n').filter(line => line.trim());

    const categoryPictograms: Pictogram[] = [];

    for (const line of lines) {
      try {
        const p = JSON.parse(line);
        // Check if pictogram has categories in the correct structure
        const categories = p.sources?.es?.raw?.categories || [];
        if (categories.includes(category) && p.labels?.es) {
          categoryPictograms.push({
            id: Number(p.id),
            labels: p.labels,
            image_urls: p.image_urls,
          });

          if (categoryPictograms.length >= limit) break;
        }
      } catch (e) {
        continue;
      }
    }

    return categoryPictograms;
  } catch (error) {
    console.error('Error loading pictograms by category:', error);
    return [];
  }
}