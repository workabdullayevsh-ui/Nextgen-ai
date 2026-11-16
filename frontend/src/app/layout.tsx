import type { Metadata, Viewport } from "next";
import { AuthProvider } from "@/lib/auth";
import { I18nProvider } from "@/lib/i18n";
import { ToastProvider } from "@/components/ui";
import "./globals.css";

export const metadata: Metadata = {
  title: "NEXTGEN AI — Energy Intelligence",
  description:
    "Ko‘p tashkilotli energiya intellekti platformasi: iste’mol tahlili, anomaliyalar, prognoz va asoslangan AI tahlil. Dasturchi: Shohjahon Abdullayev",
  applicationName: "NEXTGEN AI",
  manifest: "/manifest.json",
  icons: {
    icon: "/icon-192.png",
    apple: "/apple-touch-icon.png",
  },
  appleWebApp: {
    capable: true,
    statusBarStyle: "black-translucent",
    title: "NEXTGEN AI",
  },
};

export const viewport: Viewport = {
  themeColor: "#080D19",
  width: "device-width",
  initialScale: 1,
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="uz">
      <body className="min-h-screen bg-bg text-ink antialiased">
        <I18nProvider>
          <ToastProvider>
            <AuthProvider>{children}</AuthProvider>
          </ToastProvider>
        </I18nProvider>
      </body>
    </html>
  );
}
