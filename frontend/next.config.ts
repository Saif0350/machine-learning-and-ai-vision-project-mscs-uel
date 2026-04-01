import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  env: {
    Frontend: process.env.FRONTEND,
    Backend: process.env.NEXT_PUBLIC_BACKEND,
  },
  images: {
    remotePatterns: [
      {
        protocol: "https",
        hostname: "*",
      },
      {
        protocol: "http",
        hostname: "*",
      },
    ],
  },
};

export default nextConfig;
