import React from "react";

interface Slide {
  image: string;
  caption: string;
}

interface ImageCarouselProps {
  slides: Slide[];
  className?: string;
}

const ImageCarousel: React.FC<ImageCarouselProps> = ({ slides, className }) => {
  return (
    <div className={`image-carousel ${className}`}>
      {slides.map((slide, index) => (
        <div key={index} className="carousel-slide">
          <img src={slide.image} alt={slide.caption} className="carousel-image" />
          <div className="carousel-caption">{slide.caption}</div>
        </div>
      ))}
    </div>
  );
};

export default ImageCarousel;