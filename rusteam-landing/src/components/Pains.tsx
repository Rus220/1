import AnimateOnScroll from "./AnimateOnScroll";

const pains = [
  {
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="w-7 h-7">
        <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z" />
        <line x1="12" y1="9" x2="12" y2="13" />
        <line x1="12" y1="17" x2="12.01" y2="17" />
      </svg>
    ),
    title: "Скрытые повреждения",
    text: "Авто с ДТП, коррозией или восстановленным кузовом — без проверки вы не узнаете",
  },
  {
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="w-7 h-7">
        <circle cx="12" cy="12" r="10" />
        <polyline points="12 6 12 12 16 14" />
      </svg>
    ),
    title: "Скрученный пробег",
    text: "До 40% авто на вторичном рынке имеют скрученный пробег. Это влияет на ресурс",
  },
  {
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="w-7 h-7">
        <line x1="12" y1="1" x2="12" y2="23" />
        <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6" />
      </svg>
    ),
    title: "Обман с ценой",
    text: "Заниженная цена в объявлении, а потом «дополнительные расходы» — классическая схема",
  },
  {
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="w-7 h-7">
        <rect x="1" y="4" width="22" height="16" rx="2" ry="2" />
        <line x1="1" y1="10" x2="23" y2="10" />
      </svg>
    ),
    title: "Потеря денег при переводе",
    text: "Перевод денег за границу без гарантий — риск потерять всё без возможности возврата",
  },
  {
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="w-7 h-7">
        <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" />
        <circle cx="12" cy="12" r="3" />
      </svg>
    ),
    title: "Отсутствие контроля",
    text: "Вы не видите процесс: где авто, в каком состоянии, что происходит на таможне",
  },
];

export default function Pains() {
  return (
    <section id="pains" className="py-20 bg-dark-800">
      <div className="max-w-6xl mx-auto px-5">
        <AnimateOnScroll>
          <h2 className="text-3xl md:text-4xl font-extrabold text-center mb-3 tracking-tight">
            С чем вы <span className="text-gold">рискуете столкнуться</span>
          </h2>
        </AnimateOnScroll>
        <AnimateOnScroll>
          <p className="text-center text-white/55 mb-12 max-w-lg mx-auto">
            Покупка авто за рубежом без проверенного партнёра — это лотерея
          </p>
        </AnimateOnScroll>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
          {pains.map((p, i) => (
            <AnimateOnScroll key={p.title} delay={i * 100}>
              <div className="bg-dark-700 border border-white/[0.06] rounded-2xl p-6 hover:border-gold/15 hover:-translate-y-1 transition-all group">
                <div className="text-gold mb-4 group-hover:scale-110 transition-transform">
                  {p.icon}
                </div>
                <h3 className="font-bold text-lg mb-2">{p.title}</h3>
                <p className="text-white/55 text-sm leading-relaxed">{p.text}</p>
              </div>
            </AnimateOnScroll>
          ))}
        </div>

        {/* Inline CTA */}
        <AnimateOnScroll>
          <div className="text-center mt-12">
            <p className="text-white/50 mb-4 text-sm">
              Мы закрываем все эти риски — проверка, договор, контроль
            </p>
            <a
              href="#lead"
              className="inline-block px-8 py-3.5 bg-gold text-black font-bold rounded-xl hover:bg-gold-hover transition-all hover:-translate-y-0.5"
            >
              Получить консультацию
            </a>
          </div>
        </AnimateOnScroll>
      </div>
    </section>
  );
}
