/** @type {import('next').NextConfig} */
const BACKEND =
  process.env.BACKEND_INTERNAL_URL ??
  (process.env.VERCEL
    ? "https://pamela-messenger-null-dir.trycloudflare.com"
    : "http://127.0.0.1:8000");

const nextConfig = {
  reactStrictMode: true,
  poweredByHeader: false,
  typescript: {
    ignoreBuildErrors: true,
  },
  eslint: {
    ignoreDuringBuilds: true,
  },
  async rewrites() {
    return [
      { source: "/api/v1/:path*", destination: `${BACKEND}/api/v1/:path*` },
      { source: "/health/:path*", destination: `${BACKEND}/health/:path*` },
    ];
  },
};

export default nextConfig;
