// Tipos de base de datos para Supabase
export interface Contact {
    id: string;
    user_id: string;
    contact_id: string;
    created_at: string;
}

export interface Message {
    id: string;
    sender_id: string;
    receiver_id: string;
    content: string;
    created_at: string;
    read: boolean;
}

// Tipo extendido con información del usuario
export interface ContactWithUser {
    id: string;
    contact_id: string;
    name: string;
    email: string;
    lastMessage?: string;
    lastMessageTime?: string;
    unread: number;
}

// Tipo para la respuesta de add_contact_by_email
export interface AddContactResponse {
    status: 'ok' | 'error';
    message?: string;
    contact_id?: string;
}
