import AnimateOnScroll from "./AnimateOnScroll";

export default function About() {
  return (
    <section id="about" className="py-20 bg-dark-800">
      <div className="max-w-6xl mx-auto px-5">
        <AnimateOnScroll>
          <h2 className="text-3xl md:text-4xl font-extrabold text-center mb-3 tracking-tight">
            О <span className="text-gold">компании</span>
          </h2>
        </AnimateOnScroll>

        <AnimateOnScroll delay={100}>
          <div className="max-w-3xl mx-auto mt-10 bg-dark-700 border border-white/[0.06] rounded-3xl p-8 md:p-10">
            <div className="flex flex-col md:flex-row gap-8 items-center">
              {/* Avatar placeholder */}
              <div className="shrink-0 w-28 h-28 bg-dark-600 rounded-2xl flex items-center justify-center border border-white/[0.08]">
                <span className="text-4xl font-black text-gold">RS</span>
              </div>

              <div>
                <h3 className="text-xl font-bold mb-3">RUSTEAM — импорт авто из Китая и&nbsp;Кореи</h3>
                <div className="space-y-3 text-white/55 text-sm leading-relaxed">
                  <p>
                    Мы — команда, которая занимается подбором и доставкой автомобилей из Китая и
                    Кореи в Россию. Не перекупщики и не посредники.
                    Работаем напрямую с площадками и дилерами.
                  </p>
                  <p>
                    За время работы привезли более 150 автомобилей.
                    Каждый клиент получает персонального менеджера, доступ к фото- и видеоотчётам
                    и полное сопровождение от подбора до постановки на учёт.
                  </p>
                  <p>
                    Наш принцип: вы платите за результат, а не за обещания.
                    Поэтому работаем по договору с фиксированной ценой и поэтапной оплатой.
                  </p>
                </div>
              </div>
            </div>

            {/* Stats */}
            <div className="grid grid-cols-3 gap-4 mt-8 pt-8 border-t border-white/[0.06]">
              {[
                { val: "150+", label: "авто доставлено" },
                { val: "25–45", label: "дней доставка" },
                { val: "100%", label: "по договору" },
              ].map((s) => (
                <div key={s.label} className="text-center">
                  <div className="text-2xl font-black text-gold">{s.val}</div>
                  <div className="text-xs text-white/40 mt-1">{s.label}</div>
                </div>
              ))}
            </div>
          </div>
        </AnimateOnScroll>
      </div>
    </section>
  );
}
