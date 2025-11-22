import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { MessageSquare, Volume2, Type, Users, Heart, Sparkles, Target, Lightbulb } from "lucide-react";
import { useEffect, useState } from "react";

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
        className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
          isScrolled ? "bg-background/95 backdrop-blur-sm shadow-sm" : "bg-transparent"
        }`}
      >
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <MessageSquare className="h-6 w-6 text-primary" />
              <span className="text-xl font-bold text-foreground">PictoAmigos</span>
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
      <section id="inicio" className="min-h-screen flex items-center justify-center px-4">
        <div className="container mx-auto max-w-5xl text-center">
          <h1 className="text-5xl md:text-7xl font-bold text-foreground mb-6 leading-tight">
            PictoAmigos
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
              Conocer PictoAmigos
            </Button>
            <Button size="lg" variant="outline" onClick={() => window.location.href = "/auth"}>
              Probar la plataforma
            </Button>
          </div>
        </div>
      </section>

      {/* Quiénes Somos */}
      <section id="quienes-somos" className="py-20 px-4 bg-muted/30">
        <div className="container mx-auto max-w-4xl">
          <h2 className="text-3xl md:text-4xl font-bold text-center mb-12 text-foreground">
            ¿Quiénes somos?
          </h2>
          <div className="space-y-6 text-lg text-foreground/90 leading-relaxed">
            <p>
              PictoAmigos nace de la necesidad de crear puentes de comunicación para personas que enfrentan 
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
        </div>
      </section>

      {/* Conoce el Proyecto */}
      <section id="proyecto" className="py-20 px-4">
        <div className="container mx-auto max-w-6xl">
          <h2 className="text-3xl md:text-4xl font-bold text-center mb-4 text-foreground">
            Conoce el proyecto
          </h2>
          <p className="text-center text-muted-foreground mb-12 max-w-2xl mx-auto">
            Una solución integral para la comunicación accesible
          </p>
          
          <div className="grid md:grid-cols-3 gap-8 mb-20">
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

          {/* Cómo Funciona */}
          <h3 className="text-2xl md:text-3xl font-bold text-center mb-12 text-foreground">
            Cómo funciona
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
      <section id="para-quienes" className="py-20 px-4 bg-muted/30">
        <div className="container mx-auto max-w-6xl">
          <h2 className="text-3xl md:text-4xl font-bold text-center mb-4 text-foreground">
            Para quiénes
          </h2>
          <p className="text-center text-muted-foreground mb-12 max-w-3xl mx-auto">
            PictoAmigos está diseñado para transformar la manera en que las personas se comunican, 
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
                  PictoAmigos ofrece autonomía y voz propia. Permite expresar necesidades, emociones y 
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
                  Terapeutas del lenguaje, docentes y otros profesionales encuentran en PictoAmigos una 
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

      {/* Equipo */}
      <section id="equipo" className="py-20 px-4">
        <div className="container mx-auto max-w-6xl">
          <h2 className="text-3xl md:text-4xl font-bold text-center mb-4 text-foreground">
            Equipo
          </h2>
          <p className="text-center text-muted-foreground mb-12 max-w-3xl mx-auto">
            Un grupo multidisciplinario comprometido con la accesibilidad y la innovación tecnológica 
            al servicio de la comunicación.
          </p>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            <Card>
              <CardHeader>
                <CardTitle className="text-lg">Fabrizio Bussalleu</CardTitle>
                <CardDescription className="font-medium text-primary">
                  Desarrollo e Innovación
                </CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground">
                  Especialista en arquitectura de sistemas y desarrollo de soluciones tecnológicas accesibles.
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="text-lg">Jorge García</CardTitle>
                <CardDescription className="font-medium text-primary">
                  Inteligencia Artificial
                </CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground">
                  Experto en procesamiento de lenguaje natural y sistemas de traducción multimodal.
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="text-lg">Alejandro Colfer</CardTitle>
                <CardDescription className="font-medium text-primary">
                  Experiencia de Usuario
                </CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground">
                  Diseñador centrado en la accesibilidad y la creación de interfaces intuitivas para todos.
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="text-lg">Joaquín del Solar</CardTitle>
                <CardDescription className="font-medium text-primary">
                  Gestión y Estrategia
                </CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground">
                  Líder de proyecto enfocado en el impacto social y la sostenibilidad de la iniciativa.
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* CTA Final */}
      <section className="py-20 px-4 bg-secondary text-secondary-foreground">
        <div className="container mx-auto max-w-4xl text-center">
          <h2 className="text-3xl md:text-4xl font-bold mb-6">
            La comunicación es un derecho de todos
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
            Explorar PictoAmigos
          </Button>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 px-4 bg-background border-t border-border">
        <div className="container mx-auto max-w-6xl">
          <div className="grid md:grid-cols-3 gap-8 mb-8">
            <div>
              <div className="flex items-center gap-2 mb-3">
                <MessageSquare className="h-6 w-6 text-primary" />
                <span className="text-lg font-bold text-foreground">PictoAmigos</span>
              </div>
              <p className="text-sm text-muted-foreground">
                Comunicación accesible mediante pictogramas
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
              <p className="text-sm text-muted-foreground">
                ¿Tienes preguntas? Contáctanos para conocer más sobre PictoAmigos.
              </p>
            </div>
          </div>

          <div className="pt-8 border-t border-border text-center text-sm text-muted-foreground">
            <p>© {new Date().getFullYear()} PictoAmigos. Todos los derechos reservados.</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Index;
