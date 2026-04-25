"""Parse car information from supplier channel messages."""

import re
from decimal import Decimal, InvalidOperation
from dataclasses import dataclass, field


@dataclass
class CarInfo:
    brand: str = ""
    model: str = ""
    trim: str = ""
    year: int = 0
    engine_cc: int = 0
    hp: Decimal = Decimal("0")
    engine_type: str = "ДВС"
    price_cny: Decimal = Decimal("0")
    raw_text: str = ""

    @property
    def has_hp(self) -> bool:
        return self.hp > 0

    @property
    def is_complete_for_calc(self) -> bool:
        return (
            self.year > 0
            and self.engine_cc > 0
            and self.price_cny > 0
            and self.hp > 0
        )

    @property
    def display_name(self) -> str:
        parts = [p for p in [self.brand, self.model, self.trim] if p]
        return " ".join(parts) if parts else "Автомобиль"


def _extract_year(text: str) -> int:
    patterns = [
        r'(\d{4})\s*(?:г\.?(?:од)?|year)',
        r'(?:год|year|выпуск)[:\s]*(\d{4})',
        r'\b(20[1-2]\d)\b',
    ]
    for pat in patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            y = int(m.group(1))
            if 2000 <= y <= 2027:
                return y
    return 0


def _extract_engine_cc(text: str) -> int:
    patterns = [
        r'(\d[\d\s]*)\s*(?:см[³3]|cc|куб)',
        r'(?:объ[её]м|volume|двигатель)[:\s]*(\d[\d\s.,]*)\s*(?:л|l)\b',
        r'(\d\.\d)\s*(?:л|l|t)\b',
        r'(\d\.\d)T?\b',
    ]
    for pat in patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            raw = m.group(1).replace(" ", "").replace(",", ".")
            try:
                val = float(raw)
            except ValueError:
                continue
            if val < 100:
                return int(val * 1000)
            return int(val)
    return 0


def _extract_hp(text: str) -> Decimal:
    patterns = [
        r'(\d+)\s*(?:л\.?\s*с\.?|hp|лошад|л/с|лс)',
        r'(?:мощность|power)[:\s]*(\d+)',
    ]
    for pat in patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            try:
                return Decimal(m.group(1))
            except InvalidOperation:
                continue
    return Decimal("0")


def _extract_price_cny(text: str) -> Decimal:
    patterns = [
        r'(\d[\d\s]*)\s*(?:юан|cny|¥|元|yuan)',
        r'(?:цена|price|стоимость)[:\s]*([\d\s]+)\s*(?:юан|cny|¥|元)',
        r'(?:цена|price|стоимость)[:\s]*([\d\s.,]+)',
        r'¥\s*([\d\s.,]+)',
    ]
    for pat in patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            raw = m.group(1).replace(" ", "").replace(",", "")
            try:
                val = Decimal(raw)
                if val > 1000:
                    return val
            except InvalidOperation:
                continue
    return Decimal("0")


def _extract_engine_type(text: str) -> str:
    text_lower = text.lower()
    if any(w in text_lower for w in ["электро", "ev", "electric", "bev"]):
        return "EV"
    if any(w in text_lower for w in ["гибрид", "hybrid", "phev", "hev"]):
        return "ГИБРИД"
    if any(w in text_lower for w in ["дизель", "diesel"]):
        return "ДИЗЕЛЬ"
    return "ДВС"


def _extract_brand_model(text: str) -> tuple[str, str, str]:
    known_brands = [
        "Chery", "Haval", "Geely", "BYD", "Changan", "Exeed", "Omoda",
        "Jetour", "Tank", "Hongqi", "JAC", "FAW", "Dongfeng", "GWM",
        "Great Wall", "BAIC", "Zeekr", "NIO", "XPeng", "Li Auto",
        "Lixiang", "Voyah", "Avatr", "Deepal", "Leapmotor", "Wuling",
        "MG", "Lynk", "Lynk & Co", "GAC", "Trumpchi", "Kaiyi",
        "SWM", "Forthing", "AITO", "Denza", "iCAR",
    ]
    known_models: dict[str, list[str]] = {
        "Chery": ["Tiggo 4", "Tiggo 4 Pro", "Tiggo 7", "Tiggo 7 Pro", "Tiggo 7 Pro Max",
                   "Tiggo 8", "Tiggo 8 Pro", "Tiggo 8 Pro Max", "Tiggo 8 Plus",
                   "Tiggo 9", "Arrizo 5", "Arrizo 8"],
        "Haval": ["Jolion", "F7", "F7x", "H5", "H6", "H9", "Dargo", "M6"],
        "Geely": ["Atlas", "Atlas Pro", "Monjaro", "Coolray", "Tugella", "Emgrand",
                   "Preface", "Boyue", "Xingyue", "Xingyue L"],
        "Exeed": ["TXL", "VX", "LX", "RX"],
        "Omoda": ["C5", "S5", "C7", "E5"],
        "Jetour": ["Dashing", "X70", "X70 Plus", "X90", "T2"],
        "Tank": ["300", "500", "700"],
        "BYD": ["Song Plus", "Song Pro", "Yuan Plus", "Han", "Tang", "Seal",
                "Dolphin", "Atto 3", "Destroyer 05"],
        "Changan": ["CS35 Plus", "CS55 Plus", "CS75 Plus", "Uni-K", "Uni-V", "Uni-T",
                    "Eado Plus"],
    }

    brand = ""
    model = ""
    trim = ""

    for b in known_brands:
        if re.search(r'\b' + re.escape(b) + r'\b', text, re.IGNORECASE):
            brand = b
            if b in known_models:
                for mdl in sorted(known_models[b], key=len, reverse=True):
                    if re.search(re.escape(mdl), text, re.IGNORECASE):
                        model = mdl
                        break
            if not model:
                pattern = r'\b' + re.escape(b) + r'\s+(\S+(?:\s+\S+){0,3})'
                m = re.search(pattern, text, re.IGNORECASE)
                if m:
                    model = m.group(1).strip().rstrip(".,;!?")
            break

    first_line = text.strip().split("\n")[0].strip()
    if not brand and len(first_line) < 100:
        parts = first_line.split()
        if len(parts) >= 2:
            brand = parts[0]
            model = " ".join(parts[1:4])

    return brand, model, trim


def parse_car_message(text: str) -> CarInfo:
    """Parse a forwarded supplier message and extract car information."""
    brand, model, trim = _extract_brand_model(text)
    return CarInfo(
        brand=brand,
        model=model,
        trim=trim,
        year=_extract_year(text),
        engine_cc=_extract_engine_cc(text),
        hp=_extract_hp(text),
        engine_type=_extract_engine_type(text),
        price_cny=_extract_price_cny(text),
        raw_text=text,
    )
