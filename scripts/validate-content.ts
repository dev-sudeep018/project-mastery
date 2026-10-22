import { loadContent } from "./content";
const entries = await loadContent();
console.log(
  `Validated metadata, required files and prerequisites for ${entries.length} packages. Run pnpm content:check or pnpm test:python for executable checks.`,
);
