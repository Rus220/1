"""Fetch current exchange rates from the Central Bank of Russia (CBR)."""

from datetime import datetime
from decimal import Decimal
from xml.etree import ElementTree

import requests


CBR_DAILY_URL = "https://www.cbr.ru/scripts/XML_daily.asp"


def fetch_cbr_rates() -> dict:
    """Return {'EUR': Decimal, 'CNY': Decimal, 'date': str} from CBR daily XML feed."""
    resp = requests.get(CBR_DAILY_URL, timeout=15)
    resp.raise_for_status()
    resp.encoding = "windows-1251"

    root = ElementTree.fromstring(resp.text)
    date_str = root.attrib.get("Date", datetime.now().strftime("%d.%m.%Y"))

    rates: dict = {"date": date_str}
    needed = {"EUR": "R01239", "CNY": "R01375"}

    for valute in root.findall("Valute"):
        v_id = valute.attrib.get("ID", "")
        for currency, code in needed.items():
            if v_id == code:
                nominal = int(valute.findtext("Nominal", "1"))
                value_str = valute.findtext("Value", "0").replace(",", ".")
                rates[currency] = Decimal(value_str) / Decimal(nominal)

    if "EUR" not in rates or "CNY" not in rates:
        raise ValueError(f"Could not find EUR/CNY in CBR response. Found: {list(rates.keys())}")

    return rates
