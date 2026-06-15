export default function Footer() {
  return (
    <footer className="bg-dark-900 border-t border-white/[0.06] py-10">
      <div className="max-w-6xl mx-auto px-5 flex flex-col items-center gap-5 text-center">
        <div className="flex items-center gap-2.5">
          <span className="w-9 h-9 bg-gold text-black font-black text-sm rounded-lg flex items-center justify-center">
            RS
          </span>
          <span className="font-bold text-lg tracking-wide">RUSTEAM</span>
        </div>

        <div className="flex flex-wrap justify-center gap-5 text-sm text-white/50">
          <a href="tel:+79612475867" className="hover:text-gold transition-colors">
            +7 961 247-58-67
          </a>
          <a
            href="https://t.me/vivat116"
            target="_blank"
            rel="noopener"
            className="hover:text-gold transition-colors"
          >
            Telegram
          </a>
          <a
            href="https://t.me/rusteam_auto"
            target="_blank"
            rel="noopener"
            className="hover:text-gold transition-colors"
          >
            Telegram-канал
          </a>
        </div>

        <p className="text-white/25 text-xs">
          &copy; 2024–2026 RUSTEAM. Импорт авто из Китая и Кореи.
        </p>
      </div>
    </footer>
  );
}
