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
    mileage_km: int = 0
    raw_text: str = ""

    @property
    def has_hp(self) -> bool:
        return self.hp > 0

    @property
    def has_mileage(self) -> bool:
        return self.mileage_km > 0

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


def _clean_text(text: str) -> str:
    """Remove emojis and special decorative characters from text."""
    emoji_pattern = re.compile(
        r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF'
        r'\U0001F1E0-\U0001F1FF\U00002700-\U000027BF\U0000FE00-\U0000FE0F'
        r'\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF'
        r'\U00002702-\U000027B0\U000024C2-\U0001F251\U00002600-\U000026FF'
        r'\U0000200D\U0000231A-\U0000231B\U000023E9-\U000023F3\U000023F8-\U000023FA'
        r'\U000025AA-\U000025AB\U000025B6\U000025C0\U000025FB-\U000025FE'
        r'\U00002614-\U00002615\U00002648-\U00002653\U0000267F\U00002934-\U00002935'
        r'\U000023CF\U0000203C\U00002049\U00002122\U00002139\U00002194-\U000021AA'
        r'\U00002328\U000023ED-\U000023EF\U00002934-\U00002935\U000025AA-\U000025FE'
        r'\U00002B05-\U00002B07\U00002B1B-\U00002B1C\U00002B50\U00002B55'
        r'\U00003030\U0000303D\U00003297\U00003299'
        r'\U0000FE0F\U000020E3\U0000200D]+',
        re.UNICODE,
    )
    return emoji_pattern.sub('', text).strip()


def _extract_brand_model(text: str) -> tuple[str, str, str]:
    known_brands = [
        "Chery", "Haval", "Geely", "BYD", "Changan", "Exeed", "Omoda",
        "Jetour", "Tank", "Hongqi", "JAC", "FAW", "Dongfeng", "GWM",
        "Great Wall", "BAIC", "Zeekr", "NIO", "XPeng", "Li Auto",
        "Lixiang", "Voyah", "Avatr", "Deepal", "Leapmotor", "Wuling",
        "MG", "Lynk", "Lynk & Co", "GAC", "Trumpchi", "Kaiyi",
        "SWM", "Forthing", "AITO", "Denza", "iCAR",
        "Volkswagen", "VW", "Audi", "BMW", "Mercedes", "Toyota", "Honda",
        "Hyundai", "Kia", "Nissan", "Mazda", "Lexus", "Porsche",
        "Land Rover", "Volvo", "Skoda", "Ford", "Chevrolet", "Cadillac",
        "Infiniti", "Mitsubishi", "Subaru", "Suzuki", "Peugeot", "Renault",
        "Citroen", "Opel", "Fiat", "Tesla", "Mini", "Jeep", "Dodge",
        "Lincoln", "Buick", "Genesis", "Smart",
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
                # Extract model from same line only, up to 3 words after brand
                for line in text.split("\n"):
                    bm = re.search(r'\b' + re.escape(b) + r'\s+(\S+(?:\s+\S+){0,3})', line, re.IGNORECASE)
                    if bm:
                        model = bm.group(1).strip().rstrip(".,;!?")
                        break
            break

    first_line = _clean_text(text.strip().split("\n")[0].strip())
    if not brand and len(first_line) < 100:
        parts = first_line.split()
        if len(parts) >= 2:
            brand = parts[0]
            model = " ".join(parts[1:4])

    # Clean brand and model from trailing garbage
    brand = re.sub(r'[\-\—\–,;!?:]+$', '', brand).strip()
    model = re.sub(r'[\-\—\–,;!?:]+$', '', model).strip()
    # Remove common trailing phrases (e.g. "— в продаже", "в наличии", etc.)
    model = re.sub(
        r'[\s\-\—\–]*(в\s+продаже|в\s+наличии|на\s+продажу|в\s+наличие|'
        r'на\s+заказ|под\s+заказ|в\s+пути|в\s+stock)\s*$',
        '', model, flags=re.IGNORECASE,
    ).strip()
    # Remove trailing dashes and single stray characters
    model = re.sub(r'[\-\—\–,;!?:]+$', '', model).strip()
    model = re.sub(r'[\s\-\—\–]+[а-яА-Яa-zA-Z]$', '', model).strip()

    return brand, model, trim


def _extract_mileage(text: str) -> int:
    """Extract mileage in km from text."""
    patterns = [
        r'(\d[\d\s]*)\s*(?:км|km|\u043a\u0438\u043b\u043e\u043c\u0435\u0442\u0440)',
        r'(?:\u043f\u0440\u043e\u0431\u0435\u0433|mileage)[:\s]*(\d[\d\s]*)',
    ]
    for pat in patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            try:
                val = int(m.group(1).replace(' ', '').replace('\u00a0', ''))
                if val > 0:
                    return val
            except ValueError:
                continue
    return 0


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
        mileage_km=_extract_mileage(text),
        raw_text=text,
    )
