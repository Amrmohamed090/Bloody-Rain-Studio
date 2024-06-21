new TypeIt("#element", {
    strings: ["Welcome To", "<span>Bloody Rain</span>"],
    speed: 80,
    waitUntilVisible: true,
    cursor: {
      animation: {
          options: {
              iterations: Infinity,
              easing: "linear",
              fill: "forwards",
          },
          loop: false,
      },
  }
  }).go();