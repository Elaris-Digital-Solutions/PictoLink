export const fadeInFrom = (direction: "up" | "down" | "left" | "right", options: { distance?: number; duration?: number } = {}) => {
  const { distance = 20, duration = 0.5 } = options;
  const x = direction === "left" ? -distance : direction === "right" ? distance : 0;
  const y = direction === "up" ? -distance : direction === "down" ? distance : 0;

  return {
    hidden: { opacity: 0, x, y },
    visible: { opacity: 1, x: 0, y: 0, transition: { duration } },
  };
};

export const sectionReveal = (options: { delayChildren?: number; staggerChildren?: number } = {}) => {
  const { delayChildren = 0, staggerChildren = 0.1 } = options;

  return {
    hidden: {},
    visible: {
      transition: {
        delayChildren,
        staggerChildren,
      },
    },
  };
};

export const staggerChildren = (options: { stagger?: number; delayChildren?: number } = {}) => {
  const { stagger = 0.1, delayChildren = 0 } = options;

  return {
    hidden: {},
    visible: {
      transition: {
        delayChildren,
        staggerChildren: stagger,
      },
    },
  };
};

export const viewportSettings = {
  once: true,
  amount: 0.2,
};