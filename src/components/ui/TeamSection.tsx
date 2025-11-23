import React from 'react';

interface TeamSectionProps {
  images: { src: string; caption: string }[];
}

const TeamSection: React.FC<TeamSectionProps> = ({ images }) => {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
      {images.map((image, index) => (
        <div key={index} className="text-center">
          <img
            src={image.src}
            alt={image.caption}
            className="w-full h-64 object-cover rounded-lg shadow-md"
          />
          <p className="mt-4 text-lg font-medium text-foreground">{image.caption}</p>
        </div>
      ))}
    </div>
  );
};

export default TeamSection;