import { defineConfig } from "vite";
import { viteStaticCopy } from "vite-plugin-static-copy";

export default defineConfig({
  base: "/spiceiodemoapp/",
  plugins: [
    viteStaticCopy({
      targets: [
        {
          src: "vello_svg/*",
          dest: "vello_svg",
        },
      ],
    }),
  ],
});
