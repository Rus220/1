import AnimateOnScroll from "./AnimateOnScroll";

const steps = [
  {
    num: "01",
    title: "Подбор авто под бюджет",
    text: "Подбираем варианты на проверенных площадках Китая и Кореи. Отправляем фото, видео, характеристики и реальные цены.",
  },
  {
    num: "02",
    title: "Проверка и отчёты",
    text: "Полная техническая диагностика: кузов, двигатель, трансмиссия, электроника. Видеоосмотр + фотоотчёт до покупки.",
  },
  {
    num: "03",
    title: "Заключение договора",
    text: "Подписываем официальный договор с фиксированной стоимостью. Все условия прозрачны — никаких сюрпризов.",
  },
  {
    num: "04",
    title: "Выкуп и доставка",
    text: "Выкупаем авто, организуем логистику: автовоз или контейнер. Вы отслеживаете перемещение в реальном времени.",
  },
  {
    num: "05",
    title: "Таможня и выдача",
    text: "Растаможка, получение ЭПТС, постановка на учёт. Передаём готовый к эксплуатации автомобиль с документами.",
  },
];

export default function Process() {
  return (
    <section id="process" className="py-20 bg-dark-900">
      <div className="max-w-6xl mx-auto px-5">
        <AnimateOnScroll>
          <h2 className="text-3xl md:text-4xl font-extrabold text-center mb-3 tracking-tight">
            Как мы <span className="text-gold">работаем</span>
          </h2>
        </AnimateOnScroll>
        <AnimateOnScroll>
          <p className="text-center text-white/55 mb-14 max-w-lg mx-auto">
            5 понятных шагов от заявки до вашего нового авто
          </p>
        </AnimateOnScroll>

        <div className="max-w-2xl mx-auto relative">
          {/* Timeline line */}
          <div className="absolute left-6 top-0 bottom-0 w-0.5 bg-gradient-to-b from-gold to-gold/10 hidden md:block" />

          {steps.map((s, i) => (
            <AnimateOnScroll key={s.num} delay={i * 120}>
              <div className="flex gap-6 mb-8 last:mb-0">
                <div className="shrink-0 w-12 h-12 rounded-full bg-dark-700 border-2 border-gold flex items-center justify-center text-gold font-black text-sm relative z-10">
                  {s.num}
                </div>
                <div className="pt-2">
                  <h3 className="font-bold text-lg mb-1">{s.title}</h3>
                  <p className="text-white/55 text-sm leading-relaxed">
                    {s.text}
                  </p>
                </div>
              </div>
            </AnimateOnScroll>
          ))}
        </div>
      </div>
    </section>
  );
}
