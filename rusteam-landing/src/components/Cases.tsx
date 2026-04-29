import AnimateOnScroll from "./AnimateOnScroll";

const cases = [
  {
    country: "Китай",
    model: "Li L7 Pro",
    year: 2024,
    priceAbroad: "3 250 000",
    priceRu: "4 500 000",
    saving: "1 250 000",
    days: 25,
  },
  {
    country: "Китай",
    model: "Zeekr 001",
    year: 2024,
    priceAbroad: "3 100 000",
    priceRu: "4 200 000",
    saving: "1 100 000",
    days: 28,
  },
  {
    country: "Корея",
    model: "Hyundai Tucson",
    year: 2023,
    priceAbroad: "2 400 000",
    priceRu: "3 300 000",
    saving: "900 000",
    days: 20,
  },
  {
    country: "Китай",
    model: "BYD Han EV",
    year: 2024,
    priceAbroad: "2 850 000",
    priceRu: "3 900 000",
    saving: "1 050 000",
    days: 22,
  },
  {
    country: "Корея",
    model: "Kia K5",
    year: 2023,
    priceAbroad: "2 100 000",
    priceRu: "2 900 000",
    saving: "800 000",
    days: 18,
  },
  {
    country: "Китай",
    model: "Tank 500",
    year: 2024,
    priceAbroad: "4 200 000",
    priceRu: "5 800 000",
    saving: "1 600 000",
    days: 30,
  },
  {
    country: "Китай",
    model: "Changan Uni-V",
    year: 2024,
    priceAbroad: "1 750 000",
    priceRu: "2 400 000",
    saving: "650 000",
    days: 24,
  },
  {
    country: "Корея",
    model: "Genesis G80",
    year: 2023,
    priceAbroad: "3 600 000",
    priceRu: "5 100 000",
    saving: "1 500 000",
    days: 22,
  },
];

export default function Cases() {
  return (
    <section id="cases" className="py-20 bg-dark-800">
      <div className="max-w-6xl mx-auto px-5">
        <AnimateOnScroll>
          <h2 className="text-3xl md:text-4xl font-extrabold text-center mb-3 tracking-tight">
            Реальные <span className="text-gold">кейсы</span>
          </h2>
        </AnimateOnScroll>
        <AnimateOnScroll>
          <p className="text-center text-white/55 mb-12 max-w-lg mx-auto">
            Авто, которые мы уже привезли. Цены и сроки — факт, не обещания.
          </p>
        </AnimateOnScroll>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-5">
          {cases.map((c, i) => (
            <AnimateOnScroll key={c.model} delay={(i % 4) * 100}>
              <div className="bg-dark-700 border border-white/[0.06] rounded-2xl overflow-hidden hover:border-gold/15 hover:-translate-y-1 transition-all">
                {/* Header */}
                <div className="p-5 pb-3 border-b border-white/[0.04] flex items-center gap-3">
                  <span className="text-[0.65rem] font-bold tracking-wider uppercase bg-gold text-black px-2.5 py-0.5 rounded-full">
                    {c.country}
                  </span>
                  <span className="font-bold flex-1">{c.model}</span>
                  <span className="text-xs text-white/40">{c.year}</span>
                </div>

                {/* Body */}
                <div className="px-5 py-3">
                  <div className="flex justify-between py-2.5 text-sm text-white/55 border-b border-white/[0.03]">
                    <span>Итого с доставкой</span>
                    <span className="text-white font-semibold">{c.priceAbroad} ₽</span>
                  </div>
                  <div className="flex justify-between py-2.5 text-sm text-white/55 border-b border-white/[0.03]">
                    <span>Цена в РФ</span>
                    <span className="text-white/40 line-through">{c.priceRu} ₽</span>
                  </div>
                  <div className="flex justify-between py-2.5 text-sm font-semibold">
                    <span>Экономия</span>
                    <span className="text-success font-extrabold">{c.saving} ₽</span>
                  </div>
                  <div className="flex justify-between py-2.5 text-sm text-white/55">
                    <span>Срок доставки</span>
                    <span>{c.days} дней</span>
                  </div>
                </div>
              </div>
            </AnimateOnScroll>
          ))}
        </div>

        {/* CTA */}
        <AnimateOnScroll>
          <div className="text-center mt-12">
            <a
              href="#lead"
              className="inline-block px-8 py-3.5 bg-gold text-black font-bold rounded-xl hover:bg-gold-hover transition-all hover:-translate-y-0.5"
            >
              Рассчитать стоимость моего авто
            </a>
          </div>
        </AnimateOnScroll>
      </div>
    </section>
  );
}
