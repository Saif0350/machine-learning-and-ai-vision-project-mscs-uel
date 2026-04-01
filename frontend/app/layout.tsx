import type { Metadata } from "next";
import { Orbitron, Plus_Jakarta_Sans } from "next/font/google";
import "./globals.css";
import Header from "@/components/Navbar/Header";
import Footer from "@/components/Navbar/Footer";
import NextTopLoader from "nextjs-toploader";
import AOS from "@/components/Wrappers/AOS";

export const orbitron = Orbitron({
  subsets: ["latin"],
  weight: ["400", "700"],
});

export const plusJakarta = Plus_Jakarta_Sans({
  subsets: ["latin"],
  weight: ["400", "500", "600", "700"],
});

export const metadata: Metadata = {
  title: "Fruit Image Classification ",
  description: "Crafted by saif alam ansari",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${plusJakarta.className} antialiased`}>
        <NextTopLoader color="#E1F482" showSpinner={false} />
        <AOS />
        <Header />
        {children}
        <Footer />
      </body>
    </html>
  );
}
