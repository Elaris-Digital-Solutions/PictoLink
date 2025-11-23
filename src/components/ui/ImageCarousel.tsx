import React, { useEffect, useMemo, useState } from "react";

type Slide = {
  image: string;
  caption: string;
};

interface ImageCarouselProps {
  slides: Slide[];
  className?: string;
  showCaption?: boolean;
}

const ImageCarousel: React.FC<ImageCarouselProps> = ({ slides, className, showCaption = true }) => {
  const [currentIndex, setCurrentIndex] = useState<number>(0);
  const [isHovered, setIsHovered] = useState<boolean>(false);

  const normalizedSlides = useMemo(() => {
    if (!slides || slides.length === 0) {
      return [] as Slide[];
    }

    if (slides.length === 1) {
      return Array.from({ length: 3 }, () => slides[0]);
    }

    return slides;
  }, [slides]);

  useEffect(() => {
    if (normalizedSlides.length === 0) return;

    const id = setInterval(() => {
      setCurrentIndex((prev) => {
        if (isHovered) return prev;
        return (prev + 1) % normalizedSlides.length;
      });
    }, 2000);

    return () => clearInterval(id);
  }, [isHovered, normalizedSlides.length]);

  useEffect(() => {
    setCurrentIndex(0);
  }, [normalizedSlides.length]);

  if (normalizedSlides.length === 0) return null;

  return (
    <div
      className={`image-carousel${className ? ` ${className}` : ""}`}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      aria-roledescription="carousel"
    >
      {normalizedSlides.map((slide, idx) => {
        const isActive = idx === currentIndex;
        return (
          <div
            key={idx}
            className={`image-carousel__slide ${isActive ? "active" : ""}`}
            aria-hidden={!isActive}
          >
            <img
              src={slide.image}
              alt={slide.caption ?? `Slide ${idx + 1}`}
              className="image-carousel__img"
            />
            {showCaption && (
              <div className="image-carousel__caption">{slide.caption}</div>
            )}
          </div>
        );
      })}
    </div>
  );
};

export default ImageCarousel;
