"""Tests for CBR rate fetching."""

import pytest
from decimal import Decimal

from cbr_rates import fetch_cbr_rates


class TestCBR:
    def test_fetch_rates_live(self):
        """Integration test: fetch real CBR rates."""
        rates = fetch_cbr_rates()
        assert "EUR" in rates
        assert "CNY" in rates
        assert "date" in rates
        assert isinstance(rates["EUR"], Decimal)
        assert isinstance(rates["CNY"], Decimal)
        assert rates["EUR"] > Decimal("50")
        assert rates["EUR"] < Decimal("200")
        assert rates["CNY"] > Decimal("5")
        assert rates["CNY"] < Decimal("30")
