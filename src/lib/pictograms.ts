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

export const CATEGORY_ICONS: Record<string, number> = {
  'favoritos': 2292, // Star/Favorite icon ID
  'mas usados': 5584,
  'personas': 31807,
  'saludos': 34567,
  'necesidades': 39122,
  'sentimientos': 35545,
  'lugares': 6964,
  'acciones': 28669,
  'comida': 32464,
  'animales': 38967,
  'transporte': 6981,
};

export const CUSTOM_CATEGORY_DATA: Record<string, number[]> = {
  'mas usados': [], // Will be populated dynamically
  'personas': [31807, 6997, 38961, 38962, 38963, 38964, 38965, 38966, 38968, 38969, 38970, 38971, 38972],
  'saludos': [34567, 34568, 6554, 6556, 6555, 6653, 6724],
  'necesidades': [39122, 32464, 28669, 32465, 32466, 2275, 32467, 32468, 32469],
  'sentimientos': [35545, 35546, 35547, 35548, 35549, 35550],
  'lugares': [6964, 6965, 6966, 6967, 6968, 6969],
  'acciones': [28669, 32465, 32466, 7004, 7007, 7006, 2345, 2345],
  'comida': [32464, 32470, 32471, 32472, 32473, 32474, 32475, 32476],
  'animales': [38967, 38968, 38969, 38970, 38971, 38972, 38973],
  'transporte': [6981, 6982, 6983, 6984, 6985, 6986]
};

export function getPictogramCategories(): string[] {
  // Ensure 'favoritos' and 'mas usados' are first
  const keys = Object.keys(CATEGORY_ICONS);
  const priority = ['favoritos', 'mas usados'];
  return [
    ...priority,
    ...keys.filter(k => !priority.includes(k))
  ];
}

export async function searchPictograms(query: string, lang: 'es' | 'en' = 'es'): Promise<Pictogram[]> {
  return await searchPictogramsAPI(query);
}

export async function getPictogramsByCategory(category: string, limit: number = 50): Promise<Pictogram[]> {
  try {
    const customIds = CUSTOM_CATEGORY_DATA[category.toLowerCase()];

    const response = await fetch('/data/arasaac_catalog.jsonl');
    const text = await response.text();
    const lines = text.split('\n').filter(line => line.trim());

    const categoryPictograms: Pictogram[] = [];

    if (customIds) {
      const idSet = new Set(customIds);
      for (const line of lines) {
        try {
          const p = JSON.parse(line);
          if (idSet.has(p.id)) {
            categoryPictograms.push({
              id: Number(p.id),
              labels: p.labels,
              image_urls: p.image_urls,
            });
          }
        } catch (e) { continue; }
      }
      categoryPictograms.sort((a, b) => customIds.indexOf(a.id) - customIds.indexOf(b.id));
      return categoryPictograms;
    }

    let searchCategory = category;
    if (category === 'animales') searchCategory = 'animal';
    if (category === 'comida') searchCategory = 'food';
    if (category === 'transporte') searchCategory = 'transport';

    for (const line of lines) {
      try {
        const p = JSON.parse(line);
        const categories = p.sources?.es?.raw?.categories || [];
        if (categories.includes(searchCategory) && p.labels?.es) {
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