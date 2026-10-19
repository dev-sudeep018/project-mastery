import http from "node:http";
import { readFile, stat } from "node:fs/promises";
import path from "node:path";

export function createStaticServer({ directory, host, port, runner = false }) {
  const base = path.resolve(directory);
  const types = {
    ".html": "text/html; charset=utf-8",
    ".js": "text/javascript",
    ".mjs": "text/javascript",
    ".css": "text/css",
    ".json": "application/json",
    ".wasm": "application/wasm",
    ".woff2": "font/woff2",
    ".ttf": "font/ttf",
    ".svg": "image/svg+xml",
    ".png": "image/png",
    ".py": "text/plain",
  };
  const appOrigin = process.env.APP_ORIGIN ?? "http://localhost:3000";
  const server = http.createServer(async (request, response) => {
    response.setHeader("X-Content-Type-Options", "nosniff");
    response.setHeader("Referrer-Policy", "no-referrer");
    if (runner) {
      response.setHeader(
        "Content-Security-Policy",
        `default-src 'none'; script-src 'self' 'wasm-unsafe-eval'; worker-src 'self'; connect-src 'self'; img-src 'none'; style-src 'none'; font-src 'none'; base-uri 'none'; form-action 'none'; frame-ancestors ${appOrigin}; object-src 'none'`,
      );
      response.setHeader(
        "Permissions-Policy",
        "camera=(), microphone=(), geolocation=(), payment=(), usb=()",
      );
      response.setHeader("Cross-Origin-Resource-Policy", "same-origin");
    }
    if (request.method !== "GET" && request.method !== "HEAD") {
      response.writeHead(405).end();
      return;
    }
    try {
      const url = new URL(request.url, `http://${host}:${port}`);
      const pathname = decodeURIComponent(url.pathname);
      let target = path.resolve(base, "." + pathname);
      if (!target.startsWith(base + path.sep) && target !== base) {
        response.writeHead(403).end();
        return;
      }
      if (
        pathname.includes("\\") ||
        pathname.split("/").some((s) => s.startsWith("."))
      ) {
        response.writeHead(403).end();
        return;
      }
      if ((await stat(target)).isDirectory())
        target = path.join(target, "index.html");
      const body = await readFile(target);
      response.setHeader(
        "Content-Type",
        types[path.extname(target)] ?? "application/octet-stream",
      );
      response.setHeader(
        "Cache-Control",
        pathname.startsWith("/runtime/") ? "public, max-age=3600" : "no-store",
      );
      response.writeHead(200).end(request.method === "HEAD" ? undefined : body);
    } catch {
      response.writeHead(404).end("Not found");
    }
  });
  server.listen(port, host, () =>
    console.log(`${runner ? "Runner" : "Application"}: http://${host}:${port}`),
  );
  return server;
}
