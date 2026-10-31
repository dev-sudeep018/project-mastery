import type { NextConfig } from "next";
const config: NextConfig = {
  output: "export",
  trailingSlash: true,
  transpilePackages: ["@zeroshot/problem-schema", "@zeroshot/runner-protocol"],
  images: { unoptimized: true },
  devIndicators: false,
};
export default config;
