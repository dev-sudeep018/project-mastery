import { spawn } from "node:child_process";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { createRequire } from "node:module";
import { createStaticServer } from "./http.mjs";
const root = fileURLToPath(new URL("../", import.meta.url));
const require = createRequire(path.join(root, "apps/web/package.json"));
const runner = createStaticServer({
  directory: path.join(root, "apps/runner/public"),
  host: "127.0.0.1",
  port: 4174,
  runner: true,
});
const web = spawn(
  process.execPath,
  [
    require.resolve("next/dist/bin/next"),
    "dev",
    "--webpack",
    "--hostname",
    "localhost",
  ],
  { cwd: path.join(root, "apps/web"), stdio: "inherit" },
);
function stop() {
  runner.close();
  web.kill();
}
process.on("SIGINT", stop);
process.on("SIGTERM", stop);
web.on("exit", (code) => {
  runner.close();
  process.exitCode = code ?? 0;
});
