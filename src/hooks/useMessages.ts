import { useState, useEffect, useCallback } from "react";
import { supabase } from "@/lib/supabase";
import { useAuth } from "@/contexts/AuthContext";
import type { Message } from "@/types/database.types";
import type { RealtimeChannel } from "@supabase/supabase-js";

export function useMessages(contactId: string | null) {
    const { user } = useAuth();
    const [messages, setMessages] = useState<Message[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    // Cargar mensajes de la conversación
    const loadMessages = useCallback(async () => {
        if (!user || !contactId) {
            setMessages([]);
            return;
        }

        try {
            setLoading(true);
            setError(null);

            const { data, error: messagesError } = await supabase
                .from("messages")
                .select("*")
                .or(
                    `and(sender_id.eq.${user.id},receiver_id.eq.${contactId}),and(sender_id.eq.${contactId},receiver_id.eq.${user.id})`
                )
                .order("created_at", { ascending: true });

            if (messagesError) throw messagesError;

            setMessages(data || []);

            // Marcar mensajes como leídos
            await supabase
                .from("messages")
                .update({ read: true })
                .eq("sender_id", contactId)
                .eq("receiver_id", user.id)
                .eq("read", false);
        } catch (err: any) {
            console.error("Error loading messages:", err);
            setError(err.message);
        } finally {
            setLoading(false);
        }
    }, [user, contactId]);

    // Cargar mensajes cuando cambia el contacto
    useEffect(() => {
        loadMessages();
    }, [loadMessages]);

    // Suscribirse a nuevos mensajes en tiempo real
    useEffect(() => {
        if (!user || !contactId) return;

        let channel: RealtimeChannel;

        const setupRealtimeSubscription = async () => {
            channel = supabase
                .channel(`messages:${user.id}:${contactId}`)
                .on(
                    "postgres_changes",
                    {
                        event: "INSERT",
                        schema: "public",
                        table: "messages",
                        filter: `receiver_id=eq.${user.id}`,
                    },
                    (payload) => {
                        const newMessage = payload.new as Message;

                        // Solo añadir si es de este contacto
                        if (newMessage.sender_id === contactId) {
                            setMessages((prev) => [...prev, newMessage]);

                            // Marcar como leído automáticamente
                            supabase
                                .from("messages")
                                .update({ read: true })
                                .eq("id", newMessage.id);
                        }
                    }
                )
                .subscribe();
        };

        setupRealtimeSubscription();

        return () => {
            if (channel) {
                supabase.removeChannel(channel);
            }
        };
    }, [user, contactId]);

    const sendMessage = async (content: string): Promise<void> => {
        if (!user || !contactId) throw new Error("No user or contact selected");
        if (!content.trim()) throw new Error("Message cannot be empty");

        try {
            setError(null);

            const { data, error: sendError } = await supabase
                .from("messages")
                .insert({
                    sender_id: user.id,
                    receiver_id: contactId,
                    content: content.trim(),
                })
                .select()
                .single();

            if (sendError) throw sendError;

            // Añadir mensaje a la lista local
            setMessages((prev) => [...prev, data]);
        } catch (err: any) {
            console.error("Error sending message:", err);
            setError(err.message);
            throw err;
        }
    };

    return {
        messages,
        loading,
        error,
        sendMessage,
        refreshMessages: loadMessages,
    };
}
