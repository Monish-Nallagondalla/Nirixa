import type { Metadata } from "next";
import { Geist, JetBrains_Mono, Newsreader } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const jetbrainsMono = JetBrains_Mono({
  variable: "--font-mono-precision",
  subsets: ["latin"],
});

const newsreader = Newsreader({
  variable: "--font-serif-editorial",
  subsets: ["latin"],
  style: ["normal", "italic"],
});

export const metadata: Metadata = {
  title: "Nirixa Episteme OS • Cognitive Workbench & Research Studio",
  description: "Epistemic operating system for research synthesis, original thought assets, and human-AI coevolution.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      suppressHydrationWarning
      className={`${geistSans.variable} ${jetbrainsMono.variable} ${newsreader.variable} h-full antialiased`}
    >
      <body
        suppressHydrationWarning
        className="min-h-full flex flex-col bg-[#0D0F14] text-[#ECE8DD] font-sans selection:bg-[#D49B48]/20 selection:text-[#F3EFE0]"
      >
        {children}
      </body>
    </html>
  );
}
