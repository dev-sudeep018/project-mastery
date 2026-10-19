import type { NextConfig } from "next";
const config: NextConfig = {
  output: "export",
  trailingSlash: true,
  transpilePackages: ["@mastery/problem-schema", "@mastery/runner-protocol"],
  images: { unoptimized: true },
  devIndicators: false,
};
export default config;
