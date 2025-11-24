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

const ARASAAC_API_BASE = 'https://api.arasaac.org/v1';

export async function searchPictograms(query: string, lang: 'es' | 'en' = 'es'): Promise<Pictogram[]> {
  try {
    // Load local catalog data
    const response = await fetch('/data/arasaac_catalog.jsonl');
    const text = await response.text();
    const lines = text.split('\n').filter(line => line.trim());

    // Parse and filter pictograms
    const filteredPictograms: Pictogram[] = [];

    for (const line of lines) {
      try {
        const p = JSON.parse(line);
        if (p.labels && p.labels[lang]) {
          const label = p.labels[lang].toLowerCase();
          const searchTerm = query.toLowerCase();

          // Check if label or synonyms match
          const matches = label.includes(searchTerm) ||
            (p.synonyms?.[lang]?.some((syn: string) => syn.toLowerCase().includes(searchTerm)));

          if (matches) {
            filteredPictograms.push({
              id: Number(p.id),
              labels: p.labels,
              image_urls: p.image_urls,
            });

            // Limit to 10 results
            if (filteredPictograms.length >= 10) break;
          }
        }
      } catch (e) {
        // Skip invalid lines
        continue;
      }
    }

    return filteredPictograms;
  } catch (error) {
    console.error('Error searching pictograms:', error);
    return [];
  }
}

export function getPictogramCategories(): string[] {
  return [
    'person', 'family', 'animal', 'food', 'object', 'place', 'action', 'emotion',
    'communication', 'transport', 'nature', 'leisure', 'work', 'health', 'education'
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