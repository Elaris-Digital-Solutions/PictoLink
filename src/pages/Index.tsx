import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { MessageSquare, Volume2, Type, Users, Heart, Sparkles, Target, Lightbulb, Mail, Phone, Instagram, MapPin } from "lucide-react";
import { useEffect, useState } from "react";
import NuestroEquipo from "@/components/NuestroEquipo";

const Index = () => {
  const [isScrolled, setIsScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 20);
    };
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  const scrollToSection = (id: string) => {
    const element = document.getElementById(id);
    if (element) {
      const offset = 80;
      const elementPosition = element.getBoundingClientRect().top;
      const offsetPosition = elementPosition + window.pageYOffset - offset;
      window.scrollTo({
        top: offsetPosition,
        behavior: "smooth",
      });
    }
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Navbar */}
      <nav
        className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${isScrolled ? "bg-background/95 backdrop-blur-sm shadow-sm" : "bg-transparent"
          }`}
      >
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <img src="/logo.png" alt="PictoLink" className="h-12 w-auto" />
            </div>

            <div className="hidden md:flex items-center gap-6">
              <button
                onClick={() => scrollToSection("inicio")}
                className="text-sm font-medium text-foreground hover:text-primary transition-colors"
              >
                Inicio
              </button>
              <button
                onClick={() => scrollToSection("quienes-somos")}
                className="text-sm font-medium text-foreground hover:text-primary transition-colors"
              >
                ¿Quiénes somos?
              </button>
              <button
                onClick={() => scrollToSection("proyecto")}
                className="text-sm font-medium text-foreground hover:text-primary transition-colors"
              >
                Proyecto
              </button>
              <button
                onClick={() => scrollToSection("para-quienes")}
                className="text-sm font-medium text-foreground hover:text-primary transition-colors"
              >
                Para quiénes
              </button>
              <button
                onClick={() => scrollToSection("equipo")}
                className="text-sm font-medium text-foreground hover:text-primary transition-colors"
              >
                Equipo
              </button>
              <Button size="sm" onClick={() => window.location.href = "/auth"}>
                Probar la plataforma
              </Button>
            </div>

            <Button size="sm" className="md:hidden" onClick={() => window.location.href = "/auth"}>
              Probar
            </Button>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section
        id="inicio"
        className="min-h-screen flex items-center justify-center px-4 bg-cover bg-center relative bg-white"
        style={{ backgroundImage: "url('/hero-placeholder.png')" }}
      >
        <div className="absolute inset-0 bg-gradient-to-b from-white/50 to-white/90"></div>
        <div className="container mx-auto max-w-5xl text-center relative z-10">
          <h1 className="text-5xl md:text-7xl font-bold text-foreground mb-6 leading-tight">
            Picto<span className="text-primary">Link</span>
          </h1>
          <p className="text-xl md:text-2xl text-secondary font-medium mb-4">
            Comunicación accesible mediante pictogramas para todas las personas
          </p>
          <p className="text-lg text-muted-foreground mb-10 max-w-3xl mx-auto">
            Una plataforma diseñada para personas con dificultades de comunicación, lenguaje o aprendizaje,
            junto con sus familias, cuidadores y profesionales.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button size="lg" onClick={() => scrollToSection("quienes-somos")}>
              Conocer PictoLink
            </Button>
            <Button size="lg" variant="outline" onClick={() => window.location.href = "/auth"}>
              Probar la plataforma
            </Button>
          </div>
        </div>
      </section>

      {/* Quiénes Somos */}
      <section id="quienes-somos" className="py-20 px-4 bg-white">
        <div className="container mx-auto max-w-6xl">
          <h2 className="text-3xl md:text-4xl font-bold text-center mb-12 text-foreground">
            ¿Quiénes <span className="text-primary">somos?</span>
          </h2>
          <div className="grid md:grid-cols-2 gap-12 items-center">
            <div className="space-y-6 text-lg text-foreground/90 leading-relaxed">
              <p>
                PictoLink nace de la necesidad de crear puentes de comunicación para personas que enfrentan
                barreras en el lenguaje verbal. Ya sea por condiciones del desarrollo, accidentes, ictus o
                cualquier otra circunstancia, millones de personas encuentran dificultades para expresarse y
                ser comprendidas.
              </p>
              <p>
                Somos un equipo comprometido con el desarrollo de tecnología accesible que empodere a las personas
                a comunicarse de manera efectiva. Creemos que la comunicación es un derecho fundamental, y que la
                tecnología puede ser una herramienta poderosa para garantizar ese derecho.
              </p>
              <p>
                Nuestra plataforma utiliza pictogramas como lenguaje visual universal, facilitando la expresión
                de ideas, necesidades y emociones de manera clara y comprensible para todos los involucrados en
                el proceso comunicativo.
              </p>
            </div>
            <div className="relative h-full min-h-[400px] rounded-2xl overflow-hidden shadow-lg">
              <img
                src="/team.webp"
                alt="Equipo PictoLink"
                className="w-full h-full object-cover"
              />
            </div>
          </div>
        </div>
      </section>

      {/* Conoce el Proyecto */}
      <section id="proyecto" className="py-20 px-4 bg-[#FBF0ED]">
        <div className="container mx-auto max-w-6xl">
          <h2 className="text-3xl md:text-4xl font-bold text-center mb-4 text-foreground">
            Conoce el <span className="text-primary">proyecto</span>
          </h2>
          <p className="text-center text-muted-foreground mb-12 max-w-2xl mx-auto">
            Una solución integral para la comunicación accesible
          </p>
          <div className="grid md:grid-cols-3 gap-8">
            <Card>
              <CardHeader>
                <Target className="h-10 w-10 text-primary mb-3" />
                <CardTitle>Objetivo principal</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground">
                  Facilitar la comunicación efectiva mediante un sistema visual de pictogramas que permita
                  expresar ideas, necesidades y emociones sin barreras lingüísticas.
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <Users className="h-10 w-10 text-primary mb-3" />
                <CardTitle>Para quién</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground">
                  Personas con dificultades de comunicación por desarrollo, accidentes o condiciones neurológicas,
                  así como sus familias, cuidadores, terapeutas del lenguaje y docentes.
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <Sparkles className="h-10 w-10 text-primary mb-3" />
                <CardTitle>Qué nos diferencia</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground">
                  Una plataforma integral que combina tecnología de traducción automática con un diseño
                  centrado en la accesibilidad, creando una experiencia fluida y natural.
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* Cómo Funciona */}
      <section id="como-funciona" className="py-20 px-4 bg-white">
        <div className="container mx-auto max-w-6xl">
          <h3 className="text-2xl md:text-3xl font-bold text-center mb-12 text-foreground">
            Cómo <span className="text-primary">funciona</span>
          </h3>
          <div className="grid md:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <MessageSquare className="h-8 w-8 text-primary mb-2" />
                <CardTitle>Comunicación por pictogramas</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground">
                  Sistema visual intuitivo que permite construir frases y expresar ideas complejas mediante
                  pictogramas organizados de forma clara y accesible.
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <Type className="h-8 w-8 text-primary mb-2" />
                <CardTitle>Traducción texto ↔ pictogramas</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground">
                  Convierte texto escrito en secuencias de pictogramas y viceversa, facilitando la comunicación
                  entre usuarios y personas que utilizan lenguaje verbal.
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <Volume2 className="h-8 w-8 text-primary mb-2" />
                <CardTitle>Audio ↔ pictogramas</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground">
                  Tecnología de voz que transforma mensajes hablados en pictogramas y genera audio a partir de
                  secuencias visuales, creando una experiencia multimodal.
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <Lightbulb className="h-8 w-8 text-primary mb-2" />
                <CardTitle>Uso en múltiples contextos</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground">
                  Adaptable a entornos familiares, terapéuticos y educativos, con funcionalidades específicas
                  para cada necesidad y tipo de usuario.
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* Para Quiénes */}
      <section id="para-quienes" className="py-20 px-4 bg-[#FBF0ED]">
        <div className="container mx-auto max-w-6xl">
          <h2 className="text-3xl md:text-4xl font-bold text-center mb-4 text-foreground">
            Para <span className="text-primary">quiénes</span>
          </h2>
          <p className="text-center text-muted-foreground mb-12 max-w-3xl mx-auto">
            PictoLink está diseñado para transformar la manera en que las personas se comunican,
            conectan y comprenden.
          </p>

          <div className="grid md:grid-cols-3 gap-8">
            <Card>
              <CardHeader>
                <Heart className="h-10 w-10 text-primary mb-3" />
                <CardTitle>Para personas con dificultades de comunicación</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <p className="text-muted-foreground">
                  PictoLink ofrece autonomía y voz propia. Permite expresar necesidades, emociones y
                  pensamientos de manera independiente, reduciendo la frustración y mejorando la calidad de vida.
                </p>
                <p className="text-muted-foreground">
                  La interfaz adaptativa se ajusta a diferentes niveles de habilidad y necesidades específicas.
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <Users className="h-10 w-10 text-primary mb-3" />
                <CardTitle>Para familias y cuidadores</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <p className="text-muted-foreground">
                  Facilitamos la comprensión mutua en el día a día. Las familias pueden comunicarse de manera
                  más efectiva con sus seres queridos, anticipar necesidades y fortalecer vínculos.
                </p>
                <p className="text-muted-foreground">
                  El sistema incluye herramientas para personalizar vocabularios según el contexto familiar.
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <Sparkles className="h-10 w-10 text-primary mb-3" />
                <CardTitle>Para profesionales</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <p className="text-muted-foreground">
                  Terapeutas del lenguaje, docentes y otros profesionales encuentran en PictoLink una
                  herramienta flexible para el trabajo terapéutico y educativo.
                </p>
                <p className="text-muted-foreground">
                  Permite crear materiales personalizados, hacer seguimiento del progreso y adaptar estrategias
                  de intervención.
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>



      {/* Nuestro Equipo */}
      <NuestroEquipo />

      {/* CTA Final */}
      <section className="py-20 px-4 bg-secondary text-secondary-foreground">
        <div className="container mx-auto max-w-4xl text-center">
          <h2 className="text-3xl md:text-4xl font-bold mb-6">
            La comunicación es un derecho de <span className="text-primary">todos</span>
          </h2>
          <p className="text-lg mb-8 opacity-90 max-w-3xl mx-auto">
            Estamos construyendo un futuro donde cada persona tiene voz, donde las barreras de comunicación
            se transforman en puentes de conexión y comprensión.
          </p>
          <Button
            size="lg"
            variant="outline"
            className="bg-secondary-foreground text-secondary hover:bg-secondary-foreground/90"
            onClick={() => window.location.href = "/auth"}
          >
            Explorar PictoLink
          </Button>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 px-4 bg-background border-t border-border">
        <div className="container mx-auto max-w-6xl">
          <div className="grid md:grid-cols-3 gap-8 mb-8">
            <div>
              <div className="flex items-center gap-2 mb-3">
                <img src="/elaris-upc.png" alt="Elaris UPC" className="h-16 w-auto" />
              </div>
              <p className="text-sm text-muted-foreground">
                Comunicación accesible mediante pictogramas para que todas las personas puedan hacerse escuchar.
                Proyecto desarrollado por Elaris Digital Solutions en colaboración con la UPC.
              </p>
            </div>

            <div>
              <h3 className="font-semibold mb-3 text-foreground">Navegación</h3>
              <div className="space-y-2">
                <button
                  onClick={() => scrollToSection("inicio")}
                  className="block text-sm text-muted-foreground hover:text-primary transition-colors"
                >
                  Inicio
                </button>
                <button
                  onClick={() => scrollToSection("quienes-somos")}
                  className="block text-sm text-muted-foreground hover:text-primary transition-colors"
                >
                  ¿Quiénes somos?
                </button>
                <button
                  onClick={() => scrollToSection("proyecto")}
                  className="block text-sm text-muted-foreground hover:text-primary transition-colors"
                >
                  Proyecto
                </button>
                <button
                  onClick={() => scrollToSection("para-quienes")}
                  className="block text-sm text-muted-foreground hover:text-primary transition-colors"
                >
                  Para quiénes
                </button>
                <button
                  onClick={() => scrollToSection("equipo")}
                  className="block text-sm text-muted-foreground hover:text-primary transition-colors"
                >
                  Equipo
                </button>
              </div>
            </div>

            <div>
              <h3 className="font-semibold mb-3 text-foreground">Contacto</h3>
              <p className="text-sm text-muted-foreground mb-4">
                ¿Tienes preguntas? Contáctanos para conocer más sobre PictoLink.
              </p>
              <div className="space-y-3">
                <a href="mailto:contact@elarisdigitalsolutions.com" className="flex items-center gap-2 text-sm text-muted-foreground hover:text-primary transition-colors">
                  <Mail className="h-4 w-4" />
                  <span>contact@elarisdigitalsolutions.com</span>
                </a>
                <a href="tel:+51987450340" className="flex items-center gap-2 text-sm text-muted-foreground hover:text-primary transition-colors">
                  <Phone className="h-4 w-4" />
                  <span>+51 987 450 340</span>
                </a>
                <a href="https://www.instagram.com/elarisdigitalsolutions" target="_blank" rel="noopener noreferrer" className="flex items-center gap-2 text-sm text-muted-foreground hover:text-primary transition-colors">
                  <Instagram className="h-4 w-4" />
                  <span>@elarisdigitalsolutions</span>
                </a>
                <div className="flex items-center gap-2 text-sm text-muted-foreground">
                  <MapPin className="h-4 w-4" />
                  <span>Surco</span>
                </div>
              </div>
            </div>
          </div>

          <div className="pt-8 border-t border-border text-center text-sm text-muted-foreground">
            <p>© {new Date().getFullYear()} PictoLink. Todos los derechos reservados. <a href="https://www.instagram.com/elarisdigitalsolutions" target="_blank" rel="noopener noreferrer" className="hover:text-primary transition-colors underline decoration-1 underline-offset-2">Desarrollado por Elaris Digital Solutions</a></p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Index;
