import { useState } from "react";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Input } from "@/components/ui/input";
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
import { Search, MessageSquare } from "lucide-react";
import { useAuth } from "@/contexts/AuthContext";

interface Contact {
  id: string;
  name: string;
  lastMessage: string;
  timestamp: string;
  unread: number;
}

export function ChatSidebar() {
  const { user } = useAuth();
  const { state } = useSidebar();
  const [searchQuery, setSearchQuery] = useState("");

  // Lista de contactos vacía por ahora - se puede expandir en el futuro
  const contacts: Contact[] = [];

  const filteredContacts = contacts.filter((contact) =>
    contact.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
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

        {/* Barra de búsqueda */}
        {state === "expanded" && (
          <div className="p-3 border-b border-border">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <Input
                placeholder="Buscar contactos..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-9"
              />
            </div>
          </div>
        )}

        {/* Lista de contactos */}
        <SidebarGroup>
          {state === "expanded" && (
            <SidebarGroupLabel className="px-4 py-2 text-xs font-semibold text-muted-foreground">
              Contactos
            </SidebarGroupLabel>
          )}
          <SidebarGroupContent>
            <ScrollArea className="h-[calc(100vh-240px)]">
              {filteredContacts.length === 0 ? (
                <div className="p-8 text-center">
                  <MessageSquare className="h-12 w-12 text-muted-foreground/50 mx-auto mb-3" />
                  {state === "expanded" && (
                    <>
                      <p className="text-sm font-medium text-muted-foreground mb-1">
                        No hay contactos aún
                      </p>
                      <p className="text-xs text-muted-foreground">
                        Tus conversaciones aparecerán aquí
                      </p>
                    </>
                  )}
                </div>
              ) : (
                <SidebarMenu>
                  {filteredContacts.map((contact) => (
                    <SidebarMenuItem key={contact.id}>
                      <SidebarMenuButton
                        asChild
                        className="h-auto py-3 px-4 hover:bg-muted/50 cursor-pointer"
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
                                <span className="text-xs text-muted-foreground">
                                  {contact.timestamp}
                                </span>
                              </div>
                              <div className="flex items-center justify-between">
                                <p className="text-xs text-muted-foreground truncate">
                                  {contact.lastMessage}
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
  );
}
