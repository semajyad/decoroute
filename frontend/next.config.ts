import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  reactCompiler: true,
  output: 'export',
  trailingSlash: true,
  images: {
    domains: ['cascade-projects-pw62zlcjv-semajyads-projects.vercel.app'],
  },
};

export default nextConfig;
