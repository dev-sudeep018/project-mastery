import path from "node:path";
import { fileURLToPath } from "node:url";
import { createStaticServer } from "./http.mjs";
const root = fileURLToPath(new URL("../", import.meta.url));
const servers = [
  createStaticServer({
    directory: path.join(root, "apps/web/out"),
    host: "localhost",
    port: 3000,
  }),
  createStaticServer({
    directory: path.join(root, "apps/runner/public"),
    host: "127.0.0.1",
    port: 4174,
    runner: true,
  }),
];
for (const signal of ["SIGINT", "SIGTERM"])
  process.on(signal, () => servers.forEach((s) => s.close()));
