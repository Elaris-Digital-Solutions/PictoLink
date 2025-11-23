import TeamSection from "./ui/TeamSection.tsx";

const NuestroEquipo = () => {
	return (
		<div className="py-20 px-4 bg-[#FBF0ED]">
			<div className="container mx-auto max-w-6xl">
				<h2 className="text-3xl md:text-4xl font-bold text-center mb-12 text-foreground">
					Nuestro <span className="text-primary">Equipo</span>
				</h2>
				<TeamSection
					images={[
						{ src: "/team.webp", caption: "Equipo completo" },
						{ src: "/fabrizio.webp", caption: "Fabrizio Bussalleu" },
						{ src: "/colfer.webp", caption: "Alejandro Colfer" },
						{ src: "/jorge.webp", caption: "Jorge García" },
						{ src: "/delso.webp", caption: "Joaquín del Solar" },
					]}
				/>
			</div>
		</div>
	);
};

export default NuestroEquipo;
