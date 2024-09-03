import { Application, Assets, Graphics } from "pixi.js";
import { Viewport } from "pixi-viewport";

(async () => {
  // Create a new application
  const app = new Application();

  // Initialize the application
  await app.init({ antialias: true, resizeTo: window });

  // Append the application canvas to the document body
  document.body.appendChild(app.canvas);

  const demoSvg = await Assets.load({
    src: "/spiceiodemo/demo3.svg",
    data: {
      parseAsGraphicsContext: true,
    },
  });
  // create viewport
  const viewport = new Viewport({
    screenWidth: window.innerWidth,
    screenHeight: window.innerHeight,
    worldWidth: 1000,
    worldHeight: 1000,

    events: app.renderer.events, // the interaction module is important for wheel to work properly when renderer.view is placed or scaled
  });

  app.stage.addChild(viewport);
  // activate plugins
  viewport.drag().pinch().wheel().decelerate();

  const graphics = new Graphics(demoSvg);

  // line it up as this svg is not centered
  // const bounds = graphics.getLocalBounds();

  // graphics.pivot.set((bounds.x + bounds.width) / 4, (bounds.y + bounds.height) / 4);
  graphics.scale.set(4);

  graphics.position.set(app.screen.width / 2 - 500, app.screen.height / 4 + 500);

  viewport.addChild(graphics);
})();
