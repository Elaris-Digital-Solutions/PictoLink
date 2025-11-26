import { Pictogram } from './pictograms';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

export async function convertTextToPictos(text: string): Promise<Pictogram[]> {
    console.log(`[API] convertTextToPictos called with text: "${text}"`);
    const url = `${API_BASE_URL}/text-to-pictos`;
    console.log(`[API] Fetching URL: ${url}`);

    try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 5000); // 5 second timeout

        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text }),
            signal: controller.signal
        });
        clearTimeout(timeoutId);

        console.log(`[API] Response status: ${response.status}`);

        if (!response.ok) {
            throw new Error(`API error: ${response.status} ${response.statusText}`);
        }

        const data = await response.json();
        console.log('[API] Data received:', data);
        return data.pictograms;
    } catch (error) {
        console.error('Error converting text to pictograms:', error);
        if (error instanceof Error && error.name === 'AbortError') {
            console.error('Request timed out');
        }
        throw error; // Re-throw to let the caller handle it (or fallback)
    }
}

export async function convertPictosToText(pictograms: Pictogram[]): Promise<string> {
    try {
        const response = await fetch(`${API_BASE_URL}/pictos-to-text`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ pictograms }),
        });

        if (!response.ok) {
            throw new Error(`API error: ${response.statusText}`);
        }

        const data = await response.json();
        return data.text;
    } catch (error) {
        console.error('Error converting pictograms to text:', error);
        return '';
    }
}

export async function searchPictogramsAPI(query: string): Promise<Pictogram[]> {
    try {
        const response = await fetch(`${API_BASE_URL}/search?q=${encodeURIComponent(query)}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (!response.ok) {
            throw new Error(`API error: ${response.statusText}`);
        }

        const data = await response.json();
        return data.pictograms;
    } catch (error) {
        console.error('Error searching pictograms:', error);
        return [];
    }
}

export async function getAutocompleteSuggestions(query: string): Promise<string[]> {
    if (!query || query.length < 2) return [];
    try {
        const response = await fetch(`${API_BASE_URL}/autocomplete?q=${encodeURIComponent(query)}`);
        if (!response.ok) return [];
        return await response.json();
    } catch (error) {
        console.error('Error fetching suggestions:', error);
        return [];
    }
}
