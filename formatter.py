"""Format calculation results and generate Telegram posts."""

import html
from decimal import Decimal, ROUND_DOWN


def _fmt(value: Decimal, precision: int = 2) -> str:
    """Format Decimal to string with exact digits, with space thousands separator."""
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


def _fmt_rub(value: Decimal) -> str:
    """Format rubles without kopecks (truncate to whole number)."""
    whole = value.quantize(Decimal("1"), rounding=ROUND_DOWN)
    return _fmt(whole, 0)


def format_calculation(calc: dict, cbr_date: str) -> str:
    """Format the full calculation breakdown — premium styled."""
    c = calc

    text = (
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "📊  <b>РАСЧЁТ СТОИМОСТИ</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"

        f"🏷 <b>Автомобиль:</b>  {c.get('car_name', 'Н/Д')}\n\n"

        f"🌍 Страна:  Китай (CNY)\n"
        f"💴 Цена:  {_fmt(c['price_cny'], 0)} CNY\n"
        f"📅 Возраст:  {c['year']} г. → категория <b>{c['age_category']}</b>\n"
        f"⚙️ Объём:  {c['engine_cc']} см³\n"
        f"🐎 Мощность:  {_fmt(c['hp'], 0)} л.с.\n"
        f"🔧 Двигатель:  {c['engine_type']}\n\n"

        "┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈\n"
        f"💱 Курс ВТБ:  <b>{_fmt(c['vtb_rate'], 4)} ₽</b> за 1 CNY\n"
        f"🏦 Курсы ЦБ РФ ({cbr_date}):\n"
        f"     CNY ≈ {_fmt(c['cny_cbr'], 4)}  |  EUR ≈ {_fmt(c['eur_cbr'], 4)}\n"
        "┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈\n\n"

        "🚗  <b>АВТОМОБИЛЬ</b>\n\n"

        f"     Цена авто:  {_fmt(c['price_cny'], 0)} CNY = <b>{_fmt(c['invoice_rub'])} ₽</b>\n"
        f"     Инвойс:  {_fmt(c['invoice_rub'])} ₽\n"
        f"     Комиссия банка 2%:  {_fmt(c['bank_commission'])} ₽\n\n"

        "🛃  <b>ТАМОЖНЯ</b>\n\n"

        f"     Инвойс в EUR:  {_fmt(c['invoice_eur'])} €\n"
        f"     Пошлина:  {_fmt(c['duty_eur'])} € = <b>{_fmt(c['duty_rub'])} ₽</b>\n"
        f"     <i>({html.escape(c['duty_method'])})</i>\n"
        f"     Оформление:  {_fmt(c['processing_fee'], 0)} ₽\n"
        f"     <i>({html.escape(c['processing_info'])})</i>\n"
        f"     Утильсбор:  {_fmt(c['util_fee'], 0)} ₽\n"
        f"     <i>({html.escape(c['util_info'])})</i>\n"
        f"     Таможня итого:  <b>{_fmt(c['customs_total'])} ₽</b>\n\n"

        "📦  <b>ПРОЧЕЕ</b>\n\n"

        f"     Логистика до Казани:  {_fmt(c['logistics'], 0)} ₽\n"
        f"     Брокерские услуги:  {_fmt(c['broker'], 0)} ₽\n"
        f"     Комиссия:  {_fmt(c['commission'], 0)} ₽\n\n"

        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"💰  <b>ИТОГО «ПОД КЛЮЧ» в Казань:</b>\n"
        f"🔥  <b>{_fmt_rub(c['grand_total'])} ₽</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"

        "⚠️ <i>Расчёт предварительный.\n"
        "Итоговая сумма зависит от курсов ЦБ РФ на дату оплаты.</i>"
    )
    return text


def format_telegram_post(calc: dict, car_name: str, bot_username: str = "zakazRUSTEAMBOT") -> str:
    """Generate a ready-to-publish Telegram channel post — premium styled."""
    c = calc
    grand_total = _fmt_rub(c['grand_total'])

    post = (
        f"✨🚘 <b>{car_name}</b>\n"
        f"Выгодно и надёжно из Китая!\n\n"

        f"Отличный выбор для тех, кто хочет современный\n"
        f"автомобиль с богатым оснащением по лучшей цене.\n\n"

        f"▫️ <b>Модель:</b>  {car_name}\n"
        f"▫️ <b>Год выпуска:</b>  {c['year']}\n"
        f"▫️ <b>Объём двигателя:</b>  {c['engine_cc']} см³\n"
        f"▫️ <b>Мощность:</b>  {_fmt(c['hp'], 0)} л.с.\n"
        f"▫️ <b>Двигатель:</b>  {c['engine_type']}\n\n"

        "─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─\n\n"

        f"🏎 Автомобиль в наличии.\n"
        f"Полный цикл доставки и оформления под ключ.\n\n"

        f"💰 <b>Стоимость под ключ в Казань:</b>\n"
        f"🔥 <b>{grand_total} ₽</b>\n\n"

        f"💱 Курс ВТБ: {_fmt(c['vtb_rate'], 4)} ₽ за 1 CNY\n\n"

        "─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─\n\n"

        f"💎 <a href=\"https://t.me/{bot_username}\"><b>БЕСПЛАТНЫЙ РАСЧЁТ ЦЕНЫ</b></a>\n\n"

        f"Хотите бесплатный расчёт именно вашего\n"
        f"автомобиля — напишите нам! 👇\n\n"

        f"📱 Telegram: @vivat116\n"
        f"💬 WA <a href=\"https://wa.me/79612475867\">79612475867</a>\n"
        f"☎️ Телефон: +79612475867"
    )
    return post
