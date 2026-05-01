# 🚗 Telegram Customs Calculator Bot

Telegram-бот для расчёта стоимости растаможки автомобилей из Китая с доставкой в Россию.

## Возможности

- **Парсинг объявлений** — распознаёт марку, год, объём двигателя, мощность, пробег, тип двигателя и цену из пересланных сообщений
- **Курсы ЦБ РФ** — автоматически загружает актуальные курсы EUR и CNY
- **Расчёт стоимости** — инвойс, комиссия банка, таможенная пошлина, оформление, утильсбор, логистика, брокер
- **Готовый пост** — генерирует отформатированный пост для Telegram-канала

## Структура проекта

```
├── bot.py            # Telegram-бот (хендлеры, conversation flow)
├── parser.py         # Парсинг объявлений (марка, объём, тип двигателя и т.д.)
├── calculator.py     # Расчёт таможенных пошлин и стоимости
├── formatter.py      # Форматирование результатов и постов
├── cbr_rates.py      # Получение курсов ЦБ РФ
├── health.py         # HTTP health-check сервер (для Render)
├── requirements.txt  # Зависимости Python
├── Dockerfile        # Docker-образ для деплоя
├── Procfile          # Конфиг запуска (Railway/Heroku)
├── runtime.txt       # Версия Python
└── tests/            # Тесты
    ├── test_parser.py
    ├── test_calculator.py
    ├── test_formatter.py
    └── test_cbr.py
```

## Локальный запуск

```bash
pip install -r requirements.txt
export TELEGRAM_BOT_TOKEN="your-token-here"
python bot.py
```

## Docker

```bash
docker build -t customs-bot .
docker run -e TELEGRAM_BOT_TOKEN="your-token" customs-bot
```

## Тесты

```bash
pytest tests/ -v
```

## Деплой (Render.com)

Бот задеплоен как Web Service на Render с автодеплоем.

**Переменные окружения:**
- `TELEGRAM_BOT_TOKEN` — токен бота от @BotFather
- `PORT` — порт для health-check (по умолчанию 10000, выставляется Render автоматически)

## Правила расчёта

Актуальные правила расчёта таможни на 2026 год — см. `calculator.py`.
