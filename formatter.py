"""Format calculation results and generate Telegram posts."""

import html
import random
from decimal import Decimal, ROUND_DOWN

# БПСВ-фразы для постов — каждая закрывает боль/страх/потребность/возражение
BPSV_PHRASES = [
    # Боль: переплата на вторичке
    "Оформляем на физлицо — вы первый владелец в РФ. "
    "Экспертиза до оплаты, договор до первого платежа.",

    # Боль: сложно и непонятно
    "Независимая экспертиза до оплаты. "
    "Договор подписываем до первого платежа — вы защищены на каждом этапе.",

    # Боль: утильсбор
    "Утильсбор 3 400 ₽ вместо 800 000+ ₽ — оформляем на физлицо. "
    "Страховка от двери до двери на полную стоимость.",

    # Потребность: документы
    "Оплата поэтапная, все документы (ПТС, ГТД, СБКТС) готовим мы. "
    "Вам остаётся только ГИБДД.",

    # Страх: обманут
    "Договор до оплаты, экспертиза до покупки. "
    "Таможенные платежи списываются с вашего личного счёта в ФТС.",

    # Страх: проблемы с документами
    "Таможенные платежи уплачены полностью, доплат не будет. "
    "Все документы на ваше имя — вы полноправный владелец.",

    # Страх: битый/утопленник
    "Экспертиза до оплаты за авто. "
    "В Китае эксперт несёт личную ответственность за достоверность отчёта. Гарантия 90 дней.",

    # Возражение: долго
    "Доставка 25–45 дней. Договор до первого платежа, "
    "оплата поэтапная — видно прогресс на каждом шаге.",

    # Возражение: не доверяю
    "Оплата через валютный контроль банка — не на карту, не на крипту. "
    "Каждый этап подтверждён документом.",

    # Потребность: первый владелец
    "Автомобиль оформляется на вас — вы полноправный владелец. "
    "Это не лазейка, а закон.",

    # Боль: страшно покупать из Китая
    "Страховка на полную стоимость от двери до двери. "
    "Договор подписываем до первого платежа, экспертиза до оплаты.",

    # Возражение: сам найду дешевле
    "Независимая экспертиза исключает ДТП и скрученный пробег. "
    "Покупка без проверки = риск на сотни тысяч рублей.",

    # Потребность: прозрачность
    "Прозрачный процесс: договор, экспертиза, оплата через банк. "
    "Таможенные платежи на ваше имя — никаких серых схем.",

    # Страх: потеряю при перепродаже
    "Вы — первый владелец в РФ, чистый ПТС. "
    "При перепродаже никаких вопросов по документам.",

    # Боль: дорого в РФ
    "Экономия 20–40% от цен вторичного рынка РФ. "
    "Оформляем на физлицо — утильсбор 3 400 ₽ вместо 800 000+ ₽.",

    # Потребность: всё включено
    "Полный цикл: подбор, экспертиза, таможня, доставка, документы. "
    "Вам остаётся только поставить на учёт в ГИБДД.",

    # Страх: нелегально
    "Легальный ввоз на физлицо: договор, квитанции ФТС, ПТС на ваше имя. "
    "Это закон, не серая схема.",

    # Возражение: доплаты
    "Цена под ключ — без скрытых доплат. "
    "Таможня, логистика, брокер, документы — всё включено.",
]


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
        f"🚩 Пробег:  {_fmt(Decimal(c.get('mileage_km', 0)), 0)} км\n"
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
    """Generate a ready-to-publish Telegram channel post — БПСВ styled."""
    c = calc
    grand_total = _fmt_rub(c['grand_total'])
    mileage = int(c.get('mileage_km', 0))
    year = c['year']

    # Title: brand + price + city (hooks through benefit)
    title = f"<b>{car_name} за {grand_total} ₽ под ключ в Казань</b>"

    # БПСВ paragraph: concrete facts, random phrase
    bpsv_phrase = random.choice(BPSV_PHRASES)
    if mileage > 0:
        bpsv = f"Пробег {_fmt(Decimal(mileage), 0)} км, {year} год.\n<b>{bpsv_phrase}</b>"
    else:
        bpsv = f"{year} год.\n<b>{bpsv_phrase}</b>"

    post = (
        f"{title}\n\n"

        f"{bpsv}\n\n"

        f"▫️ <b>Модель:</b>  {car_name}\n"
        f"▫️ <b>Год выпуска:</b>  {year}\n"
        f"▫️ <b>Объём двигателя:</b>  {c['engine_cc']} см³\n"
        f"▫️ <b>Мощность:</b>  {_fmt(c['hp'], 0)} л.с.\n"
        f"▫️ <b>Пробег:</b>  {_fmt(Decimal(mileage), 0)} км\n"
        f"▫️ <b>Двигатель:</b>  {c['engine_type']}\n\n"

        "─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─\n\n"

        f"🏎 Автомобиль в наличии.\n"
        f"Полный цикл доставки и оформления под ключ\n"
        f"в любой город России.\n\n"

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

    brand = c.get("brand", "")
    if brand:
        post += f"\n\n#{brand.upper()}"

    return post
