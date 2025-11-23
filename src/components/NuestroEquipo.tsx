import { useState, useEffect } from "react";

const NuestroEquipo = () => {
	const teamImages = [
		{ src: "/team.webp", caption: "Elaris Digital Solutions" },
		{ src: "/fabrizio.webp", caption: "Fabrizio Bussalleu" },
		{ src: "/colfer.webp", caption: "Alejandro Colfer" },
		{ src: "/jorge.webp", caption: "Jorge García" },
		{ src: "/delso.webp", caption: "Joaquín del Solar" },
	];

	const [currentImageIndex, setCurrentImageIndex] = useState(0);

	useEffect(() => {
		const interval = setInterval(() => {
			setCurrentImageIndex((prevIndex) => (prevIndex + 1) % teamImages.length);
		}, 4000); // Change image every 1 second

		return () => clearInterval(interval);
	}, [teamImages.length]);

	return (
		<section id="equipo" className="py-20 px-4 bg-white">
			<div className="container mx-auto max-w-6xl">
				<div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
					{/* Left Column: Text */}
					<div className="space-y-6">
						<h2 className="text-4xl md:text-5xl font-bold text-foreground">
							Nuestro <span className="text-primary">Equipo</span>
						</h2>

						<div className="space-y-4 text-lg text-foreground/80 leading-relaxed">
							<p>
								Proyecto liderado por un equipo multidisciplinario de estudiantes apasionados por la tecnología y la inclusión social.
								<span className="font-semibold text-foreground"> Fabrizio Bussalleu, Alejandro Colfer, Jorge García y Joaquín del Solar</span> han unido sus conocimientos para dar vida a PictoLink.
							</p>

							<p>
								Con la colaboración de expertos en educación especial y terapia del lenguaje, buscamos romper las barreras de comunicación que enfrentan millones de personas.
							</p>

							<p>
								El proyecto cuenta también con la participación de jóvenes voluntarios comprometidos con la creación de un mundo más accesible y empático para todos.
							</p>
						</div>
					</div>

					{/* Right Column: Image Carousel */}
					<div className="relative w-full aspect-video md:h-[500px] md:aspect-auto rounded-3xl overflow-hidden shadow-xl">
						{teamImages.map((image, index) => (
							<div
								key={index}
								className={`absolute inset-0 transition-opacity duration-1000 ease-in-out ${index === currentImageIndex ? "opacity-100" : "opacity-0"
									}`}
							>
								<img
									src={image.src}
									alt={image.caption}
									className="w-full h-full object-cover md:object-contain"
								/>
								{/* Caption Overlay */}
								<div className="absolute bottom-4 left-4 right-4 bg-black/60 backdrop-blur-sm text-white p-4 rounded-xl">
									<p className="font-medium text-center">{image.caption}</p>
								</div>
							</div>
						))}
					</div>
				</div>
			</div>
		</section>
	);
};

export default NuestroEquipo;
