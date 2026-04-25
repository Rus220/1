"""Tests for customs calculator — covering all age categories, duty brackets, and edge cases."""

from decimal import Decimal
import pytest

from calculator import (
    calculate,
    _get_car_age_category,
    _calc_duty_0_3,
    _calc_duty_by_volume,
    _get_customs_processing,
    _get_util_fee,
    DUTY_3_5,
    DUTY_5_PLUS,
)


# ---------------------------------------------------------------------------
# Age category
# ---------------------------------------------------------------------------

class TestAgeCategory:
    def test_new_car(self):
        assert _get_car_age_category(2026, 2026) == "0-3"

    def test_1_year(self):
        assert _get_car_age_category(2025, 2026) == "0-3"

    def test_3_years(self):
        assert _get_car_age_category(2023, 2026) == "0-3"

    def test_4_years(self):
        assert _get_car_age_category(2022, 2026) == "3-5"

    def test_5_years(self):
        assert _get_car_age_category(2021, 2026) == "3-5"

    def test_6_years(self):
        assert _get_car_age_category(2020, 2026) == "5-7"

    def test_7_years(self):
        assert _get_car_age_category(2019, 2026) == "5-7"

    def test_8_years(self):
        assert _get_car_age_category(2018, 2026) == "7+"

    def test_future_car(self):
        assert _get_car_age_category(2027, 2026) == "0-3"


# ---------------------------------------------------------------------------
# Duty 0-3 years
# ---------------------------------------------------------------------------

class TestDuty0_3:
    def test_bracket_under_8500(self):
        duty, _ = _calc_duty_0_3(Decimal("8000"), 1500)
        by_pct = Decimal("8000") * Decimal("0.54")
        by_vol = Decimal("1500") * Decimal("2.5")
        assert duty == max(by_pct, by_vol)

    def test_bracket_8501_16700(self):
        duty, _ = _calc_duty_0_3(Decimal("10000"), 1500)
        by_pct = Decimal("10000") * Decimal("0.48")
        by_vol = Decimal("1500") * Decimal("3.5")
        assert duty == max(by_pct, by_vol)

    def test_bracket_16701_42300(self):
        duty, _ = _calc_duty_0_3(Decimal("30000"), 2000)
        by_pct = Decimal("30000") * Decimal("0.48")
        by_vol = Decimal("2000") * Decimal("5.5")
        assert duty == max(by_pct, by_vol)

    def test_bracket_42301_84500(self):
        duty, _ = _calc_duty_0_3(Decimal("50000"), 2000)
        by_pct = Decimal("50000") * Decimal("0.48")
        by_vol = Decimal("2000") * Decimal("7.5")
        assert duty == max(by_pct, by_vol)

    def test_bracket_84501_169000(self):
        duty, _ = _calc_duty_0_3(Decimal("100000"), 3000)
        by_pct = Decimal("100000") * Decimal("0.48")
        by_vol = Decimal("3000") * Decimal("15")
        assert duty == max(by_pct, by_vol)

    def test_bracket_over_169000(self):
        duty, _ = _calc_duty_0_3(Decimal("200000"), 4000)
        by_pct = Decimal("200000") * Decimal("0.48")
        by_vol = Decimal("4000") * Decimal("20")
        assert duty == max(by_pct, by_vol)


# ---------------------------------------------------------------------------
# Duty 3-5 and 5+ years
# ---------------------------------------------------------------------------

class TestDutyByVolume:
    def test_3_5_1500cc(self):
        duty, _ = _calc_duty_by_volume(1500, DUTY_3_5)
        assert duty == Decimal("1500") * Decimal("1.7")

    def test_3_5_2000cc(self):
        duty, _ = _calc_duty_by_volume(2000, DUTY_3_5)
        assert duty == Decimal("2000") * Decimal("2.7")

    def test_5plus_1500cc(self):
        duty, _ = _calc_duty_by_volume(1500, DUTY_5_PLUS)
        assert duty == Decimal("1500") * Decimal("3.2")

    def test_5plus_3000cc(self):
        duty, _ = _calc_duty_by_volume(3000, DUTY_5_PLUS)
        assert duty == Decimal("3000") * Decimal("5.0")

    def test_5plus_large(self):
        duty, _ = _calc_duty_by_volume(5000, DUTY_5_PLUS)
        assert duty == Decimal("5000") * Decimal("5.7")


# ---------------------------------------------------------------------------
# Customs processing
# ---------------------------------------------------------------------------

class TestCustomsProcessing:
    def test_under_200k(self):
        fee, _ = _get_customs_processing(Decimal("150000"))
        assert fee == Decimal("1231")

    def test_200k_450k(self):
        fee, _ = _get_customs_processing(Decimal("300000"))
        assert fee == Decimal("2462")

    def test_450k_1200k(self):
        fee, _ = _get_customs_processing(Decimal("800000"))
        assert fee == Decimal("4924")

    def test_1200k_2700k(self):
        fee, _ = _get_customs_processing(Decimal("2000000"))
        assert fee == Decimal("13541")

    def test_2700k_4200k(self):
        fee, _ = _get_customs_processing(Decimal("3000000"))
        assert fee == Decimal("18465")

    def test_4200k_5500k(self):
        fee, _ = _get_customs_processing(Decimal("5000000"))
        assert fee == Decimal("21344")

    def test_5500k_10000k(self):
        fee, _ = _get_customs_processing(Decimal("8000000"))
        assert fee == Decimal("49240")

    def test_over_10000k(self):
        fee, _ = _get_customs_processing(Decimal("15000000"))
        assert fee == Decimal("73860")


# ---------------------------------------------------------------------------
# Recycling fee (utilisation)
# ---------------------------------------------------------------------------

class TestUtilFee:
    def test_benefit_new(self):
        fee, info = _get_util_fee(2024, Decimal("150"), 1500, "ДВС", 2026)
        assert fee == Decimal("3400")
        assert "льгота" in info

    def test_benefit_old(self):
        fee, info = _get_util_fee(2020, Decimal("120"), 2000, "БЕНЗИН", 2026)
        assert fee == Decimal("5200")
        assert "льгота" in info

    def test_no_benefit_high_hp(self):
        fee, _ = _get_util_fee(2024, Decimal("200"), 1500, "ДВС", 2026)
        assert fee > Decimal("5200")

    def test_no_benefit_large_engine(self):
        fee, _ = _get_util_fee(2024, Decimal("150"), 3000, "ДВС", 2026)
        assert fee > Decimal("5200")

    def test_no_benefit_ev(self):
        fee, _ = _get_util_fee(2024, Decimal("100"), 0, "EV", 2026)
        assert fee > Decimal("5200")

    def test_full_rate_new_small(self):
        fee, _ = _get_util_fee(2024, Decimal("200"), 1000, "ДВС", 2026)
        assert fee == Decimal("306000")

    def test_full_rate_old_small(self):
        fee, _ = _get_util_fee(2018, Decimal("200"), 1000, "ДВС", 2026)
        assert fee == Decimal("405900")


# ---------------------------------------------------------------------------
# Full calculation integration test
# ---------------------------------------------------------------------------

class TestFullCalculation:
    def test_new_car_chery_tiggo8(self):
        """Chery Tiggo 8 Pro, 2024, 1.6T (1598cc), 186 hp, 135000 CNY."""
        result = calculate(
            price_cny=Decimal("135000"),
            vtb_rate=Decimal("11.87"),
            eur_cbr=Decimal("100.50"),
            cny_cbr=Decimal("12.35"),
            engine_cc=1598,
            hp=Decimal("186"),
            year=2024,
            engine_type="ДВС",
            current_year=2026,
        )

        assert result["age_category"] == "0-3"
        assert result["invoice_rub"] == Decimal("135000") * Decimal("11.87")
        assert result["bank_commission"] == result["invoice_rub"] * Decimal("0.02")
        assert result["invoice_eur"] == result["invoice_rub"] / Decimal("100.50")

        # Verify duty is max of percent and volume
        inv_eur = result["invoice_eur"]
        assert result["duty_eur"] > 0
        assert result["duty_rub"] == result["duty_eur"] * Decimal("100.50")

        # Grand total = invoice + commission + customs_total + logistics + broker + commission_fee
        expected_total = (
            result["invoice_rub"]
            + result["bank_commission"]
            + result["customs_total"]
            + Decimal("230000")
            + Decimal("97000")
            + Decimal("100000")
        )
        assert result["grand_total"] == expected_total

    def test_3_5_year_car(self):
        """Car from 2022, age = 4 years → 3-5 category."""
        result = calculate(
            price_cny=Decimal("100000"),
            vtb_rate=Decimal("12.00"),
            eur_cbr=Decimal("95.00"),
            cny_cbr=Decimal("12.00"),
            engine_cc=1500,
            hp=Decimal("150"),
            year=2022,
            engine_type="ДВС",
            current_year=2026,
        )
        assert result["age_category"] == "3-5"
        expected_duty = Decimal("1500") * Decimal("1.7")
        assert result["duty_eur"] == expected_duty

    def test_old_car_7plus(self):
        """Car from 2015, age > 7 → 7+ category, uses 5plus table."""
        result = calculate(
            price_cny=Decimal("50000"),
            vtb_rate=Decimal("11.50"),
            eur_cbr=Decimal("98.00"),
            cny_cbr=Decimal("12.00"),
            engine_cc=2000,
            hp=Decimal("140"),
            year=2015,
            engine_type="ДВС",
            current_year=2026,
        )
        assert result["age_category"] == "7+"
        expected_duty = Decimal("2000") * Decimal("4.8")
        assert result["duty_eur"] == expected_duty

    def test_no_rounding(self):
        """Ensure intermediate values are not rounded."""
        result = calculate(
            price_cny=Decimal("123456"),
            vtb_rate=Decimal("11.87"),
            eur_cbr=Decimal("100.50"),
            cny_cbr=Decimal("12.35"),
            engine_cc=1498,
            hp=Decimal("147"),
            year=2025,
            engine_type="ДВС",
            current_year=2026,
        )
        # invoice_rub should be exact multiplication
        assert result["invoice_rub"] == Decimal("123456") * Decimal("11.87")
        # bank commission exact
        assert result["bank_commission"] == result["invoice_rub"] * Decimal("0.02")
