import AnimateOnScroll from "./AnimateOnScroll";

const items = [
  {
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="w-8 h-8">
        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
        <polyline points="14 2 14 8 20 8" />
        <line x1="16" y1="13" x2="8" y2="13" />
        <line x1="16" y1="17" x2="8" y2="17" />
      </svg>
    ),
    title: "Работаем по договору",
    text: "Официальный договор с полным описанием условий, сроков и стоимости. Юридическая защита на каждом этапе.",
  },
  {
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="w-8 h-8">
        <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
        <path d="M9 12l2 2 4-4" />
      </svg>
    ),
    title: "150+ автомобилей доставлено",
    text: "Реальный опыт. Каждый кейс — с фотоотчётом. Спросите, покажем документы по любой сделке.",
  },
  {
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="w-8 h-8">
        <line x1="12" y1="1" x2="12" y2="23" />
        <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6" />
      </svg>
    ),
    title: "Прозрачная стоимость",
    text: "Итоговая цена фиксируется в договоре до начала работ. Без скрытых комиссий и «допрасходов».",
  },
  {
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="w-8 h-8">
        <polygon points="23 7 16 12 23 17 23 7" />
        <rect x="1" y="5" width="15" height="14" rx="2" ry="2" />
      </svg>
    ),
    title: "Отчёты на каждом этапе",
    text: "Фото, видео, скриншоты — от осмотра на площадке до погрузки и получения. Полная прозрачность.",
  },
];

export default function Trust() {
  return (
    <section id="trust" className="py-20 bg-dark-900">
      <div className="max-w-6xl mx-auto px-5">
        <AnimateOnScroll>
          <h2 className="text-3xl md:text-4xl font-extrabold text-center mb-3 tracking-tight">
            Почему нам <span className="text-gold">доверяют</span>
          </h2>
        </AnimateOnScroll>
        <AnimateOnScroll>
          <p className="text-center text-white/55 mb-12 max-w-lg mx-auto">
            Факты вместо обещаний. Документы вместо слов.
          </p>
        </AnimateOnScroll>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
          {items.map((item, i) => (
            <AnimateOnScroll key={item.title} delay={i * 100}>
              <div className="bg-dark-700 border border-white/[0.06] rounded-2xl p-6 hover:border-gold/15 transition-all text-center">
                <div className="text-gold mb-4 flex justify-center">{item.icon}</div>
                <h3 className="font-bold text-base mb-2">{item.title}</h3>
                <p className="text-white/50 text-sm leading-relaxed">{item.text}</p>
              </div>
            </AnimateOnScroll>
          ))}
        </div>
      </div>
    </section>
  );
}
