import { useState, useRef, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { MessageSquare, Send, LogOut, Menu } from "lucide-react";
import { useAuth } from "@/contexts/AuthContext";
import { ScrollArea } from "@/components/ui/scroll-area";

interface Message {
  id: string;
  text: string;
  sender: "user" | "bot";
  timestamp: Date;
}

const Chat = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      text: "¡Hola! Bienvenido a PictoAmigos. Estoy aquí para ayudarte con la comunicación mediante pictogramas.",
      sender: "bot",
      timestamp: new Date(),
    },
  ]);
  const [inputMessage, setInputMessage] = useState("");
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!user) {
      navigate("/auth");
    }
  }, [user, navigate]);

  useEffect(() => {
    scrollRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSendMessage = () => {
    if (!inputMessage.trim()) return;

    const newMessage: Message = {
      id: Date.now().toString(),
      text: inputMessage,
      sender: "user",
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, newMessage]);
    setInputMessage("");

    // Simular respuesta del bot
    setTimeout(() => {
      const botResponse: Message = {
        id: (Date.now() + 1).toString(),
        text: "Gracias por tu mensaje. En esta versión de demostración, pronto podrás comunicarte usando pictogramas. ¿En qué más puedo ayudarte?",
        sender: "bot",
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, botResponse]);
    }, 1000);
  };

  const handleLogout = () => {
    logout();
    navigate("/");
  };

  const formatTime = (date: Date) => {
    return date.toLocaleTimeString("es-ES", {
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  if (!user) return null;

  return (
    <div className="flex flex-col h-screen bg-background">
      {/* Header */}
      <header className="bg-secondary text-secondary-foreground px-4 py-3 flex items-center justify-between shadow-sm">
        <div className="flex items-center gap-3">
          <Avatar className="h-10 w-10">
            <AvatarFallback className="bg-primary text-primary-foreground">
              {user.name.charAt(0).toUpperCase()}
            </AvatarFallback>
          </Avatar>
          <div>
            <h2 className="font-semibold">{user.name}</h2>
            <p className="text-xs opacity-80">En línea</p>
          </div>
        </div>
        <Button
          variant="ghost"
          size="icon"
          onClick={handleLogout}
          className="text-secondary-foreground hover:bg-secondary-foreground/10"
        >
          <LogOut className="h-5 w-5" />
        </Button>
      </header>

      {/* Chat Header */}
      <div className="bg-card border-b px-4 py-3 flex items-center gap-3">
        <MessageSquare className="h-6 w-6 text-primary" />
        <div>
          <h3 className="font-semibold text-foreground">PictoAmigos Asistente</h3>
          <p className="text-xs text-muted-foreground">Siempre disponible</p>
        </div>
      </div>

      {/* Messages */}
      <ScrollArea className="flex-1 p-4">
        <div className="space-y-4 max-w-4xl mx-auto">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${
                message.sender === "user" ? "justify-end" : "justify-start"
              }`}
            >
              <div
                className={`max-w-[70%] rounded-2xl px-4 py-2 ${
                  message.sender === "user"
                    ? "bg-primary text-primary-foreground rounded-br-sm"
                    : "bg-muted text-foreground rounded-bl-sm"
                }`}
              >
                <p className="text-sm">{message.text}</p>
                <p
                  className={`text-xs mt-1 ${
                    message.sender === "user"
                      ? "text-primary-foreground/70"
                      : "text-muted-foreground"
                  }`}
                >
                  {formatTime(message.timestamp)}
                </p>
              </div>
            </div>
          ))}
          <div ref={scrollRef} />
        </div>
      </ScrollArea>

      {/* Input */}
      <div className="bg-card border-t p-4">
        <div className="max-w-4xl mx-auto flex gap-2">
          <Input
            placeholder="Escribe un mensaje..."
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyPress={(e) => {
              if (e.key === "Enter") {
                handleSendMessage();
              }
            }}
            className="flex-1"
          />
          <Button
            onClick={handleSendMessage}
            size="icon"
            disabled={!inputMessage.trim()}
          >
            <Send className="h-4 w-4" />
          </Button>
        </div>
      </div>
    </div>
  );
};

export default Chat;
