"""Customs duty calculator for cars imported to Russia (2026 rules)."""

from decimal import Decimal, ROUND_HALF_UP


# ---------------------------------------------------------------------------
# Duty tables
# ---------------------------------------------------------------------------

# 0-3 years: list of (max_invoice_eur, percent, eur_per_cc)
DUTY_0_3: list[tuple[Decimal, Decimal, Decimal]] = [
    (Decimal("8500"),   Decimal("0.54"), Decimal("2.5")),
    (Decimal("16700"),  Decimal("0.48"), Decimal("3.5")),
    (Decimal("42300"),  Decimal("0.48"), Decimal("5.5")),
    (Decimal("84500"),  Decimal("0.48"), Decimal("7.5")),
    (Decimal("169000"), Decimal("0.48"), Decimal("15")),
    (Decimal("999999999"), Decimal("0.48"), Decimal("20")),
]

# 3-5 years: eur per cc by engine volume range
DUTY_3_5: list[tuple[int, Decimal]] = [
    (1000,  Decimal("1.5")),
    (1500,  Decimal("1.7")),
    (1800,  Decimal("2.5")),
    (2300,  Decimal("2.7")),
    (3000,  Decimal("3.0")),
    (999999, Decimal("3.6")),
]

# 5+ years: eur per cc by engine volume range
DUTY_5_PLUS: list[tuple[int, Decimal]] = [
    (1000,  Decimal("3.0")),
    (1500,  Decimal("3.2")),
    (1800,  Decimal("3.5")),
    (2300,  Decimal("4.8")),
    (3000,  Decimal("5.0")),
    (999999, Decimal("5.7")),
]

# Customs processing fee by invoice amount in rubles
CUSTOMS_PROCESSING: list[tuple[Decimal, Decimal]] = [
    (Decimal("200000"),   Decimal("1231")),
    (Decimal("450000"),   Decimal("2462")),
    (Decimal("1200000"),  Decimal("4924")),
    (Decimal("2700000"),  Decimal("13541")),
    (Decimal("4200000"),  Decimal("18465")),
    (Decimal("5500000"),  Decimal("21344")),
    (Decimal("10000000"), Decimal("49240")),
    (Decimal("999999999999"), Decimal("73860")),
]

# Recycling fee (utilisation) 2026 — full commercial rates by engine volume
UTIL_FULL: list[tuple[int, Decimal]] = [
    (1000,  Decimal("306000")),
    (2000,  Decimal("612000")),
    (3000,  Decimal("918000")),
    (3500,  Decimal("1224000")),
    (999999, Decimal("1530000")),
]

UTIL_FULL_OLD: list[tuple[int, Decimal]] = [
    (1000,  Decimal("405900")),
    (2000,  Decimal("811800")),
    (3000,  Decimal("1217700")),
    (3500,  Decimal("1623600")),
    (999999, Decimal("2029500")),
]

# Logistics / broker / commission constants
LOGISTICS_RUB = Decimal("230000")
BROKER_RUB = Decimal("97000")
COMMISSION_RUB = Decimal("100000")

BANK_COMMISSION_RATE = Decimal("0.02")


def _get_car_age_category(year: int, current_year: int = 2026) -> str:
    age = current_year - year
    if age < 0:
        age = 0
    if age <= 3:
        return "0-3"
    if age <= 5:
        return "3-5"
    if age <= 7:
        return "5-7"
    return "7+"


def _calc_duty_0_3(invoice_eur: Decimal, engine_cc: int) -> tuple[Decimal, str]:
    cc = Decimal(engine_cc)
    for max_eur, pct, eur_cc in DUTY_0_3:
        if invoice_eur <= max_eur:
            by_percent = invoice_eur * pct
            by_volume = cc * eur_cc
            duty = max(by_percent, by_volume)
            method = f"max({pct * 100}% = {by_percent} €, {eur_cc} €/см³ = {by_volume} €)"
            return duty, method
    last = DUTY_0_3[-1]
    by_percent = invoice_eur * last[1]
    by_volume = cc * last[2]
    duty = max(by_percent, by_volume)
    method = f"max({last[1] * 100}% = {by_percent} €, {last[2]} €/см³ = {by_volume} €)"
    return duty, method


def _calc_duty_by_volume(engine_cc: int, table: list[tuple[int, Decimal]]) -> tuple[Decimal, str]:
    cc = Decimal(engine_cc)
    for max_cc, eur_cc in table:
        if engine_cc <= max_cc:
            duty = cc * eur_cc
            method = f"{eur_cc} €/см³ × {engine_cc} см³"
            return duty, method
    last = table[-1]
    duty = cc * last[1]
    method = f"{last[1]} €/см³ × {engine_cc} см³"
    return duty, method


def _get_customs_processing(invoice_rub: Decimal) -> tuple[Decimal, str]:
    for max_rub, fee in CUSTOMS_PROCESSING:
        if invoice_rub <= max_rub:
            return fee, f"инвойс ≤ {max_rub} ₽"
    return CUSTOMS_PROCESSING[-1][1], f"> 10 000 000 ₽"


def _get_util_fee(year: int, hp: Decimal, engine_cc: int, engine_type: str,
                  current_year: int = 2026) -> tuple[Decimal, str]:
    age = current_year - year
    if age < 0:
        age = 0

    is_individual_benefit = (
        engine_type.upper() in ("ДВС", "БЕНЗИН", "ДИЗЕЛЬ", "ГИБРИД")
        and hp <= Decimal("160")
        and engine_cc < 3000
    )

    if is_individual_benefit:
        if age <= 3:
            return Decimal("3400"), "льгота физлицо (ДВС ≤160 л.с. <3000 см³, до 3 лет)"
        else:
            return Decimal("5200"), "льгота физлицо (ДВС ≤160 л.с. <3000 см³, старше 3 лет)"

    table = UTIL_FULL if age <= 3 else UTIL_FULL_OLD
    for max_cc, fee in table:
        if engine_cc <= max_cc:
            label = "до 3 лет" if age <= 3 else "старше 3 лет"
            return fee, f"полная ставка ({label}, ≤{max_cc} см³)"
    last = table[-1]
    label = "до 3 лет" if age <= 3 else "старше 3 лет"
    return last[1], f"полная ставка ({label})"


def calculate(
    price_cny: Decimal,
    vtb_rate: Decimal,
    eur_cbr: Decimal,
    cny_cbr: Decimal,
    engine_cc: int,
    hp: Decimal,
    year: int,
    engine_type: str = "ДВС",
    current_year: int = 2026,
) -> dict:
    """Full customs calculation. Returns dict with all intermediate and final values."""

    # Step 1: Invoice in rubles
    invoice_rub = price_cny * vtb_rate

    # Step 2: Bank commission
    bank_commission = invoice_rub * BANK_COMMISSION_RATE

    # Step 3: Invoice in EUR
    invoice_eur = invoice_rub / eur_cbr

    # Step 4: Duty
    age_cat = _get_car_age_category(year, current_year)
    if age_cat == "0-3":
        duty_eur, duty_method = _calc_duty_0_3(invoice_eur, engine_cc)
    elif age_cat == "3-5":
        duty_eur, duty_method = _calc_duty_by_volume(engine_cc, DUTY_3_5)
    else:  # 5-7 and 7+
        duty_eur, duty_method = _calc_duty_by_volume(engine_cc, DUTY_5_PLUS)

    duty_rub = duty_eur * eur_cbr

    # Step 5: Customs processing
    processing_fee, processing_info = _get_customs_processing(invoice_rub)

    # Step 6: Recycling fee
    util_fee, util_info = _get_util_fee(year, hp, engine_cc, engine_type, current_year)

    # Step 7: Customs total
    customs_total = duty_rub + processing_fee + util_fee

    # Step 8: Grand total
    grand_total = (
        invoice_rub
        + bank_commission
        + customs_total
        + LOGISTICS_RUB
        + BROKER_RUB
        + COMMISSION_RUB
    )

    return {
        "price_cny": price_cny,
        "vtb_rate": vtb_rate,
        "eur_cbr": eur_cbr,
        "cny_cbr": cny_cbr,
        "engine_cc": engine_cc,
        "hp": hp,
        "year": year,
        "engine_type": engine_type,
        "age_category": age_cat,
        "invoice_rub": invoice_rub,
        "bank_commission": bank_commission,
        "invoice_eur": invoice_eur,
        "duty_eur": duty_eur,
        "duty_method": duty_method,
        "duty_rub": duty_rub,
        "processing_fee": processing_fee,
        "processing_info": processing_info,
        "util_fee": util_fee,
        "util_info": util_info,
        "customs_total": customs_total,
        "logistics": LOGISTICS_RUB,
        "broker": BROKER_RUB,
        "commission": COMMISSION_RUB,
        "grand_total": grand_total,
    }
