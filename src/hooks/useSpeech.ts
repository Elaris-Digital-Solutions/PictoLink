import { useState, useEffect, useCallback } from 'react';

// ---------------------------------------------------------------------------
// Hook: useSpeechRecognition (Speech-to-Text)
// ---------------------------------------------------------------------------
// This hook requests microphone permission when the user starts listening.
// It creates a new SpeechRecognition instance each time to avoid stale
// references and ensures the transcript is updated in real time.
// Errors are exposed via the `error` field so the UI can show a helpful
// message to the user.
// ---------------------------------------------------------------------------
export function useSpeechRecognition() {
    const [isListening, setIsListening] = useState(false);
    const [transcript, setTranscript] = useState('');
    const [isSupported, setIsSupported] = useState(false);
    const [error, setError] = useState<string | null>(null);
    // We keep a reference to the current SpeechRecognition instance.
    const [recognition, setRecognition] = useState<any>(null);

    // Detect if the browser supports the Web Speech API.
    useEffect(() => {
        const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
        if (SpeechRecognition) {
            setIsSupported(true);
        } else {
            setIsSupported(false);
            setError('Este navegador no soporta reconocimiento de voz.');
        }
    }, []);

    // Start listening – request microphone permission first.
    const startListening = useCallback(async () => {
        if (!isSupported || isListening) return;
        try {
            // Ask the browser for microphone permission.
            await navigator.mediaDevices.getUserMedia({ audio: true });
        } catch (e) {
            console.error('Error requesting mic permission', e);
            setError('Permiso de micrófono denegado. Por favor, habilítalo en la configuración del navegador.');
            return;
        }

        const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
        if (!SpeechRecognition) {
            setError('Reconocimiento de voz no disponible.');
            return;
        }

        const instance = new SpeechRecognition();
        instance.continuous = true;
        instance.interimResults = true;
        instance.lang = 'es-ES'; // Español

        instance.onresult = (event: any) => {
            let finalTranscript = '';
            let interimTranscript = '';
            for (let i = event.resultIndex; i < event.results.length; i++) {
                const result = event.results[i][0].transcript;
                if (event.results[i].isFinal) {
                    finalTranscript += result + ' ';
                } else {
                    interimTranscript += result;
                }
            }
            setTranscript(finalTranscript || interimTranscript);
            setError(null);
        };

        instance.onerror = (event: any) => {
            console.error('Speech recognition error:', event.error);
            if (event.error === 'not-allowed') {
                setError('Permiso de micrófono denegado.');
            } else if (event.error === 'no-speech') {
                setError('No se detectó voz. Intenta hablar más cerca del micrófono.');
            } else {
                setError(`Error: ${event.error}`);
            }
            setIsListening(false);
        };

        instance.onend = () => {
            setIsListening(false);
        };

        setRecognition(instance);
        setTranscript('');
        setError(null);
        instance.start();
        setIsListening(true);
    }, [isSupported, isListening]);

    // Stop listening.
    const stopListening = useCallback(() => {
        if (recognition && isListening) {
            try {
                recognition.stop();
            } catch (e) {
                console.error('Error stopping recognition', e);
            }
            setIsListening(false);
        }
    }, [recognition, isListening]);

    // Reset transcript and error.
    const resetTranscript = useCallback(() => {
        setTranscript('');
        setError(null);
    }, []);

    return {
        isListening,
        transcript,
        isSupported,
        error,
        startListening,
        stopListening,
        resetTranscript,
    };
}

// ---------------------------------------------------------------------------
// Hook: useSpeechSynthesis (Text-to-Speech)
// ---------------------------------------------------------------------------
export function useSpeechSynthesis() {
    const [isSpeaking, setIsSpeaking] = useState(false);
    const [isSupported, setIsSupported] = useState(false);
    const [voices, setVoices] = useState<SpeechSynthesisVoice[]>([]);

    // Load available voices once.
    useEffect(() => {
        setIsSupported('speechSynthesis' in window);
        if ('speechSynthesis' in window) {
            const loadVoices = () => {
                const available = window.speechSynthesis.getVoices();
                setVoices(available);
            };
            loadVoices();
            if (window.speechSynthesis.onvoiceschanged !== undefined) {
                window.speechSynthesis.onvoiceschanged = loadVoices;
            }
        }
    }, []);

    const speak = useCallback((text: string) => {
        if (!isSupported || !text) return;

        // Cancel any ongoing speech immediately to ensure responsiveness
        window.speechSynthesis.cancel();

        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = 'es-ES';
        utterance.rate = 1.0; // Increased slightly for faster feedback
        utterance.onend = () => setIsSpeaking(false);
        utterance.onerror = (e) => {
            console.error('Speech synthesis error:', e);
            setIsSpeaking(false);
        };

        // Force immediate speak
        window.speechSynthesis.speak(utterance);

        // Chrome bug workaround: sometimes speech synthesis gets stuck. 
        // Resuming it can help kickstart it if it's paused.
        if (window.speechSynthesis.paused) {
            window.speechSynthesis.resume();
        }
    }, [isSupported, voices]);

    const stop = useCallback(() => {
        if (isSupported) {
            window.speechSynthesis.cancel();
            setIsSpeaking(false);
        }
    }, [isSupported]);

    return {
        speak,
        stop,
        isSpeaking,
        isSupported,
    };
}
