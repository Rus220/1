"""Format calculation results and generate Telegram posts."""

from decimal import Decimal


def _fmt(value: Decimal, precision: int = 2) -> str:
    """Format Decimal to string with exact digits, no rounding, with space thousands separator."""
    if precision == 0:
        s = str(value.quantize(Decimal("1")))
    else:
        q = Decimal("0." + "0" * precision)
        s = str(value.quantize(q))

    parts = s.split(".")
    integer_part = parts[0]

    sign = ""
    if integer_part.startswith("-"):
        sign = "-"
        integer_part = integer_part[1:]

    formatted_int = ""
    for i, ch in enumerate(reversed(integer_part)):
        if i > 0 and i % 3 == 0:
            formatted_int = " " + formatted_int
        formatted_int = ch + formatted_int

    if len(parts) == 2:
        return sign + formatted_int + "." + parts[1]
    return sign + formatted_int


def format_calculation(calc: dict, cbr_date: str) -> str:
    """Format the full calculation breakdown."""
    c = calc

    text = (
        "=== РАСЧЁТ СТОИМОСТИ ===\n"
        f"Автомобиль: {c.get('car_name', 'Н/Д')}\n\n"
        f"Страна: Китай (CNY)\n"
        f"Цена: {_fmt(c['price_cny'], 0)} CNY\n"
        f"Возраст: {c['year']} г. → категория {c['age_category']}\n"
        f"Объём: {c['engine_cc']} см³\n"
        f"Мощность: {_fmt(c['hp'], 0)} л.с.\n"
        f"Двигатель: {c['engine_type']}\n\n"
        f"Курс ВТБ: {_fmt(c['vtb_rate'], 4)} ₽ за 1 CNY\n"
        f"Актуальные курсы ЦБ РФ ({cbr_date}): "
        f"CNY ≈ {_fmt(c['cny_cbr'], 4)} | EUR ≈ {_fmt(c['eur_cbr'], 4)}\n\n"
        "─── Разбивка стоимости ───\n\n"
        "🚗 АВТОМОБИЛЬ\n\n"
        f"Цена авто: {_fmt(c['price_cny'], 0)} CNY = {_fmt(c['invoice_rub'])} ₽\n"
        f"Инвойс: {_fmt(c['invoice_rub'])} ₽\n"
        f"Комиссия банка 2%: {_fmt(c['bank_commission'])} ₽\n\n"
        "🛃 ТАМОЖНЯ\n\n"
        f"Инвойс в EUR: {_fmt(c['invoice_eur'])} €\n"
        f"Пошлина ({c['duty_method']}): {_fmt(c['duty_eur'])} € = {_fmt(c['duty_rub'])} ₽\n"
        f"Таможенное оформление ({c['processing_info']}): {_fmt(c['processing_fee'], 0)} ₽\n"
        f"Утильсбор ({c['util_info']}): {_fmt(c['util_fee'], 0)} ₽\n"
        f"Таможня итого: {_fmt(c['customs_total'])} ₽\n\n"
        "📦 ПРОЧЕЕ\n\n"
        f"Логистика: {_fmt(c['logistics'], 0)} ₽\n"
        f"Брокер: {_fmt(c['broker'], 0)} ₽\n"
        f"Комиссия: {_fmt(c['commission'], 0)} ₽\n\n"
        f"💰 ИТОГО «ПОД КЛЮЧ» в Казань = {_fmt(c['grand_total'])} ₽\n\n"
        "⚠️ Расчёт предварительный. Итоговая сумма зависит от курсов ЦБ РФ на дату оплаты."
    )
    return text


def format_telegram_post(calc: dict, car_name: str, bot_username: str = "zakazRUSTEAMBOT") -> str:
    """Generate a ready-to-publish Telegram channel post."""
    c = calc
    grand_total = _fmt(c['grand_total'])

    post = (
        f"🚘 {car_name} — выгодно и надёжно из Китая!\n\n"
        f"Отличный выбор для тех, кто хочет современный автомобиль "
        f"с богатым оснащением по разумной цене.\n\n"
        f"▪️ Модель: {car_name}\n"
        f"▪️ Год выпуска: {c['year']}\n"
        f"▪️ Объём двигателя: {c['engine_cc']} см³\n"
        f"▪️ Мощность: {_fmt(c['hp'], 0)} л.с.\n"
        f"▪️ Двигатель: {c['engine_type']}\n\n"
        f"Автомобиль в наличии. Полный цикл доставки и оформления под ключ.\n\n"
        f"💰 Стоимость под ключ в Казань: {grand_total} ₽\n"
        f"Курс ВТБ: {_fmt(c['vtb_rate'], 4)} ₽ за 1 CNY\n\n"
        f"💰 БЕСПЛАТНЫЙ РАСЧЁТ ЦЕНЫ — "
        f"<a href=\"https://t.me/{bot_username}\">напишите нам</a>\n\n"
        f"Хотите бесплатный расчёт именно вашего автомобиля — напишите нам!\n\n"
        f"📱 Telegram: @vivat116\n"
        f"💬 WA: +79612475867\n"
        f"☎️ Телефон: +79612475867"
    )
    return post
