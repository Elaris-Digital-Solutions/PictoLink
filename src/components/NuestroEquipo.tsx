import { motion } from "framer-motion";
import ImageCarousel from "@/components/ImageCarousel";
import { fadeInFrom, sectionReveal, staggerChildren, viewportSettings } from "@/lib/motion";

const teamSlides = [
  {
    image: "/team.webp",
    caption: "Equipo completo",
  },
  {
    image: "/fabrizio.webp",
    caption: "Fabrizio Bussalleu",
  },
  {
    image: "/jorge.webp",
    caption: "Jorge García",
  },
  {
    image: "/colfer.webp",
    caption: "Alejandro Colfer",
  },
  {
    image: "/delso.webp",
    caption: "Joaquín del Solar",
  },
];

const NuestroEquipo = () => {
  return (
    <motion.section
      id="equipo"
      className="py-20 bg-white"
      initial="hidden"
      whileInView="visible"
      viewport={viewportSettings}
      variants={sectionReveal({ delayChildren: 0.05, staggerChildren: 0.08 })}
    >
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          className="grid md:grid-cols-2 gap-12 items-center max-w-5xl mx-auto"
          variants={staggerChildren({ stagger: 0.08, delayChildren: 0.05 })}
        >
          <motion.div
            className="space-y-6"
            variants={staggerChildren({ stagger: 0.08, delayChildren: 0.04 })}
          >
            <motion.h2
              className="text-4xl sm:text-5xl font-bold text-foreground"
              variants={fadeInFrom("up", { distance: 18 })}
            >
              Nuestro <span className="text-primary">Equipo</span>
            </motion.h2>
            <motion.p
              className="text-lg text-muted-foreground leading-relaxed text-justify"
              variants={fadeInFrom("up", { distance: 16 })}
            >
              Somos un equipo multidisciplinario que combina desarrollo de software, inteligencia artificial, diseño de experiencia de usuario y gestión de proyectos con impacto social.
            </motion.p>
            <motion.p
              className="text-lg text-muted-foreground leading-relaxed text-justify"
              variants={fadeInFrom("up", { distance: 16 })}
            >
              Estamos comprometidos con la accesibilidad, la comunicación y el uso responsable de la tecnología para mejorar la vida de las personas con dificultades de comunicación.
            </motion.p>
          </motion.div>

          <motion.div
            className="flex justify-center"
            variants={fadeInFrom("right", { duration: 0.5, distance: 20 })}
          >
            <ImageCarousel
              slides={teamSlides}
              className="w-full max-w-sm h-[22rem] md:h-[24rem] rounded-3xl overflow-hidden shadow-[var(--shadow-soft)]"
            />
          </motion.div>
        </motion.div>
      </div>
    </motion.section>
  );
};

export default NuestroEquipo;
