import AnimateOnScroll from "./AnimateOnScroll";

export default function FinalCTA() {
  return (
    <section className="py-24 bg-dark-900">
      <div className="max-w-6xl mx-auto px-5">
        <AnimateOnScroll>
          <div className="max-w-2xl mx-auto text-center bg-dark-700 border border-white/[0.06] rounded-3xl p-10 md:p-14 relative overflow-hidden">
            {/* Gradient border effect */}
            <div className="absolute inset-0 rounded-3xl p-px bg-gradient-to-br from-gold/25 via-transparent to-tg/25 pointer-events-none" style={{ mask: "linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0)", maskComposite: "exclude", WebkitMaskComposite: "xor" }} />

            <h2 className="text-2xl md:text-3xl lg:text-4xl font-extrabold mb-4 tracking-tight">
              Получите подбор авто под ваш бюджет{" "}
              <span className="text-gold">уже сегодня</span>
            </h2>
            <p className="text-white/50 mb-8 max-w-md mx-auto leading-relaxed">
              Расчёт с учётом всех расходов — за 15 минут. Бесплатно и без обязательств.
            </p>

            <div className="flex flex-wrap justify-center gap-3 mb-6">
              <a
                href="#lead"
                className="px-8 py-4 bg-gold text-black font-bold text-base rounded-2xl hover:bg-gold-hover hover:shadow-[0_0_40px_rgba(230,175,46,0.15)] transition-all hover:-translate-y-0.5"
              >
                Получить расчёт
              </a>
              <a
                href="https://t.me/vivat116"
                target="_blank"
                rel="noopener"
                className="px-8 py-4 bg-tg text-white font-bold text-base rounded-2xl hover:bg-tg/80 transition-all hover:-translate-y-0.5 flex items-center gap-2"
              >
                <svg viewBox="0 0 24 24" fill="currentColor" className="w-5 h-5">
                  <path d="M11.944 0A12 12 0 0 0 0 12a12 12 0 0 0 12 12 12 12 0 0 0 12-12A12 12 0 0 0 12 0a12 12 0 0 0-.056 0zm4.962 7.224c.1-.002.321.023.465.14a.506.506 0 0 1 .171.325c.016.093.036.306.02.472-.18 1.898-.962 6.502-1.36 8.627-.168.9-.499 1.201-.82 1.23-.696.065-1.225-.46-1.9-.902-1.056-.693-1.653-1.124-2.678-1.8-1.185-.78-.417-1.21.258-1.91.177-.184 3.247-2.977 3.307-3.23.007-.032.014-.15-.056-.212s-.174-.041-.249-.024c-.106.024-1.793 1.14-5.061 3.345-.48.33-.913.49-1.302.48-.428-.008-1.252-.241-1.865-.44-.752-.245-1.349-.374-1.297-.789.027-.216.325-.437.893-.663 3.498-1.524 5.83-2.529 6.998-3.014 3.332-1.386 4.025-1.627 4.476-1.635z" />
                </svg>
                Telegram
              </a>
            </div>

            <a
              href="https://t.me/rusteam_auto"
              target="_blank"
              rel="noopener"
              className="inline-flex items-center gap-2 text-tg text-sm font-medium hover:opacity-80 transition-opacity"
            >
              <svg viewBox="0 0 24 24" fill="currentColor" className="w-4 h-4">
                <path d="M11.944 0A12 12 0 0 0 0 12a12 12 0 0 0 12 12 12 12 0 0 0 12-12A12 12 0 0 0 12 0a12 12 0 0 0-.056 0zm4.962 7.224c.1-.002.321.023.465.14a.506.506 0 0 1 .171.325c.016.093.036.306.02.472-.18 1.898-.962 6.502-1.36 8.627-.168.9-.499 1.201-.82 1.23-.696.065-1.225-.46-1.9-.902-1.056-.693-1.653-1.124-2.678-1.8-1.185-.78-.417-1.21.258-1.91.177-.184 3.247-2.977 3.307-3.23.007-.032.014-.15-.056-.212s-.174-.041-.249-.024c-.106.024-1.793 1.14-5.061 3.345-.48.33-.913.49-1.302.48-.428-.008-1.252-.241-1.865-.44-.752-.245-1.349-.374-1.297-.789.027-.216.325-.437.893-.663 3.498-1.524 5.83-2.529 6.998-3.014 3.332-1.386 4.025-1.627 4.476-1.635z" />
              </svg>
              Подписаться на наш Telegram-канал
            </a>
          </div>
        </AnimateOnScroll>
      </div>
    </section>
  );
}
