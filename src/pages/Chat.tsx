import { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { MessageSquare, Send, LogOut, Mic, MicOff, Image, X, Plus } from 'lucide-react';
import { useAuth } from '@/contexts/AuthContext';
import { ScrollArea } from '@/components/ui/scroll-area';
import { SidebarProvider, SidebarTrigger } from '@/components/ui/sidebar';
import { ChatSidebar } from '@/components/ChatSidebar';
import { useMessages } from '@/hooks/useMessages';
import { useContacts } from '@/hooks/useContacts';
import { useSpeechRecognition, useSpeechSynthesis } from '@/hooks/useSpeech';
import { Switch } from '@/components/ui/switch';
import { Label } from '@/components/ui/label';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { searchPictograms, type Pictogram, getPictogramCategories, getPictogramsByCategory } from '@/lib/pictograms';
import { convertTextToPictos, convertPictosToText, getAutocompleteSuggestions } from '@/lib/api';

const Chat = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const [selectedContactId, setSelectedContactId] = useState<string | null>(null);
  const [inputMessage, setInputMessage] = useState('');
  const [autoReadEnabled, setAutoReadEnabled] = useState(false);
  const [pictograms, setPictograms] = useState<Pictogram[]>([]);
  const [showPictograms, setShowPictograms] = useState(false);
  const [selectedPictograms, setSelectedPictograms] = useState<Pictogram[]>([]);
  const [messageMode, setMessageMode] = useState<'text' | 'pictograms'>('text');
  const [categories, setCategories] = useState<string[]>([]);
  const [categoryPictograms, setCategoryPictograms] = useState<Record<string, Pictogram[]>>({});
  const [selectedCategory, setSelectedCategory] = useState<string>('');
  const [suggestions, setSuggestions] = useState<string[]>([]);

  const scrollRef = useRef<HTMLDivElement>(null);
  const prevMessagesLengthRef = useRef(0);
  const pictogramMenuRef = useRef<HTMLDivElement>(null);

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

  // Load categories when component mounts
  useEffect(() => {
    const loadCategories = async () => {
      const cats = getPictogramCategories();
      setCategories(cats);
      setSelectedCategory(cats[0]); // Select first category by default
    };
    loadCategories();
  }, []);

  // Load pictograms for selected category
  useEffect(() => {
    const loadCategoryPictograms = async () => {
      if (selectedCategory && messageMode === 'pictograms') {
        try {
          const picts = await getPictogramsByCategory(selectedCategory, 24);
          setCategoryPictograms(prev => ({
            ...prev,
            [selectedCategory]: picts
          }));
        } catch (e) {
          console.error('Error loading category pictograms:', e);
        }
      }
    };
    loadCategoryPictograms();
  }, [selectedCategory, messageMode]);

  const handleSendMessage = async () => {
    console.log('handleSendMessage called', { messageMode, inputMessage, selectedContactId });
    if (messageMode === 'text') {
      if (!inputMessage.trim() || !selectedContactId) {
        console.log('Validation failed: empty message or no contact');
        return;
      }

      let messageToSend = inputMessage;

      try {
        console.log('Attempting to convert text to pictos...');
        // Convert text to pictograms using the backend API
        const foundPictograms = await convertTextToPictos(inputMessage.trim());
        console.log('Pictogramas encontrados (API):', foundPictograms);

        if (foundPictograms.length > 0) {
          // Enviar como mensaje compuesto de pictogramas
          const ids = foundPictograms.map(p => p.id);
          const labels = foundPictograms.map(p => p.labels.es);
          messageToSend = `[pictograms:${ids.join(',')}:${labels.join(' ')}]`;
          console.log('Mensaje compuesto preparado:', messageToSend);
        }
      } catch (e) {
        console.error('Error converting text to pictograms (falling back to text):', e);
        // Fallback to sending original text is implicit as messageToSend is already set
      }

      try {
        console.log('Sending message to Supabase:', messageToSend);
        await sendMessage(messageToSend);
        console.log('Message sent successfully');
        setInputMessage('');
        resetTranscript();
        setPictograms([]);
        setShowPictograms(false);
      } catch (e) {
        console.error('Error sending message:', e);
        alert('Error al enviar mensaje: ' + (e as Error).message);
      }
    } else {
      // Modo pictogramas - enviar selección actual
      if (selectedPictograms.length === 0 || !selectedContactId) return;
      try {
        const pictogramMessage = `[pictograms:${selectedPictograms.map(p => p.id).join(',')}:${selectedPictograms.map(p => p.labels.es).join(' ')}]`;
        await sendMessage(pictogramMessage);
        setSelectedPictograms([]);
        setPictograms([]);
        setShowPictograms(false);
      } catch (e) {
        console.error('Error sending pictograms:', e);
      }
    }
  };

  const handleSearchPictograms = async () => {
    if (!inputMessage.trim()) return;
    try {
      const results = await searchPictograms(inputMessage.trim());
      setPictograms(results);
      setShowPictograms(true);
    } catch (e) {
      console.error('Error searching pictograms:', e);
    }
  };

  const handleSendPictogram = async (pictogram: Pictogram) => {
    try {
      const pictogramMessage = `[pictogram:${pictogram.id}:${pictogram.labels?.es || 'Pictograma'}]`;
      await sendMessage(pictogramMessage);
      setInputMessage('');
      setPictograms([]);
      setShowPictograms(false);
      resetTranscript();
    } catch (e) {
      console.error('Error sending pictogram:', e);
    }
  };

  const handleAddPictogram = (pictogram: Pictogram) => {
    if (!selectedPictograms.find(p => p.id === pictogram.id)) {
      setSelectedPictograms(prev => [...prev, pictogram]);
    }
  };

  const handleRemovePictogram = (pictogramId: number) => {
    setSelectedPictograms(prev => prev.filter(p => p.id !== pictogramId));
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
    const compoundMatch = content.match(/^\[pictograms:([\d,]+):(.+)\]$/);
    if (compoundMatch) {
      const [, idsString, labelsString] = compoundMatch;
      const ids = idsString.split(',').map(id => parseInt(id));
      const labels = labelsString.split(' ');

      return (
        <div className="flex flex-col gap-2">
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

  // Close pictogram menu when clicking outside
  const handleOutsideClick = (event: MouseEvent) => {
    if (
      pictogramMenuRef.current &&
      !pictogramMenuRef.current.contains(event.target as Node)
    ) {
      setShowPictograms(false);
    }
  };

  useEffect(() => {
    if (showPictograms) {
      document.addEventListener('mousedown', handleOutsideClick);
    } else {
      document.removeEventListener('mousedown', handleOutsideClick);
    }

    return () => {
      document.removeEventListener('mousedown', handleOutsideClick);
    };
  }, [showPictograms]);

  if (!user) return null;

  return (
    <SidebarProvider defaultOpen={true}>
      <div className="flex h-screen w-full bg-background overflow-hidden">
        <ChatSidebar selectedContactId={selectedContactId} onSelectContact={setSelectedContactId} />
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
          <ScrollArea className="flex-1 p-4">
            <div className="space-y-4 max-w-4xl mx-auto pb-4">
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

          {/* Input area */}
          <div className="bg-card border-t p-4 flex-none relative">
            {/* Pictogram Menu */}
            {showPictograms && (
              <div
                ref={pictogramMenuRef}
                className="absolute bottom-full left-0 w-full h-[50vh] bg-white shadow-lg border-t border-border z-50 overflow-y-auto"
              >
                <div className="p-4">
                  <h4 className="text-lg font-semibold mb-4">Selecciona un pictograma</h4>
                  <div className="grid grid-cols-4 gap-4">
                    {pictograms.map((pictogram) => (
                      <button
                        key={pictogram.id}
                        onClick={() => handleAddPictogram(pictogram)}
                        className="flex flex-col items-center gap-2 p-2 border rounded-lg hover:bg-gray-100"
                      >
                        <img
                          src={pictogram.image_urls.png_color}
                          alt={pictogram.labels?.es || 'Pictograma'}
                          className="w-16 h-16 object-contain"
                        />
                        <span className="text-sm text-center truncate">
                          {pictogram.labels?.es || 'Sin etiqueta'}
                        </span>
                      </button>
                    ))}
                  </div>
                </div>
              </div>
            )}

            <div className="max-w-4xl mx-auto">
              <Tabs value={messageMode} onValueChange={(value) => setMessageMode(value as 'text' | 'pictograms')}>
                <TabsList className="grid w-full grid-cols-2 mb-4">
                  <TabsTrigger value="text">Texto → Pictogramas</TabsTrigger>
                  <TabsTrigger value="pictograms">Solo Pictogramas</TabsTrigger>
                </TabsList>

                <TabsContent value="text" className="space-y-4 relative">
                  {/* Autocomplete Suggestions */}
                  {suggestions.length > 0 && (
                    <div className="absolute bottom-full left-0 mb-2 w-64 bg-white border border-gray-200 rounded-lg shadow-lg z-50 overflow-hidden">
                      {suggestions.map((suggestion, index) => (
                        <button
                          key={index}
                          className="w-full text-left px-4 py-2 hover:bg-gray-100 text-sm"
                          onClick={() => {
                            const words = inputMessage.split(' ');
                            words.pop(); // Remove partial word
                            words.push(suggestion);
                            setInputMessage(words.join(' ') + ' ');
                            setSuggestions([]);
                          }}
                        >
                          {suggestion}
                        </button>
                      ))}
                    </div>
                  )}

                  <div className="flex gap-2">
                    <Input
                      placeholder={
                        speechError
                          ? speechError
                          : selectedContactId
                            ? isListening
                              ? 'Escuchando...'
                              : 'Escribe una frase para convertir a pictogramas...'
                            : 'Selecciona un contacto primero...'
                      }
                      value={inputMessage}
                      onChange={(e) => {
                        const newVal = e.target.value;
                        setInputMessage(newVal);

                        // Debounced autocomplete
                        const lastWord = newVal.split(' ').pop();
                        if (lastWord && lastWord.length >= 2) {
                          getAutocompleteSuggestions(lastWord).then(setSuggestions);
                        } else {
                          setSuggestions([]);
                        }
                      }}
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
                </TabsContent>

                <TabsContent value="pictograms" className="space-y-4">
                  {/* Selector de categorías */}
                  <div className="space-y-2">
                    <h4 className="text-sm font-medium">Categorías:</h4>
                    <div className="flex gap-2 flex-wrap">
                      {categories.map((category) => (
                        <button
                          key={category}
                          onClick={() => setSelectedCategory(category)}
                          className={`px-3 py-1 rounded-full text-sm ${selectedCategory === category
                            ? 'bg-primary text-primary-foreground'
                            : 'bg-gray-100 hover:bg-gray-200'
                            }`}
                        >
                          {category.charAt(0).toUpperCase() + category.slice(1)}
                        </button>
                      ))}
                    </div>
                  </div>

                  {/* Pictogramas de la categoría seleccionada */}
                  {selectedCategory && categoryPictograms[selectedCategory] && (
                    <div className="space-y-2">
                      <h4 className="text-sm font-medium">Pictogramas de "{selectedCategory}":</h4>
                      <div className="grid grid-cols-6 gap-2 max-h-64 overflow-y-auto">
                        {categoryPictograms[selectedCategory].map((pictogram) => (
                          <button
                            key={pictogram.id}
                            onClick={() => handleAddPictogram(pictogram)}
                            className={`flex flex-col items-center gap-1 p-2 rounded-lg border hover:bg-gray-50 transition-colors ${selectedPictograms.some(p => p.id === pictogram.id)
                              ? 'border-green-500 bg-green-50'
                              : 'border-gray-200'
                              }`}
                          >
                            <img
                              src={pictogram.image_urls.png_color}
                              alt={pictogram.labels?.es || 'Pictograma'}
                              className="w-12 h-12 object-contain"
                            />
                            <p className="text-xs text-center truncate w-full">{pictogram.labels?.es || 'Sin etiqueta'}</p>
                          </button>
                        ))}
                      </div>
                    </div>
                  )}
                  {/* Pictogramas seleccionados */}
                  {/* Pictogramas seleccionados */}
                  <div className="space-y-2">
                    <h4 className="text-sm font-medium">Mensaje compuesto:</h4>
                    <div className="flex gap-2 flex-wrap p-3 bg-gray-50 rounded-lg min-h-[60px] items-center">
                      {selectedPictograms.length === 0 ? (
                        <p className="text-sm text-muted-foreground italic w-full text-center">
                          Selecciona pictogramas para formar una frase
                        </p>
                      ) : (
                        selectedPictograms.map((pictogram, index) => (
                          <div key={`${pictogram.id}-${index}`} className="flex items-center gap-2 bg-white p-2 rounded border">
                            <img
                              src={pictogram.image_urls.png_color}
                              alt={pictogram.labels?.es || 'Pictograma'}
                              className="w-8 h-8 object-contain"
                            />
                            <span className="text-sm">{pictogram.labels?.es || 'Sin etiqueta'}</span>
                            <Button
                              onClick={() => handleRemovePictogram(pictogram.id)}
                              size="sm"
                              variant="ghost"
                              className="h-6 w-6 p-0"
                            >
                              <X className="h-3 w-3" />
                            </Button>
                          </div>
                        ))
                      )}
                    </div>
                  </div>

                  {/* Botón enviar */}
                  <div className="flex justify-end">
                    <Button
                      onClick={handleSendMessage}
                      disabled={selectedPictograms.length === 0 || !selectedContactId}
                    >
                      <Send className="h-4 w-4 mr-2" />
                      Enviar {selectedPictograms.length} pictograma{selectedPictograms.length !== 1 ? 's' : ''}
                    </Button>
                  </div>
                </TabsContent>
              </Tabs>
            </div>
          </div>
        </div>
      </div>
    </SidebarProvider >
  );
};

export default Chat;
