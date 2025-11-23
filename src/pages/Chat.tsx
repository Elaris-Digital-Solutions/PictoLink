import { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { MessageSquare, Send, LogOut, Mic, MicOff } from 'lucide-react';
import { useAuth } from '@/contexts/AuthContext';
import { ScrollArea } from '@/components/ui/scroll-area';
import { SidebarProvider, SidebarTrigger } from '@/components/ui/sidebar';
import { ChatSidebar } from '@/components/ChatSidebar';
import { useMessages } from '@/hooks/useMessages';
import { useContacts } from '@/hooks/useContacts';
import { useSpeechRecognition, useSpeechSynthesis } from '@/hooks/useSpeech';
import { Switch } from '@/components/ui/switch';
import { Label } from '@/components/ui/label';

const Chat = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const [selectedContactId, setSelectedContactId] = useState<string | null>(null);
  const [inputMessage, setInputMessage] = useState('');
  const [autoReadEnabled, setAutoReadEnabled] = useState(false);

  const scrollRef = useRef<HTMLDivElement>(null);
  const prevMessagesLengthRef = useRef(0);

  const { messages, sendMessage } = useMessages(selectedContactId);
  const { contacts } = useContacts();

  // Speech hooks
  const {
    isListening,
    transcript,
    error: speechError,
    isSupported: isSpeechRecognitionSupported,
    startListening,
    stopListening,
    resetTranscript,
  } = useSpeechRecognition();
  const { speak, isSupported: isSpeechSynthesisSupported } = useSpeechSynthesis();

  // Redirect unauthenticated users
  useEffect(() => {
    if (!user) navigate('/auth');
  }, [user, navigate]);

  // Auto‑scroll to newest message
  useEffect(() => {
    scrollRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Update input when transcript changes (real‑time)
  useEffect(() => {
    if (transcript) setInputMessage(transcript);
  }, [transcript]);

  // Auto‑read incoming messages when switch is enabled
  useEffect(() => {
    if (!autoReadEnabled || !isSpeechSynthesisSupported || !user) return;
    if (messages.length > prevMessagesLengthRef.current) {
      const latest = messages[messages.length - 1];
      if (latest.sender_id !== user.id) speak(latest.content);
    }
    prevMessagesLengthRef.current = messages.length;
  }, [messages, autoReadEnabled, isSpeechSynthesisSupported, user, speak]);

  const handleSendMessage = async () => {
    if (!inputMessage.trim() || !selectedContactId) return;
    try {
      await sendMessage(inputMessage);
      setInputMessage('');
      resetTranscript();
    } catch (e) {
      console.error('Error sending message:', e);
    }
  };

  const handleLogout = async () => {
    try {
      await logout();
      navigate('/');
    } catch (e) {
      console.error('Error logging out:', e);
    }
  };

  const toggleVoiceRecognition = () => {
    if (isListening) {
      stopListening();
      // Ensure the final transcript is captured before updating input
      setTimeout(() => {
        if (transcript) setInputMessage(transcript);
      }, 0);
    } else {
      resetTranscript();
      startListening();
    }
  };

  const formatTime = (date: string) =>
    new Date(date).toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' });

  const selectedContact = contacts.find((c) => c.contact_id === selectedContactId);

  if (!user) return null;

  return (
    <SidebarProvider defaultOpen={true}>
      <div className="flex min-h-screen w-full bg-background">
        <ChatSidebar selectedContactId={selectedContactId} onSelectContact={setSelectedContactId} />
        <div className="flex flex-col flex-1 min-w-0">
          {/* Header */}
          <header className="bg-white text-foreground px-4 py-3 flex items-center justify-between shadow-sm border-b border-border">
            <div className="flex items-center gap-3">
              <SidebarTrigger className="text-foreground hover:bg-gray-100" />
              <div className="h-10 w-10 rounded-full bg-[#FBF0ED] flex items-center justify-center">
                <MessageSquare className="h-6 w-6 text-primary" />
              </div>
              <div>
                <h3 className="font-semibold text-foreground">
                  {selectedContact ? selectedContact.name : 'PictoLink'}
                </h3>
                <p className="text-xs text-muted-foreground flex items-center gap-1">
                  {selectedContact ? (
                    <>
                      <span className="w-2 h-2 rounded-full bg-green-500 inline-block" /> En línea
                    </>
                  ) : (
                    'Selecciona un contacto para chatear'
                  )}
                </p>
              </div>
            </div>
            <div className="flex items-center gap-4">
              {isSpeechSynthesisSupported && (
                <div className="flex items-center gap-2">
                  <Switch id="auto-read" checked={autoReadEnabled} onCheckedChange={setAutoReadEnabled} />
                  <Label htmlFor="auto-read" className="text-sm cursor-pointer">
                    Lectura automática
                  </Label>
                </div>
              )}
              <Button
                variant="ghost"
                size="icon"
                onClick={handleLogout}
                className="text-muted-foreground hover:text-destructive hover:bg-destructive/10 transition-colors"
              >
                <LogOut className="h-5 w-5" />
              </Button>
            </div>
          </header>

          {/* Messages */}
          <ScrollArea className="flex-1 p-4">
            <div className="space-y-4 max-w-4xl mx-auto">
              {!selectedContactId ? (
                <div className="flex flex-col items-center justify-center h-[calc(100vh-200px)] text-center">
                  <MessageSquare className="h-20 w-20 text-muted-foreground/30 mb-4" />
                  <h3 className="text-lg font-semibold text-foreground mb-2">Bienvenido a PictoLink</h3>
                  <p className="text-sm text-muted-foreground max-w-md">
                    Selecciona un contacto del sidebar para comenzar a chatear, o añade nuevos contactos para expandir tu red de comunicación.
                  </p>
                </div>
              ) : messages.length === 0 ? (
                <div className="flex flex-col items-center justify-center h-[calc(100vh-200px)] text-center">
                  <MessageSquare className="h-20 w-20 text-muted-foreground/30 mb-4" />
                  <h3 className="text-lg font-semibold text-foreground mb-2">Sin mensajes aún</h3>
                  <p className="text-sm text-muted-foreground max-w-md">
                    Envía el primer mensaje a {selectedContact?.name} para comenzar la conversación.
                  </p>
                </div>
              ) : (
                messages.map((msg) => (
                  <div key={msg.id} className={`flex ${msg.sender_id === user.id ? 'justify-end' : 'justify-start'}`}>
                    <div
                      className={`max-w-[70%] rounded-2xl px-5 py-3 shadow-sm ${msg.sender_id === user.id
                        ? 'bg-primary text-primary-foreground rounded-br-sm'
                        : 'bg-[#FBF0ED] text-foreground rounded-bl-sm border border-orange-100'
                        }`}
                    >
                      <p className="text-sm">{msg.content}</p>
                      <p className={`text-xs mt-1 ${msg.sender_id === user.id ? 'text-primary-foreground/70' : 'text-muted-foreground'}`}>
                        {formatTime(msg.created_at)}
                      </p>
                    </div>
                  </div>
                ))
              )}
              <div ref={scrollRef} />
            </div>
          </ScrollArea>

          {/* Input area */}
          <div className="bg-card border-t p-4">
            <div className="max-w-4xl mx-auto flex gap-2">
              <Input
                placeholder={
                  speechError
                    ? speechError
                    : selectedContactId
                      ? isListening
                        ? 'Escuchando...'
                        : 'Escribe un mensaje...'
                      : 'Selecciona un contacto primero...'
                }
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyPress={(e) => {
                  if (e.key === 'Enter' && selectedContactId) handleSendMessage();
                }}
                className="flex-1"
                disabled={!selectedContactId}
              />
              {speechError && <p className="text-xs text-red-5 mt-1">{speechError}</p>}
              {isSpeechRecognitionSupported && (
                <Button
                  onClick={toggleVoiceRecognition}
                  size="icon"
                  variant={isListening ? 'default' : 'outline'}
                  disabled={!selectedContactId}
                  className={isListening ? 'animate-pulse' : ''}
                >
                  {isListening ? <MicOff className="h-4 w-4" /> : <Mic className="h-4 w-4" />}
                </Button>
              )}
              <Button onClick={handleSendMessage} size="icon" disabled={!inputMessage.trim() || !selectedContactId}>
                <Send className="h-4 w-4" />
              </Button>
            </div>
          </div>
        </div>
      </div>
    </SidebarProvider>
  );
};

export default Chat;
