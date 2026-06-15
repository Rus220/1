import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({
  subsets: ["latin", "cyrillic"],
  variable: "--font-inter",
});

export const metadata: Metadata = {
  title: "Авто из Китая и Кореи под ключ — доставка в Россию | RUSTEAM",
  description:
    "Привезём авто из Китая и Кореи дешевле рынка РФ на 20–40%. Полная проверка, договор, контроль на каждом этапе. Доставка 25–45 дней.",
  keywords: [
    "авто из китая",
    "авто под заказ",
    "привезти авто",
    "авто из кореи",
    "импорт авто",
    "авто под ключ",
    "купить авто из китая",
    "авто дешевле",
  ],
  openGraph: {
    title: "Авто из Китая и Кореи под ключ — RUSTEAM",
    description:
      "Экономия до 40%. Проверка, доставка, растаможка — всё включено.",
    type: "website",
    locale: "ru_RU",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ru" className={inter.className}>
      <body>{children}</body>
    </html>
  );
}
