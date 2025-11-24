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

const ARASAAC_API_BASE = 'https://api.arasaac.org/api';

export async function searchPictograms(query: string, lang: 'es' | 'en' = 'es'): Promise<Pictogram[]> {
  try {
    const response = await fetch(`${ARASAAC_API_BASE}/pictograms/${lang}/search/${encodeURIComponent(query)}`);
    if (!response.ok) {
      throw new Error('Failed to search pictograms');
    }
    const ids: number[] = await response.json();

    // Get details for each pictogram
    const pictograms = await Promise.all(
      ids.slice(0, 10).map(async (id) => {
        const detailResponse = await fetch(`${ARASAAC_API_BASE}/pictograms/${id}`);
        if (!detailResponse.ok) {
          return null;
        }
        const data = await detailResponse.json();
        return {
          id: id, // Use the id from the search results, not data._id
          labels: data.meaning || { es: 'Sin etiqueta', en: 'No label' },
          image_urls: {
            svg_color: data.svgColor || '',
            png_color: data.pngColor || '',
            detail: `https://arasaac.org/pictograms/${id}`,
          },
        } as Pictogram;
      })
    );

    return pictograms.filter(Boolean) as Pictogram[];
  } catch (error) {
    console.error('Error searching pictograms:', error);
    return [];
  }
}

export function getPictogramImageUrl(id: number): string {
  return `${ARASAAC_API_BASE}/pictograms/${id}`;
}