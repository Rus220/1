"""Tests for car message parser."""

from decimal import Decimal

from parser import parse_car_message


class TestParser:
    def test_full_message(self):
        msg = """Chery Tiggo 8 Pro Max
2024 год
Объём 1.6T (1598 см³)
186 л.с.
Бензин
Цена: 135 000 юаней"""
        car = parse_car_message(msg)
        assert car.brand == "Chery"
        assert "Tiggo 8 Pro" in car.model or "Tiggo 8 Pro Max" in car.model
        assert car.year == 2024
        assert car.engine_cc == 1598
        assert car.hp == Decimal("186")
        assert car.price_cny == Decimal("135000")

    def test_haval_message(self):
        msg = """Haval Jolion 2025
1.5T 150 л.с.
98000 юаней"""
        car = parse_car_message(msg)
        assert car.brand == "Haval"
        assert car.year == 2025
        assert car.hp == Decimal("150")
        assert car.price_cny == Decimal("98000")

    def test_no_hp(self):
        msg = """Geely Monjaro 2024
2.0T 2000cc
Цена 180000 CNY"""
        car = parse_car_message(msg)
        assert car.brand == "Geely"
        assert car.year == 2024
        assert car.engine_cc == 2000
        assert car.hp == Decimal("0")
        assert not car.has_hp

    def test_price_with_spaces(self):
        msg = """Changan CS75 Plus 2024
1.5T 1500 см³ 181 л.с.
Стоимость 125 000 юаней"""
        car = parse_car_message(msg)
        assert car.price_cny == Decimal("125000")

    def test_ev_detection(self):
        msg = """BYD Seal 2024 электро
Цена 200000 юаней"""
        car = parse_car_message(msg)
        assert car.engine_type == "EV"

    def test_display_name(self):
        msg = """Chery Tiggo 7 Pro 2024
1.5T 147 л.с. 1498 см³
110000 юаней"""
        car = parse_car_message(msg)
        assert "Chery" in car.display_name

    def test_is_complete_for_calc(self):
        msg = """Haval H6 2024
2.0T 2000cc 200 л.с.
145000 юаней"""
        car = parse_car_message(msg)
        assert car.year > 0
        assert car.engine_cc > 0
        assert car.hp > 0
        assert car.price_cny > 0
        assert car.is_complete_for_calc
