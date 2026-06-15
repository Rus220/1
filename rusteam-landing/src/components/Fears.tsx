"use client";

import { useState } from "react";
import AnimateOnScroll from "./AnimateOnScroll";

const fears = [
  {
    q: "А если авто придёт с дефектами?",
    a: "Мы проводим полную техническую проверку до покупки: кузов, ЛКП, электроника, двигатель. Если авто не проходит — ищем другой вариант. Плюс все автомобили застрахованы на время перевозки.",
  },
  {
    q: "А если потеряю деньги?",
    a: "Работаем по официальному договору. Оплата поэтапная — вы не переводите всю сумму сразу. Каждый платёж подтверждён документально. Риск потери денег исключён.",
  },
  {
    q: "А если цена вырастет в процессе?",
    a: "Итоговая стоимость фиксируется в договоре до начала работы. Курс, пошлины, логистика — всё учтено заранее. Никаких «допрасходов» по ходу.",
  },
  {
    q: "Сколько времени занимает доставка?",
    a: "Из Кореи — 15–25 дней, из Китая — 20–35 дней. Зависит от города назначения. Мы информируем о статусе на каждом этапе в реальном времени.",
  },
  {
    q: "Можно привезти конкретную модель и комплектацию?",
    a: "Да, работаем под заказ. Вы называете марку, модель, цвет, комплектацию и бюджет — мы находим точное совпадение на рынках Китая и Кореи.",
  },
  {
    q: "Что входит в стоимость «под ключ»?",
    a: "Всё: подбор, проверка, выкуп, доставка, растаможка, получение ЭПТС, постановка на учёт. Финальная сумма — в договоре. Скрытых платежей нет.",
  },
  {
    q: "Будет ли гарантия?",
    a: "Для новых авто от дилера — сохраняется заводская гарантия. Для б/у — мы гарантируем юридическую чистоту и соответствие заявленному техническому состоянию.",
  },
  {
    q: "Какие авто выгоднее всего привозить?",
    a: "Максимальная выгода — электромобили и гибриды из Китая (Li, Zeekr, BYD). Из Кореи — Hyundai, Kia, Genesis. Экономия 20–40% от цены в РФ.",
  },
];

export default function Fears() {
  const [openIndex, setOpenIndex] = useState<number | null>(null);

  return (
    <section id="fears" className="py-20 bg-dark-800">
      <div className="max-w-6xl mx-auto px-5">
        <AnimateOnScroll>
          <h2 className="text-3xl md:text-4xl font-extrabold text-center mb-3 tracking-tight">
            Снимаем <span className="text-gold">страхи</span>
          </h2>
        </AnimateOnScroll>
        <AnimateOnScroll>
          <p className="text-center text-white/55 mb-12 max-w-lg mx-auto">
            Честные ответы на вопросы, которые вы боитесь задать
          </p>
        </AnimateOnScroll>

        <div className="max-w-2xl mx-auto">
          {fears.map((f, i) => (
            <AnimateOnScroll key={i}>
              <div className="border-b border-white/[0.06] first:border-t">
                <button
                  onClick={() => setOpenIndex(openIndex === i ? null : i)}
                  className="w-full flex items-center justify-between gap-4 py-5 text-left font-semibold hover:text-gold transition-colors"
                  aria-expanded={openIndex === i}
                >
                  <span>{f.q}</span>
                  <svg
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="2"
                    className={`w-5 h-5 shrink-0 text-white/30 transition-transform duration-300 ${
                      openIndex === i ? "rotate-180 text-gold" : ""
                    }`}
                  >
                    <polyline points="6 9 12 15 18 9" />
                  </svg>
                </button>
                <div
                  className={`overflow-hidden transition-all duration-400 ${
                    openIndex === i ? "max-h-60 pb-5" : "max-h-0"
                  }`}
                >
                  <p className="text-white/55 text-sm leading-relaxed">
                    {f.a}
                  </p>
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
              Задать свой вопрос
            </a>
          </div>
        </AnimateOnScroll>
      </div>
    </section>
  );
}
