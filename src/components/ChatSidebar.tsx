import { useState } from "react";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuItem,
  SidebarMenuButton,
  useSidebar,
} from "@/components/ui/sidebar";
import { Search, MessageSquare, UserPlus } from "lucide-react";
import { useAuth } from "@/contexts/AuthContext";
import { useContacts } from "@/hooks/useContacts";
import { AddContactDialog } from "./AddContactDialog";
import { formatDistanceToNow } from "date-fns";
import { es } from "date-fns/locale";

interface ChatSidebarProps {
  selectedContactId: string | null;
  onSelectContact: (contactId: string) => void;
}

export function ChatSidebar({ selectedContactId, onSelectContact }: ChatSidebarProps) {
  const { user } = useAuth();
  const { state } = useSidebar();
  const [searchQuery, setSearchQuery] = useState("");
  const [addContactOpen, setAddContactOpen] = useState(false);
  const { contacts, loading } = useContacts();

  const filteredContacts = contacts.filter((contact) =>
    contact.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    contact.email.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const formatTime = (timestamp?: string) => {
    if (!timestamp) return "";
    try {
      return formatDistanceToNow(new Date(timestamp), {
        addSuffix: true,
        locale: es,
      });
    } catch {
      return "";
    }
  };

  return (
    <>
      <Sidebar className="border-r border-border">
        <SidebarContent>
          {/* Header con perfil */}
          <div className="p-4 border-b border-border bg-[#FBF0ED]">
            <div className="flex items-center gap-3">
              <Avatar className="h-10 w-10 border-2 border-white shadow-sm">
                <AvatarFallback className="bg-primary text-primary-foreground">
                  {user?.name.charAt(0).toUpperCase()}
                </AvatarFallback>
              </Avatar>
              {state === "expanded" && (
                <div className="flex-1 min-w-0">
                  <h2 className="font-semibold text-foreground truncate">
                    {user?.name}
                  </h2>
                  <p className="text-xs text-muted-foreground flex items-center gap-1">
                    <span className="w-2 h-2 rounded-full bg-green-500 inline-block"></span>
                    En línea
                  </p>
                </div>
              )}
            </div>
          </div>

          {/* Barra de búsqueda y botón añadir */}
          {state === "expanded" && (
            <div className="p-3 border-b border-border space-y-2">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                <Input
                  placeholder="Buscar contactos..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="pl-9"
                />
              </div>
              <Button
                onClick={() => setAddContactOpen(true)}
                className="w-full"
                size="sm"
              >
                <UserPlus className="mr-2 h-4 w-4" />
                Añadir Contacto
              </Button>
            </div>
          )}

          {/* Lista de contactos */}
          <SidebarGroup>
            {state === "expanded" && (
              <SidebarGroupLabel className="px-4 py-2 text-xs font-semibold text-muted-foreground">
                Contactos {contacts.length > 0 && `(${contacts.length})`}
              </SidebarGroupLabel>
            )}
            <SidebarGroupContent>
              <ScrollArea className="h-[calc(100vh-280px)]">
                {loading ? (
                  <div className="p-8 text-center">
                    <p className="text-sm text-muted-foreground">Cargando...</p>
                  </div>
                ) : filteredContacts.length === 0 ? (
                  <div className="p-8 text-center">
                    <MessageSquare className="h-12 w-12 text-muted-foreground/50 mx-auto mb-3" />
                    {state === "expanded" && (
                      <>
                        <p className="text-sm font-medium text-muted-foreground mb-1">
                          {searchQuery ? "No se encontraron contactos" : "No hay contactos aún"}
                        </p>
                        <p className="text-xs text-muted-foreground">
                          {searchQuery ? "Intenta con otro término de búsqueda" : "Añade contactos para comenzar a chatear"}
                        </p>
                      </>
                    )}
                  </div>
                ) : (
                  <SidebarMenu>
                    {filteredContacts.map((contact) => (
                      <SidebarMenuItem key={contact.id}>
                        <SidebarMenuButton
                          onClick={() => onSelectContact(contact.contact_id)}
                          className={`h-auto py-3 px-4 hover:bg-muted/50 cursor-pointer ${selectedContactId === contact.contact_id ? "bg-muted" : ""
                            }`}
                        >
                          <div className="flex items-center gap-3 w-full">
                            <Avatar className="h-10 w-10 shrink-0">
                              <AvatarFallback className="bg-secondary text-secondary-foreground">
                                {contact.name.charAt(0).toUpperCase()}
                              </AvatarFallback>
                            </Avatar>
                            {state === "expanded" && (
                              <div className="flex-1 min-w-0">
                                <div className="flex items-center justify-between mb-1">
                                  <h3 className="font-semibold text-sm text-foreground truncate">
                                    {contact.name}
                                  </h3>
                                  {contact.lastMessageTime && (
                                    <span className="text-xs text-muted-foreground">
                                      {formatTime(contact.lastMessageTime)}
                                    </span>
                                  )}
                                </div>
                                <div className="flex items-center justify-between">
                                  <p className="text-xs text-muted-foreground truncate">
                                    {contact.lastMessage || "Sin mensajes"}
                                  </p>
                                  {contact.unread > 0 && (
                                    <span className="bg-primary text-primary-foreground text-xs rounded-full h-5 w-5 flex items-center justify-center shrink-0 ml-2">
                                      {contact.unread}
                                    </span>
                                  )}
                                </div>
                              </div>
                            )}
                          </div>
                        </SidebarMenuButton>
                      </SidebarMenuItem>
                    ))}
                  </SidebarMenu>
                )}
              </ScrollArea>
            </SidebarGroupContent>
          </SidebarGroup>
        </SidebarContent>
      </Sidebar>

      <AddContactDialog open={addContactOpen} onOpenChange={setAddContactOpen} />
    </>
  );
}
