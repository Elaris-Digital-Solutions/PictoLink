import { useState, useEffect } from 'react';
import { Search, X } from 'lucide-react';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { ScrollArea } from '@/components/ui/scroll-area';
import { searchPictograms, getPictogramsByCategory, getPictogramCategories, CATEGORY_ICONS, type Pictogram } from '@/lib/pictograms';

interface PictogramSidebarProps {
    onSelectPictogram: (pictogram: Pictogram) => void;
    selectedPictograms: Pictogram[];
}

export function PictogramSidebar({ onSelectPictogram, selectedPictograms }: PictogramSidebarProps) {
    const [searchQuery, setSearchQuery] = useState('');
    const [searchResults, setSearchResults] = useState<Pictogram[]>([]);
    const [selectedCategory, setSelectedCategory] = useState<string>('');
    const [categoryPictograms, setCategoryPictograms] = useState<Pictogram[]>([]);
    const [isSearching, setIsSearching] = useState(false);
    const categories = getPictogramCategories();

    // Búsqueda de pictogramas
    useEffect(() => {
        const searchPictogramsDebounced = async () => {
            if (searchQuery.trim().length < 2) {
                setSearchResults([]);
                setIsSearching(false);
                return;
            }

            setIsSearching(true);
            try {
                const results = await searchPictograms(searchQuery.trim());
                setSearchResults(results.slice(0, 20)); // Limitar a 20 resultados
            } catch (error) {
                console.error('Error searching pictograms:', error);
                setSearchResults([]);
            } finally {
                setIsSearching(false);
            }
        };

        const timeoutId = setTimeout(searchPictogramsDebounced, 300);
        return () => clearTimeout(timeoutId);
    }, [searchQuery]);

    // Cargar pictogramas de categoría seleccionada
    useEffect(() => {
        const loadCategoryPictograms = async () => {
            if (!selectedCategory) {
                setCategoryPictograms([]);
                return;
            }

            try {
                const pictograms = await getPictogramsByCategory(selectedCategory, 30);
                setCategoryPictograms(pictograms);
            } catch (error) {
                console.error('Error loading category pictograms:', error);
                setCategoryPictograms([]);
            }
        };

        loadCategoryPictograms();
    }, [selectedCategory]);

    const handleClearSearch = () => {
        setSearchQuery('');
        setSearchResults([]);
    };

    const handleBackToCategories = () => {
        setSelectedCategory('');
        setCategoryPictograms([]);
    };

    const isPictogramSelected = (pictogramId: number) => {
        return selectedPictograms.some(p => p.id === pictogramId);
    };

    return (
        <div className="flex flex-col h-full bg-white border-l border-border">
            {/* Header con búsqueda */}
            <div className="p-4 border-b border-border">
                <h3 className="text-lg font-semibold mb-3">Pictogramas</h3>

                {/* Barra de búsqueda */}
                <div className="relative">
                    <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                    <Input
                        type="text"
                        placeholder="Buscar pictogramas..."
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                        className="pl-9 pr-9"
                    />
                    {searchQuery && (
                        <button
                            onClick={handleClearSearch}
                            className="absolute right-3 top-1/2 transform -translate-y-1/2 text-muted-foreground hover:text-foreground"
                        >
                            <X className="h-4 w-4" />
                        </button>
                    )}
                </div>
            </div>

            {/* Contenido */}
            <ScrollArea className="flex-1">
                <div className="p-4">
                    {/* Resultados de búsqueda */}
                    {searchQuery.trim().length >= 2 ? (
                        <div>
                            <h4 className="text-sm font-medium mb-3 text-muted-foreground">
                                {isSearching ? 'Buscando...' : `Resultados (${searchResults.length})`}
                            </h4>
                            <div className="grid grid-cols-2 gap-3">
                                {searchResults.map((pictogram) => (
                                    <button
                                        key={pictogram.id}
                                        onClick={() => onSelectPictogram(pictogram)}
                                        className={`flex flex-col items-center gap-2 p-3 rounded-lg border-2 transition-all hover:border-primary/50 ${isPictogramSelected(pictogram.id)
                                                ? 'border-primary bg-primary/5'
                                                : 'border-gray-200 hover:bg-gray-50'
                                            }`}
                                    >
                                        <img
                                            src={pictogram.image_urls.png_color}
                                            alt={pictogram.labels?.es || 'Pictograma'}
                                            className="w-16 h-16 object-contain"
                                        />
                                        <span className="text-xs text-center line-clamp-2">
                                            {pictogram.labels?.es || 'Sin etiqueta'}
                                        </span>
                                    </button>
                                ))}
                            </div>
                            {searchResults.length === 0 && !isSearching && (
                                <p className="text-sm text-muted-foreground text-center py-8">
                                    No se encontraron pictogramas
                                </p>
                            )}
                        </div>
                    ) : selectedCategory ? (
                        /* Vista de categoría seleccionada */
                        <div>
                            <div className="flex items-center gap-2 mb-4">
                                <Button
                                    variant="ghost"
                                    size="sm"
                                    onClick={handleBackToCategories}
                                    className="h-8"
                                >
                                    ← Volver
                                </Button>
                                <h4 className="text-sm font-medium capitalize">{selectedCategory.replace('_', ' ')}</h4>
                            </div>
                            <div className="grid grid-cols-2 gap-3">
                                {categoryPictograms.map((pictogram) => (
                                    <button
                                        key={pictogram.id}
                                        onClick={() => onSelectPictogram(pictogram)}
                                        className={`flex flex-col items-center gap-2 p-3 rounded-lg border-2 transition-all hover:border-primary/50 ${isPictogramSelected(pictogram.id)
                                                ? 'border-primary bg-primary/5'
                                                : 'border-gray-200 hover:bg-gray-50'
                                            }`}
                                    >
                                        <img
                                            src={pictogram.image_urls.png_color}
                                            alt={pictogram.labels?.es || 'Pictograma'}
                                            className="w-16 h-16 object-contain"
                                        />
                                        <span className="text-xs text-center line-clamp-2">
                                            {pictogram.labels?.es || 'Sin etiqueta'}
                                        </span>
                                    </button>
                                ))}
                            </div>
                            {categoryPictograms.length === 0 && (
                                <p className="text-sm text-muted-foreground text-center py-8">
                                    Cargando pictogramas...
                                </p>
                            )}
                        </div>
                    ) : (
                        /* Grid de categorías */
                        <div>
                            <h4 className="text-sm font-medium mb-3 text-muted-foreground">Categorías</h4>
                            <div className="grid grid-cols-2 gap-3">
                                {categories.map((category) => (
                                    <button
                                        key={category}
                                        onClick={() => setSelectedCategory(category)}
                                        className="flex flex-col items-center gap-2 p-4 rounded-lg border-2 border-gray-200 hover:border-primary/50 hover:bg-gray-50 transition-all"
                                    >
                                        <img
                                            src={`https://static.arasaac.org/pictograms/${CATEGORY_ICONS[category] || 2369}/${CATEGORY_ICONS[category] || 2369}_500.png`}
                                            alt={category}
                                            className="w-16 h-16 object-contain"
                                        />
                                        <span className="text-xs text-center font-medium capitalize">
                                            {category.replace('_', ' ')}
                                        </span>
                                    </button>
                                ))}
                            </div>
                        </div>
                    )}
                </div>
            </ScrollArea>
        </div>
    );
}
