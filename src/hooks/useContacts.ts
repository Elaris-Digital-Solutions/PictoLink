import { useState, useEffect } from "react";
import { supabase } from "@/lib/supabase";
import { useAuth } from "@/contexts/AuthContext";
import type { ContactWithUser, AddContactResponse } from "@/types/database.types";

export function useContacts() {
    const { user } = useAuth();
    const [contacts, setContacts] = useState<ContactWithUser[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    // Cargar contactos del usuario
    useEffect(() => {
        if (!user) {
            setContacts([]);
            setLoading(false);
            return;
        }

        loadContacts();
    }, [user]);

    const loadContacts = async () => {
        if (!user) return;

        try {
            setLoading(true);
            setError(null);

            // Obtener contactos
            const { data: contactsData, error: contactsError } = await supabase
                .from("contacts")
                .select("id, contact_id")
                .eq("user_id", user.id);

            if (contactsError) throw contactsError;

            if (!contactsData || contactsData.length === 0) {
                setContacts([]);
                setLoading(false);
                return;
            }

            // Obtener información de cada contacto
            const contactsWithInfo = await Promise.all(
                contactsData.map(async (contact) => {
                    // Obtener datos del perfil del usuario
                    const { data: profileData } = await supabase
                        .from("profiles")
                        .select("name")
                        .eq("id", contact.contact_id)
                        .single();

                    // Obtener último mensaje de la conversación
                    const { data: lastMessageData } = await supabase
                        .from("messages")
                        .select("id, content, created_at")
                        .or(
                            `and(sender_id.eq.${user.id},receiver_id.eq.${contact.contact_id}),and(sender_id.eq.${contact.contact_id},receiver_id.eq.${user.id})`
                        )
                        .order("created_at", { ascending: false })
                        .limit(1)
                        .maybeSingle();

                    // Contar mensajes no leídos
                    const { count: unreadCount } = await supabase
                        .from("messages")
                        .select("*", { count: "exact", head: true })
                        .eq("sender_id", contact.contact_id)
                        .eq("receiver_id", user.id)
                        .eq("read", false);

                    return {
                        id: contact.id,
                        contact_id: contact.contact_id,
                        name: profileData?.name || "Usuario",
                        email: "",
                        lastMessage: lastMessageData?.content,
                        lastMessageTime: lastMessageData?.created_at,
                        unread: unreadCount || 0,
                    };
                })
            );

            setContacts(contactsWithInfo);
        } catch (err: any) {
            console.error("Error loading contacts:", err);
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    const addContact = async (email: string): Promise<void> => {
        if (!user) throw new Error("No user logged in");

        try {
            setError(null);

            // Llamar a la función RPC de Supabase
            const { data, error: rpcError } = await supabase.rpc("add_contact_by_email", {
                p_user_id: user.id,
                p_email: email.trim().toLowerCase(),
            });

            if (rpcError) throw rpcError;

            const response = data as AddContactResponse;

            if (response.status === "error") {
                switch (response.message) {
                    case "user_not_found":
                        throw new Error("No se encontró un usuario con ese email");
                    case "cannot_add_self":
                        throw new Error("No puedes agregarte a ti mismo como contacto");
                    case "already_contact":
                        throw new Error("Este usuario ya está en tus contactos");
                    default:
                        throw new Error("Error al añadir contacto");
                }
            }

            // Recargar contactos
            await loadContacts();
        } catch (err: any) {
            setError(err.message);
            throw err;
        }
    };

    return {
        contacts,
        loading,
        error,
        addContact,
        refreshContacts: loadContacts,
    };
}
