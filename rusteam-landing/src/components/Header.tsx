"use client";

import { useState, useEffect } from "react";

const navLinks = [
  { href: "#pains", label: "Проблемы" },
  { href: "#process", label: "Как работаем" },
  { href: "#cases", label: "Кейсы" },
  { href: "#trust", label: "Доверие" },
  { href: "#fears", label: "FAQ" },
  { href: "#lead", label: "Расчёт" },
];

export default function Header() {
  const [isOpen, setIsOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 50);
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  const close = () => {
    setIsOpen(false);
    document.body.style.overflow = "";
  };

  const toggle = () => {
    setIsOpen((v) => {
      document.body.style.overflow = v ? "" : "hidden";
      return !v;
    });
  };

  return (
    <header
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 border-b border-white/[0.06] ${
        scrolled
          ? "bg-dark-900/95 backdrop-blur-xl"
          : "bg-dark-900/80 backdrop-blur-lg"
      }`}
    >
      <div className="max-w-6xl mx-auto px-5 flex items-center justify-between h-16">
        <a href="#" className="flex items-center gap-2.5 shrink-0">
          <span className="w-9 h-9 bg-gold text-black font-black text-sm rounded-lg flex items-center justify-center">
            RS
          </span>
          <span className="font-bold text-lg tracking-wide">RUSTEAM</span>
        </a>

        <nav className="hidden lg:flex items-center gap-6">
          {navLinks.map((l) => (
            <a
              key={l.href}
              href={l.href}
              className="text-sm text-white/60 font-medium hover:text-gold transition-colors"
            >
              {l.label}
            </a>
          ))}
        </nav>

        <a
          href="tel:+79612475867"
          className="hidden lg:block text-sm font-semibold hover:text-gold transition-colors"
        >
          +7 961 247-58-67
        </a>

        <button
          onClick={toggle}
          className="lg:hidden flex flex-col gap-[5px] p-2"
          aria-label="Меню"
        >
          <span
            className={`block w-5 h-0.5 bg-white rounded transition-transform ${
              isOpen ? "rotate-45 translate-y-[7px]" : ""
            }`}
          />
          <span
            className={`block w-5 h-0.5 bg-white rounded transition-opacity ${
              isOpen ? "opacity-0" : ""
            }`}
          />
          <span
            className={`block w-5 h-0.5 bg-white rounded transition-transform ${
              isOpen ? "-rotate-45 -translate-y-[7px]" : ""
            }`}
          />
        </button>
      </div>

      {/* Mobile overlay */}
      <div
        className={`fixed inset-0 top-16 bg-dark-900/98 backdrop-blur-xl z-40 flex flex-col items-center pt-12 gap-6 transition-all duration-300 lg:hidden ${
          isOpen ? "opacity-100 visible" : "opacity-0 invisible"
        }`}
      >
        {navLinks.map((l) => (
          <a
            key={l.href}
            href={l.href}
            onClick={close}
            className="text-xl font-semibold text-white/70 hover:text-gold transition-colors"
          >
            {l.label}
          </a>
        ))}
        <a
          href="tel:+79612475867"
          className="text-lg font-semibold text-gold"
        >
          +7 961 247-58-67
        </a>
        <a
          href="https://t.me/vivat116"
          target="_blank"
          rel="noopener"
          className="mt-4 px-8 py-3 bg-tg text-white rounded-xl font-semibold hover:bg-tg/80 transition-colors"
        >
          Написать в Telegram
        </a>
      </div>
    </header>
  );
}
