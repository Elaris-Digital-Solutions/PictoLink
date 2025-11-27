import { useState, useEffect, useCallback } from 'react';
import { supabase } from '@/lib/supabase';
import { Pictogram } from '@/lib/pictograms';

export function usePictogramPreferences() {
    const [recentPictograms, setRecentPictograms] = useState<Pictogram[]>([]);
    const [favoritePictograms, setFavoritePictograms] = useState<Pictogram[]>([]);
    const [loading, setLoading] = useState(true);
    const [userId, setUserId] = useState<string | null>(null);

    useEffect(() => {
        // Get current user
        supabase.auth.getUser().then(({ data: { user } }) => {
            if (user) {
                setUserId(user.id);
                fetchPreferences(user.id);
            } else {
                setLoading(false);
            }
        });

        const { data: { subscription } } = supabase.auth.onAuthStateChange((_event, session) => {
            if (session?.user) {
                setUserId(session.user.id);
                fetchPreferences(session.user.id);
            } else {
                setUserId(null);
                setRecentPictograms([]);
                setFavoritePictograms([]);
                setLoading(false);
            }
        });

        return () => subscription.unsubscribe();
    }, []);

    const fetchPreferences = async (uid: string) => {
        setLoading(true);
        try {
            const { data, error } = await supabase
                .from('user_pictograms')
                .select('*')
                .eq('user_id', uid);

            if (error) throw error;

            const recents = data
                .filter(item => item.type === 'recent')
                .sort((a, b) => new Date(b.last_used_at).getTime() - new Date(a.last_used_at).getTime())
                .map(item => item.data as Pictogram);

            const favorites = data
                .filter(item => item.type === 'favorite')
                .sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
                .map(item => item.data as Pictogram);

            setRecentPictograms(recents);
            setFavoritePictograms(favorites);
        } catch (error) {
            console.error('Error fetching pictogram preferences:', error);
        } finally {
            setLoading(false);
        }
    };

    const addRecent = useCallback(async (pictogram: Pictogram) => {
        if (!userId) return;

        // Optimistic update
        setRecentPictograms(prev => {
            const filtered = prev.filter(p => p.id !== pictogram.id);
            return [pictogram, ...filtered].slice(0, 20);
        });

        try {
            // Check if exists
            const { data: existing } = await supabase
                .from('user_pictograms')
                .select('id')
                .eq('user_id', userId)
                .eq('pictogram_id', pictogram.id)
                .eq('type', 'recent')
                .maybeSingle();

            if (existing) {
                // Update last_used_at
                await supabase
                    .from('user_pictograms')
                    .update({ last_used_at: new Date().toISOString(), data: pictogram })
                    .eq('id', existing.id);
            } else {
                // Insert new
                await supabase
                    .from('user_pictograms')
                    .insert({
                        user_id: userId,
                        pictogram_id: pictogram.id,
                        type: 'recent',
                        data: pictogram,
                        last_used_at: new Date().toISOString()
                    });

                // Cleanup old recents if > 20
                const { data: allRecents } = await supabase
                    .from('user_pictograms')
                    .select('id')
                    .eq('user_id', userId)
                    .eq('type', 'recent')
                    .order('last_used_at', { ascending: false });

                if (allRecents && allRecents.length > 20) {
                    const idsToDelete = allRecents.slice(20).map(r => r.id);
                    await supabase
                        .from('user_pictograms')
                        .delete()
                        .in('id', idsToDelete);
                }
            }
        } catch (error) {
            console.error('Error adding recent pictogram:', error);
        }
    }, [userId]);

    const toggleFavorite = useCallback(async (pictogram: Pictogram) => {
        if (!userId) return;

        const isFav = favoritePictograms.some(p => p.id === pictogram.id);

        // Optimistic update
        if (isFav) {
            setFavoritePictograms(prev => prev.filter(p => p.id !== pictogram.id));
        } else {
            setFavoritePictograms(prev => [pictogram, ...prev]);
        }

        try {
            if (isFav) {
                await supabase
                    .from('user_pictograms')
                    .delete()
                    .eq('user_id', userId)
                    .eq('pictogram_id', pictogram.id)
                    .eq('type', 'favorite');
            } else {
                await supabase
                    .from('user_pictograms')
                    .insert({
                        user_id: userId,
                        pictogram_id: pictogram.id,
                        type: 'favorite',
                        data: pictogram
                    });
            }
        } catch (error) {
            console.error('Error toggling favorite pictogram:', error);
        }
    }, [userId, favoritePictograms]);

    const isFavorite = useCallback((pictogramId: number) => {
        return favoritePictograms.some(p => p.id === pictogramId);
    }, [favoritePictograms]);

    return {
        recentPictograms,
        favoritePictograms,
        loading,
        addRecent,
        toggleFavorite,
        isFavorite
    };
}
