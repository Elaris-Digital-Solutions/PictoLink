import { useState } from "react";
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogHeader,
    DialogTitle,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { UserPlus, Loader2 } from "lucide-react";
import { useToast } from "@/hooks/use-toast";
import { useContacts } from "@/hooks/useContacts";

interface AddContactDialogProps {
    open: boolean;
    onOpenChange: (open: boolean) => void;
}

export function AddContactDialog({ open, onOpenChange }: AddContactDialogProps) {
    const [email, setEmail] = useState("");
    const [loading, setLoading] = useState(false);
    const { addContact } = useContacts();
    const { toast } = useToast();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        if (!email.trim()) {
            toast({
                title: "Error",
                description: "Por favor ingresa un email",
                variant: "destructive",
            });
            return;
        }

        // Validación básica de email
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email)) {
            toast({
                title: "Error",
                description: "Por favor ingresa un email válido",
                variant: "destructive",
            });
            return;
        }

        try {
            setLoading(true);
            await addContact(email);

            toast({
                title: "¡Contacto añadido!",
                description: `${email} ha sido añadido a tus contactos`,
            });

            setEmail("");
            onOpenChange(false);
        } catch (error: any) {
            toast({
                title: "Error",
                description: error.message || "No se pudo añadir el contacto",
                variant: "destructive",
            });
        } finally {
            setLoading(false);
        }
    };

    return (
        <Dialog open={open} onOpenChange={onOpenChange}>
            <DialogContent className="sm:max-w-[425px]">
                <DialogHeader>
                    <DialogTitle className="flex items-center gap-2">
                        <UserPlus className="h-5 w-5 text-primary" />
                        Añadir Contacto
                    </DialogTitle>
                    <DialogDescription>
                        Ingresa el email del usuario que deseas añadir a tus contactos
                    </DialogDescription>
                </DialogHeader>

                <form onSubmit={handleSubmit}>
                    <div className="grid gap-4 py-4">
                        <div className="grid gap-2">
                            <Label htmlFor="email">Email del contacto</Label>
                            <Input
                                id="email"
                                type="email"
                                placeholder="ejemplo@email.com"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                disabled={loading}
                                autoComplete="off"
                            />
                        </div>
                    </div>

                    <DialogFooter>
                        <Button
                            type="button"
                            variant="outline"
                            onClick={() => onOpenChange(false)}
                            disabled={loading}
                        >
                            Cancelar
                        </Button>
                        <Button type="submit" disabled={loading}>
                            {loading ? (
                                <>
                                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                                    Añadiendo...
                                </>
                            ) : (
                                <>
                                    <UserPlus className="mr-2 h-4 w-4" />
                                    Añadir
                                </>
                            )}
                        </Button>
                    </DialogFooter>
                </form>
            </DialogContent>
        </Dialog>
    );
}
