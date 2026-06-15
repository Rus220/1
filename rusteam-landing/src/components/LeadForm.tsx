"use client";

import { useState, type FormEvent } from "react";

export default function LeadForm() {
  const [name, setName] = useState("");
  const [phone, setPhone] = useState("");
  const [errors, setErrors] = useState<{ name?: string; phone?: string }>({});
  const [status, setStatus] = useState<"idle" | "sending" | "success" | "error">("idle");

  function formatPhone(raw: string) {
    const digits = raw.replace(/\D/g, "");
    let d = digits;
    if (d.startsWith("8")) d = "7" + d.slice(1);
    if (!d.startsWith("7") && d.length > 0) d = "7" + d;

    let formatted = "";
    if (d.length === 0) return "";
    formatted = "+7 ";
    if (d.length > 1) formatted += "(" + d.substring(1, 4);
    if (d.length >= 4) formatted += ") ";
    if (d.length > 4) formatted += d.substring(4, 7);
    if (d.length > 7) formatted += "-" + d.substring(7, 9);
    if (d.length > 9) formatted += "-" + d.substring(9, 11);
    return formatted;
  }

  function handlePhoneChange(val: string) {
    setPhone(formatPhone(val));
    if (errors.phone) setErrors((e) => ({ ...e, phone: undefined }));
  }

  function handleNameChange(val: string) {
    setName(val);
    if (errors.name) setErrors((e) => ({ ...e, name: undefined }));
  }

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    const newErrors: typeof errors = {};

    if (!name.trim()) newErrors.name = "Укажите имя";
    const phoneDigits = phone.replace(/\D/g, "");
    if (phoneDigits.length < 11) newErrors.phone = "Укажите корректный номер";

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    setStatus("sending");

    try {
      const res = await fetch("/api/lead", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: name.trim(), phone: phone.trim() }),
      });
      if (res.ok) {
        setStatus("success");
      } else {
        setStatus("error");
      }
    } catch {
      setStatus("error");
    }
  }

  if (status === "success") {
    return (
      <section id="lead" className="py-20 bg-dark-900">
        <div className="max-w-xl mx-auto px-5 text-center">
          <div className="bg-dark-700 border border-white/[0.06] rounded-3xl p-10">
            <div className="w-16 h-16 mx-auto mb-5 text-success">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" />
                <polyline points="22 4 12 14.01 9 11.01" />
              </svg>
            </div>
            <h3 className="text-2xl font-extrabold mb-3">Заявка отправлена!</h3>
            <p className="text-white/55 mb-6">
              Мы свяжемся с вами в течение 15 минут и подготовим расчёт.
            </p>
            <a
              href="https://t.me/vivat116"
              target="_blank"
              rel="noopener"
              className="inline-flex items-center gap-2 px-6 py-3 bg-tg text-white rounded-xl font-semibold hover:bg-tg/80 transition-colors"
            >
              Написать в Telegram
            </a>
          </div>
        </div>
      </section>
    );
  }

  return (
    <section id="lead" className="py-20 bg-dark-900">
      <div className="max-w-xl mx-auto px-5">
        <div className="bg-dark-700 border border-white/[0.06] rounded-3xl p-8 md:p-10 relative overflow-hidden">
          {/* Gradient border top */}
          <div className="absolute top-0 left-0 right-0 h-[3px] bg-gradient-to-r from-gold to-tg" />

          <h2 className="text-2xl md:text-3xl font-extrabold text-center mb-2 tracking-tight">
            Рассчитайте стоимость <span className="text-gold">бесплатно</span>
          </h2>
          <p className="text-center text-white/50 mb-8 text-sm">
            Оставьте контакт — подготовим расчёт под ваш бюджет за 15 минут
          </p>

          <form onSubmit={handleSubmit} noValidate className="space-y-5">
            <div>
              <label className="block text-sm font-semibold text-white/60 mb-1.5">
                Ваше имя
              </label>
              <input
                type="text"
                value={name}
                onChange={(e) => handleNameChange(e.target.value)}
                placeholder="Иван"
                className={`w-full px-4 py-3.5 bg-dark-900 border rounded-xl text-white placeholder:text-white/30 outline-none transition-all focus:ring-2 focus:ring-gold/30 ${
                  errors.name ? "border-danger" : "border-white/[0.08] focus:border-gold/50"
                }`}
              />
              {errors.name && (
                <p className="text-danger text-xs mt-1">{errors.name}</p>
              )}
            </div>

            <div>
              <label className="block text-sm font-semibold text-white/60 mb-1.5">
                Телефон
              </label>
              <input
                type="tel"
                value={phone}
                onChange={(e) => handlePhoneChange(e.target.value)}
                onFocus={() => {
                  if (!phone) setPhone("+7 (");
                }}
                placeholder="+7 (___) ___-__-__"
                className={`w-full px-4 py-3.5 bg-dark-900 border rounded-xl text-white placeholder:text-white/30 outline-none transition-all focus:ring-2 focus:ring-gold/30 ${
                  errors.phone ? "border-danger" : "border-white/[0.08] focus:border-gold/50"
                }`}
              />
              {errors.phone && (
                <p className="text-danger text-xs mt-1">{errors.phone}</p>
              )}
            </div>

            <button
              type="submit"
              disabled={status === "sending"}
              className="w-full py-4 bg-gold text-black font-bold text-base rounded-xl hover:bg-gold-hover transition-all hover:-translate-y-0.5 disabled:opacity-60 disabled:cursor-not-allowed flex items-center justify-center gap-2"
            >
              {status === "sending" ? (
                "Отправка..."
              ) : (
                <>
                  Получить бесплатный расчёт
                  <svg
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="2"
                    className="w-5 h-5"
                  >
                    <path d="M5 12h14M12 5l7 7-7 7" />
                  </svg>
                </>
              )}
            </button>

            {status === "error" && (
              <p className="text-danger text-sm text-center">
                Ошибка отправки. Напишите нам в{" "}
                <a
                  href="https://t.me/vivat116"
                  target="_blank"
                  rel="noopener"
                  className="underline"
                >
                  Telegram
                </a>
              </p>
            )}

            <p className="text-center text-white/30 text-xs">
              Нажимая кнопку, вы соглашаетесь с обработкой персональных данных
            </p>
          </form>
        </div>
      </div>
    </section>
  );
}
