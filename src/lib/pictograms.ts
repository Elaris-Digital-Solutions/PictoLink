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
  'mas usados': [5584, 5596, 5441, 6653, 34567, 34568, 2275, 32464, 39122, 28669, 32301],
  'personas': [2617, 2608, 6480, 7028, 7185, 7032, 2458, 31146, 2244, 2243, 2485, 2484, 2275, 4665, 4703, 8487, 8486, 2392, 7796],
  'saludos': [6009, 5896, 6944, 6943, 6942, 8194, 8128, 6936, 4576, 4550],
  'necesidades': [15905, 2370, 2349, 2276, 2369, 19524, 2367, 8163, 3299, 2863, 35559],
  'sentimientos': [2606, 2374, 10261, 35565, 2314, 2245, 30391, 3245, 3239, 13354, 11178, 2418, 38936],
  'lugares': [2317, 3082, 2859, 3116, 2299, 9116, 3389, 2341, 32234, 15905, 6211, 2434, 10283, 2826, 3142],
  'acciones': [2432, 11708, 5441, 7271, 5465, 5581, 11749, 2474, 3345, 2439, 2599, 2387, 6457, 8109, 7195, 4570, 6946],
  'comida': [2248, 2494, 2445, 4653, 2462, 2530, 2316, 2519, 2533, 2427, 6911, 8652, 8312, 11461, 4626, 4610, 4592],
  'animales': [2517, 2406, 2490, 2520, 2294, 2609, 2327, 2489, 2403, 2449, 2372, 2437, 2477, 2488, 2351],
  'transporte': [2339, 2262, 2603, 2264, 2273, 2277, 5084, 2580, 2251, 2306, 3275, 2472, 6212]
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