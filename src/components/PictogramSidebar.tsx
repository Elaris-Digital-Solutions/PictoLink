import { useState, useEffect } from 'react';
import { Search, X, Star } from 'lucide-react';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { ScrollArea } from '@/components/ui/scroll-area';
import { searchPictograms, getPictogramsByCategory, getPictogramCategories, CATEGORY_ICONS, type Pictogram } from '@/lib/pictograms';
import { getAutocompleteSuggestions } from '@/lib/api';
import { usePictogramPreferences } from '@/hooks/usePictogramPreferences';

interface PictogramSidebarProps {
    onSelectPictogram: (pictogram: Pictogram) => void;
    selectedPictograms: Pictogram[];
}

export function PictogramSidebar({ onSelectPictogram, selectedPictograms }: PictogramSidebarProps) {
    const [searchQuery, setSearchQuery] = useState('');
    const [searchResults, setSearchResults] = useState<Pictogram[]>([]);
    const [suggestions, setSuggestions] = useState<string[]>([]);
    const [selectedCategory, setSelectedCategory] = useState<string>('');
    const [categoryPictograms, setCategoryPictograms] = useState<Pictogram[]>([]);
    const [isSearching, setIsSearching] = useState(false);

    const { recentPictograms, favoritePictograms, addRecent, toggleFavorite, isFavorite } = usePictogramPreferences();
    const categories = getPictogramCategories();

    // Búsqueda de pictogramas y sugerencias
    useEffect(() => {
        const searchPictogramsDebounced = async () => {
            if (searchQuery.trim().length < 2) {
                setSearchResults([]);
                setSuggestions([]);
                setIsSearching(false);
                return;
            }

            setIsSearching(true);
            try {
                // Fetch suggestions in parallel
                const [results, newSuggestions] = await Promise.all([
                    searchPictograms(searchQuery.trim()),
                    getAutocompleteSuggestions(searchQuery.trim())
                ]);

                setSearchResults(results.slice(0, 20));
                setSuggestions(newSuggestions);
            } catch (error) {
                console.error('Error searching pictograms:', error);
                setSearchResults([]);
                setSuggestions([]);
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

            if (selectedCategory === 'favoritos') {
                setCategoryPictograms(favoritePictograms);
                return;
            }

            if (selectedCategory === 'mas usados') {
                setCategoryPictograms(recentPictograms);
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
    }, [selectedCategory, favoritePictograms, recentPictograms]);

    const handleClearSearch = () => {
        setSearchQuery('');
        setSearchResults([]);
        setSuggestions([]);
    };

    const handleBackToCategories = () => {
        setSelectedCategory('');
        setCategoryPictograms([]);
    };

    const handlePictogramClick = (pictogram: Pictogram) => {
        addRecent(pictogram);
        onSelectPictogram(pictogram);
    };

    const isPictogramSelected = (pictogramId: number) => {
        return selectedPictograms.some(p => p.id === pictogramId);
    };

    const renderPictogramButton = (pictogram: Pictogram) => (
        <div
            key={pictogram.id}
            className={`relative flex flex-col items-center gap-2 p-3 rounded-lg border-2 transition-all hover:border-primary/50 group ${isPictogramSelected(pictogram.id)
                ? 'border-primary bg-primary/5'
                : 'border-gray-200 hover:bg-gray-50'
                }`}
        >
            <button
                onClick={() => handlePictogramClick(pictogram)}
                className="absolute inset-0 w-full h-full z-0"
                aria-label={`Seleccionar ${pictogram.labels?.es}`}
            />
            <button
                onClick={(e) => {
                    e.stopPropagation();
                    toggleFavorite(pictogram);
                }}
                className="absolute top-1 right-1 z-10 p-1 rounded-full hover:bg-gray-100 transition-colors opacity-0 group-hover:opacity-100 focus:opacity-100"
                aria-label={isFavorite(pictogram.id) ? "Quitar de favoritos" : "Añadir a favoritos"}
            >
                <Star
                    className={`h-4 w-4 ${isFavorite(pictogram.id) ? "fill-yellow-400 text-yellow-400" : "text-gray-400"}`}
                />
            </button>
            <img
                src={pictogram.image_urls.png_color}
                alt={pictogram.labels?.es || 'Pictograma'}
                className="w-16 h-16 object-contain z-0 pointer-events-none"
            />
            <span className="text-xs text-center line-clamp-2 z-0 pointer-events-none">
                {pictogram.labels?.es || 'Sin etiqueta'}
            </span>
        </div>
    );

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

                    {/* Autocomplete Suggestions */}
                    {suggestions.length > 0 && (
                        <div className="absolute top-full left-0 mt-1 w-full bg-white border border-gray-200 rounded-lg shadow-lg z-50 overflow-hidden">
                            {suggestions.map((suggestion, index) => (
                                <button
                                    key={index}
                                    className="w-full text-left px-4 py-2 hover:bg-gray-100 text-sm"
                                    onClick={() => {
                                        setSearchQuery(suggestion);
                                        setSuggestions([]);
                                    }}
                                >
                                    {suggestion}
                                </button>
                            ))}
                        </div>
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
                                {searchResults.map(renderPictogramButton)}
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
                                {categoryPictograms.map(renderPictogramButton)}
                            </div>
                            {categoryPictograms.length === 0 && (
                                <p className="text-sm text-muted-foreground text-center py-8">
                                    {selectedCategory === 'favoritos'
                                        ? 'No tienes pictogramas favoritos aún'
                                        : selectedCategory === 'mas usados'
                                            ? 'No hay pictogramas recientes'
                                            : 'Cargando pictogramas...'}
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
                                        {category === 'favoritos' ? (
                                            <Star className="w-16 h-16 text-yellow-400 fill-yellow-400" />
                                        ) : (
                                            <img
                                                src={`https://static.arasaac.org/pictograms/${CATEGORY_ICONS[category] || 2369}/${CATEGORY_ICONS[category] || 2369}_500.png`}
                                                alt={category}
                                                className="w-16 h-16 object-contain"
                                            />
                                        )}
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
