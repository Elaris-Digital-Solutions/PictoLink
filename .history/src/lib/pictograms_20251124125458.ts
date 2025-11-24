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
    const allPictograms = lines.map(line => JSON.parse(line)).filter(p => p.labels && p.labels[lang]);

    const filteredPictograms = allPictograms
      .filter((p: any) => {
        const label = p.labels[lang].toLowerCase();
        const searchTerm = query.toLowerCase();
        return label.includes(searchTerm) ||
               p.synonyms?.[lang]?.some((syn: string) => syn.toLowerCase().includes(searchTerm));
      })
      .slice(0, 10) // Limit to 10 results
      .map((p: any) => ({
        id: Number(p.id),
        labels: p.labels,
        image_urls: p.image_urls,
      }));

    return filteredPictograms;
  } catch (error) {
    console.error('Error searching pictograms:', error);
    return [];
  }
}

export function getPictogramImageUrl(id: number): string {
  return `https://static.arasaac.org/pictograms/${id}/${id}_500.png`;
}