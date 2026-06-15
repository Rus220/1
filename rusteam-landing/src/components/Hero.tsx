import AnimateOnScroll from "./AnimateOnScroll";

export default function Hero() {
  return (
    <section className="relative min-h-screen flex items-center pt-24 pb-16 overflow-hidden">
      {/* Background gradients */}
      <div className="absolute inset-0 z-0">
        <div className="absolute top-0 right-0 w-[600px] h-[600px] bg-[radial-gradient(circle,rgba(230,175,46,0.06)_0%,transparent_70%)] animate-pulse" />
        <div className="absolute bottom-0 left-0 w-[400px] h-[400px] bg-[radial-gradient(circle,rgba(42,171,238,0.04)_0%,transparent_70%)]" />
        <div className="absolute inset-0 bg-gradient-to-b from-dark-900 to-dark-800" />
      </div>

      <div className="relative z-10 max-w-6xl mx-auto px-5 w-full">
        <AnimateOnScroll>
          <div className="inline-block text-xs font-bold tracking-[0.15em] uppercase text-gold bg-gold-soft px-4 py-1.5 rounded-full border border-gold/15 mb-6">
            ИМПОРТ АВТО RUSTEAM | КИТАЙ, КОРЕЯ
          </div>
        </AnimateOnScroll>

        <AnimateOnScroll delay={100}>
          <h1 className="text-4xl md:text-5xl lg:text-6xl font-black leading-[1.1] mb-5 tracking-tight max-w-3xl">
            Авто мечты — <span className="text-gold">дешевле на&nbsp;20–40%</span>{" "}
            с полной проверкой и&nbsp;доставкой
          </h1>
        </AnimateOnScroll>

        <AnimateOnScroll delay={200}>
          <p className="text-lg md:text-xl text-white/65 max-w-xl mb-8 leading-relaxed">
            Полная проверка, договор, контроль на каждом этапе. Без скрытых платежей.
            Доставка 25–45&nbsp;дней.
          </p>
        </AnimateOnScroll>

        <AnimateOnScroll delay={300}>
          <div className="flex flex-wrap gap-3 mb-12">
            <a
              href="#lead"
              className="px-8 py-4 bg-gold text-black font-bold text-base rounded-2xl hover:bg-gold-hover hover:shadow-[0_0_40px_rgba(230,175,46,0.15)] transition-all hover:-translate-y-0.5"
            >
              Рассчитать стоимость
            </a>
            <a
              href="#lead"
              className="px-8 py-4 border border-white/15 text-white font-semibold text-base rounded-2xl bg-white/5 hover:border-gold hover:text-gold hover:bg-gold-soft transition-all"
            >
              Получить подбор авто
            </a>
          </div>
        </AnimateOnScroll>

        <AnimateOnScroll delay={400}>
          <div className="flex flex-wrap gap-4">
            {[
              { val: "150+", txt: "авто доставлено" },
              { val: "25–45", txt: "дней доставка" },
              { val: "0 ₽", txt: "скрытых платежей" },
            ].map((item) => (
              <div
                key={item.txt}
                className="px-4 py-3 bg-dark-700 border border-white/[0.06] rounded-xl flex items-center gap-3"
              >
                <span className="text-2xl font-black text-gold">
                  {item.val}
                </span>
                <span className="text-sm text-white/60">{item.txt}</span>
              </div>
            ))}
          </div>
        </AnimateOnScroll>
      </div>
    </section>
  );
}
