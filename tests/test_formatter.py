"""Tests for output formatters."""

from decimal import Decimal

from formatter import _fmt, _fmt_rub, format_calculation, format_telegram_post


class TestFmt:
    def test_simple(self):
        assert _fmt(Decimal("1234.56")) == "1 234.56"

    def test_large(self):
        assert _fmt(Decimal("1234567.89")) == "1 234 567.89"

    def test_zero_precision(self):
        assert _fmt(Decimal("1234"), 0) == "1 234"

    def test_small(self):
        assert _fmt(Decimal("45.12")) == "45.12"


class TestFmtRub:
    def test_truncates_kopecks(self):
        assert _fmt_rub(Decimal("1561248.39")) == "1 561 248"

    def test_truncates_not_rounds(self):
        assert _fmt_rub(Decimal("1999999.99")) == "1 999 999"

    def test_whole_number(self):
        assert _fmt_rub(Decimal("230000")) == "230 000"


class TestFormatCalculation:
    def test_contains_key_sections(self):
        calc = {
            "car_name": "Test Car",
            "price_cny": Decimal("100000"),
            "vtb_rate": Decimal("11.87"),
            "eur_cbr": Decimal("100"),
            "cny_cbr": Decimal("12"),
            "engine_cc": 1500,
            "hp": Decimal("150"),
            "year": 2024,
            "engine_type": "ДВС",
            "age_category": "0-3",
            "invoice_rub": Decimal("1187000"),
            "bank_commission": Decimal("23740"),
            "invoice_eur": Decimal("11870"),
            "duty_eur": Decimal("6409.80"),
            "duty_method": "max(54%)",
            "duty_rub": Decimal("640980"),
            "processing_fee": Decimal("4924"),
            "processing_info": "test",
            "util_fee": Decimal("3400"),
            "util_info": "test",
            "customs_total": Decimal("649304"),
            "logistics": Decimal("230000"),
            "broker": Decimal("97000"),
            "commission": Decimal("100000"),
            "grand_total": Decimal("2287044"),
            "mileage_km": 45000,
        }
        text = format_calculation(calc, "25.04.2026")
        assert "РАСЧЁТ СТОИМОСТИ" in text
        assert "АВТОМОБИЛЬ" in text
        assert "ТАМОЖНЯ" in text
        assert "ПРОЧЕЕ" in text
        assert "ПОД КЛЮЧ" in text
        assert "предварительный" in text
        assert "2 287 044" in text  # grand total without kopecks
        assert "45 000" in text  # mileage


class TestFormatTelegramPost:
    def test_contains_required_elements(self):
        calc = {
            "price_cny": Decimal("100000"),
            "vtb_rate": Decimal("11.87"),
            "engine_cc": 1500,
            "hp": Decimal("150"),
            "year": 2024,
            "engine_type": "ДВС",
            "grand_total": Decimal("2287044.55"),
            "mileage_km": 45000,
        }
        post = format_telegram_post(calc, "Chery Tiggo 8 Pro")
        assert "Chery Tiggo 8 Pro" in post
        assert "БЕСПЛАТНЫЙ РАСЧЁТ ЦЕНЫ" in post
        assert "@vivat116" in post
        assert "+79612475867" in post
        assert "zakazRUSTEAMBOT" in post
        assert "под ключ в Казань" in post
        assert "wa.me/79612475867" in post
        assert "2 287 044 ₽" in post  # no kopecks
