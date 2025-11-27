import { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { MessageSquare, Send, LogOut, Mic, MicOff, X } from 'lucide-react';
import { useAuth } from '@/contexts/AuthContext';
import { ScrollArea } from '@/components/ui/scroll-area';
import { SidebarProvider, SidebarTrigger } from '@/components/ui/sidebar';
import { ChatSidebar } from '@/components/ChatSidebar';
import { PictogramSidebar } from '@/components/PictogramSidebar';
import { useMessages } from '@/hooks/useMessages';
import { useContacts } from '@/hooks/useContacts';
import { useSpeechRecognition, useSpeechSynthesis } from '@/hooks/useSpeech';
import { Switch } from '@/components/ui/switch';
import { Label } from '@/components/ui/label';
import { type Pictogram } from '@/lib/pictograms';
import { convertTextToPictos, convertPictosToText, getAutocompleteSuggestions } from '@/lib/api';
import styles from './Chat.module.css';

const Chat = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const [selectedContactId, setSelectedContactId] = useState<string | null>(null);
  const [inputMessage, setInputMessage] = useState('');
  const [autoReadEnabled, setAutoReadEnabled] = useState(false);
  const [selectedPictograms, setSelectedPictograms] = useState<Pictogram[]>([]);
  const [suggestions, setSuggestions] = useState<string[]>([]);

  const scrollRef = useRef<HTMLDivElement>(null);

  const { messages, sendMessage } = useMessages(selectedContactId);
  const { contacts, loading: contactsLoading, addContact } = useContacts();

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
    if (transcript && selectedPictograms.length === 0) {
      setInputMessage(transcript);
    }
  }, [transcript, selectedPictograms.length]);

  const handleSendMessage = async () => {
    if (!selectedContactId) return;

    // Priority 1: Send pictograms if any are selected
    if (selectedPictograms.length > 0) {
      try {
        console.log('Generating text from pictograms...');
        const generatedText = await convertPictosToText(selectedPictograms);
        console.log('Generated text:', generatedText);

        const ids = selectedPictograms.map(p => p.id).join(',');
        const labels = selectedPictograms.map(p => p.labels.es).join(' ');
        const pictogramMessage = `[pictograms:${ids}:${labels}|${generatedText}]`;

        await sendMessage(pictogramMessage);
        setSelectedPictograms([]);
        console.log('Pictogram message sent successfully');
      } catch (e) {
        console.error('Error sending pictograms:', e);
        alert('Error al enviar pictogramas: ' + (e as Error).message);
      }
      return;
    }

    // Priority 2: Send text message (convert to pictograms if possible)
    if (!inputMessage.trim()) {
      console.log('Validation failed: empty message');
      return;
    }

    let messageToSend = inputMessage;

    try {
      console.log('Attempting to convert text to pictos...');
      const foundPictograms = await convertTextToPictos(inputMessage.trim());
      console.log('Pictogramas encontrados (API):', foundPictograms);

      if (foundPictograms.length > 0) {
        const ids = foundPictograms.map(p => p.id);
        const labels = foundPictograms.map(p => p.labels.es);
        messageToSend = `[pictograms:${ids.join(',')}:${labels.join(' ')}|${inputMessage.trim()}]`;
        console.log('Mensaje compuesto preparado:', messageToSend);
      }
    } catch (e) {
      console.error('Error converting text to pictograms (falling back to text):', e);
    }

    try {
      console.log('Sending message to Supabase:', messageToSend);
      await sendMessage(messageToSend);
      console.log('Message sent successfully');
      setInputMessage('');
      resetTranscript();
    } catch (e) {
      console.error('Error sending message:', e);
      alert('Error al enviar mensaje: ' + (e as Error).message);
    }
  };

  const handleAddPictogram = (pictogram: Pictogram) => {
    setSelectedPictograms(prev => [...prev, pictogram]);
    setInputMessage(''); // Clear text input when adding pictogram
  };

  const handleRemovePictogram = (pictogramId: number) => {
    setSelectedPictograms(prev => prev.filter(p => p.id !== pictogramId));
  };

  const handleClearAllPictograms = () => {
    setSelectedPictograms([]);
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

  const renderMessageContent = (content: string) => {
    // Check for compound pictograms first
    // Format: [pictograms:IDS:LABELS] or [pictograms:IDS:LABELS|GENERATED_TEXT]
    const compoundMatch = content.match(/^\[pictograms:([\d,]+):([^|]+)(?:\|(.+))?\]$/);
    if (compoundMatch) {
      const [, idsString, labelsString, generatedText] = compoundMatch;
      const ids = idsString.split(',').map(id => parseInt(id));
      const labels = labelsString.split(' ');

      return (
        <div className="flex flex-col gap-3">
          <div className="flex gap-2 flex-wrap justify-center">
            {ids.map((id, index) => (
              <div key={`${id}-${index}`} className="flex flex-col items-center gap-1">
                <img
                  src={`https://static.arasaac.org/pictograms/${id}/${id}_500.png`}
                  alt={labels[index] || `Pictograma ${id}`}
                  className="w-12 h-12 object-contain"
                />
                <p className="text-xs text-center max-w-[60px] truncate">{labels[index] || `Pictograma ${id}`}</p>
              </div>
            ))}
          </div>
          {generatedText && (
            <div className="bg-white/50 p-2 rounded text-center border border-black/5">
              <p className="text-sm font-medium text-foreground">{generatedText}</p>
            </div>
          )}
        </div>
      );
    }

    // Check for single pictogram
    const pictogramMatch = content.match(/^\[pictogram:(\d+):(.+)\]$/);
    if (pictogramMatch) {
      const [, id, label] = pictogramMatch;
      return (
        <div className="flex flex-col items-center gap-2">
          <img
            src={`https://static.arasaac.org/pictograms/${id}/${id}_500.png`}
            alt={label}
            className="w-16 h-16 object-contain"
          />
          <p className="text-xs text-center">{label}</p>
        </div>
      );
    }
    return <p className="text-sm">{content}</p>;
  };

  const selectedContact = contacts.find((c) => c.contact_id === selectedContactId);

  if (!user) return null;

  return (
    <SidebarProvider defaultOpen={true}>
      <div className="flex h-screen w-full bg-background overflow-hidden">
        <ChatSidebar
          selectedContactId={selectedContactId}
          onSelectContact={setSelectedContactId}
          contacts={contacts}
          loading={contactsLoading}
          onAddContact={addContact}
        />
        <div className="flex flex-col flex-1 min-w-0 relative">
          {/* Header */}
          <header className="bg-white text-foreground p-4 flex items-center justify-between shadow-sm border-b border-border flex-none z-10">
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
          <ScrollArea className={`flex-1 p-4 ${styles.chatBackground}`}>
            <div className={`space-y-4 max-w-4xl mx-auto pb-4 ${styles.chatContent}`}>
              {!selectedContactId ? (
                <div className="flex flex-col items-center justify-center h-full text-center py-20">
                  <MessageSquare className="h-20 w-20 text-muted-foreground/30 mb-4" />
                  <h3 className="text-lg font-semibold text-foreground mb-2">Bienvenido a PictoLink</h3>
                  <p className="text-sm text-muted-foreground max-w-md">
                    Selecciona un contacto del sidebar para comenzar a chatear, o añade nuevos contactos para expandir tu red de comunicación.
                  </p>
                </div>
              ) : messages.length === 0 ? (
                <div className="flex flex-col items-center justify-center h-full text-center py-20">
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
                      {renderMessageContent(msg.content)}
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

          {/* Message Composition Area */}
          <div className="bg-card border-t p-4 flex-none">
            <div className="max-w-4xl mx-auto space-y-3">
              {/* Selected Pictograms Display */}
              {selectedPictograms.length > 0 && (
                <div className="p-3 bg-gray-50 rounded-lg border border-gray-200">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm font-medium text-foreground">
                      Mensaje con pictogramas ({selectedPictograms.length}):
                    </span>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={handleClearAllPictograms}
                      className="h-7 text-xs"
                    >
                      Limpiar todo
                    </Button>
                  </div>
                  <div className="flex gap-2 flex-wrap">
                    {selectedPictograms.map((picto, index) => (
                      <div
                        key={`${picto.id}-${index}`}
                        className="relative group bg-white p-2 rounded-lg border border-gray-300 hover:border-primary transition-colors"
                      >
                        <img
                          src={picto.image_urls.png_color}
                          alt={picto.labels?.es || 'Pictograma'}
                          className="w-12 h-12 object-contain"
                        />
                        <button
                          onClick={() => handleRemovePictogram(picto.id)}
                          className="absolute -top-1 -right-1 bg-red-500 hover:bg-red-600 text-white rounded-full p-0.5 opacity-0 group-hover:opacity-100 transition-opacity"
                        >
                          <X className="h-3 w-3" />
                        </button>
                        <span className="text-xs text-center block mt-1 max-w-[60px] truncate">
                          {picto.labels?.es}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Autocomplete Suggestions */}
              {suggestions.length > 0 && selectedPictograms.length === 0 && (
                <div className="relative">
                  <div className="absolute bottom-full left-0 mb-2 w-64 bg-white border border-gray-200 rounded-lg shadow-lg z-50 overflow-hidden">
                    {suggestions.map((suggestion, index) => (
                      <button
                        key={index}
                        className="w-full text-left px-4 py-2 hover:bg-gray-100 text-sm"
                        onClick={() => {
                          const words = inputMessage.split(' ');
                          words.pop();
                          words.push(suggestion);
                          setInputMessage(words.join(' ') + ' ');
                          setSuggestions([]);
                        }}
                      >
                        {suggestion}
                      </button>
                    ))}
                  </div>
                </div>
              )}

              {/* Text Input and Send Button */}
              <div className="flex gap-2">
                <Input
                  placeholder={
                    selectedPictograms.length > 0
                      ? "Borra los pictogramas para escribir texto"
                      : speechError
                        ? speechError
                        : selectedContactId
                          ? isListening
                            ? 'Escuchando...'
                            : 'Escribe un mensaje...'
                          : 'Selecciona un contacto primero...'
                  }
                  value={inputMessage}
                  onChange={(e) => {
                    if (selectedPictograms.length === 0) {
                      const newVal = e.target.value;
                      setInputMessage(newVal);

                      // Debounced autocomplete
                      const lastWord = newVal.split(' ').pop();
                      if (lastWord && lastWord.length >= 2) {
                        getAutocompleteSuggestions(lastWord).then(setSuggestions);
                      } else {
                        setSuggestions([]);
                      }
                    }
                  }}
                  onKeyPress={(e) => {
                    if (e.key === 'Enter' && selectedContactId) handleSendMessage();
                  }}
                  className="flex-1"
                  disabled={!selectedContactId || selectedPictograms.length > 0}
                />
                {isSpeechRecognitionSupported && selectedPictograms.length === 0 && (
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
                <Button
                  onClick={handleSendMessage}
                  size="icon"
                  disabled={
                    !selectedContactId ||
                    (selectedPictograms.length === 0 && !inputMessage.trim())
                  }
                >
                  <Send className="h-4 w-4" />
                </Button>
              </div>
            </div>
          </div>
        </div>

        {/* Pictogram Sidebar (Right) */}
        <div className="w-80 flex-shrink-0 hidden md:block">
          <PictogramSidebar
            onSelectPictogram={handleAddPictogram}
            selectedPictograms={selectedPictograms}
          />
        </div>
      </div>
    </SidebarProvider>
  );
};

export default Chat;
