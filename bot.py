"""Telegram bot for customs duty calculation on cars imported from China."""

import logging
import os
from datetime import datetime
from decimal import Decimal, InvalidOperation

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

from calculator import calculate
from cbr_rates import fetch_cbr_rates
from formatter import format_calculation, format_telegram_post
from parser import parse_car_message, CarInfo

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# Conversation states
WAITING_HP = 1
WAITING_MILEAGE = 2
WAITING_VTB_RATE = 3
CONFIRM_DATA = 4


async def start(update: Update, context) -> None:
    await update.message.reply_text(
        "👋 Привет! Я бот-калькулятор растаможки авто из Китая.\n\n"
        "Пришлите мне информацию об автомобиле (можно переслать сообщение "
        "из канала поставщика), и я рассчитаю полную стоимость под ключ в Казань.\n\n"
        "Мне потребуется:\n"
        "• Информация об авто (марка, модель, год, объём двигателя, цена в юанях)\n"
        "• Мощность в л.с. (если нет в сообщении — спрошу)\n"
        "• Курс покупки юаня ВТБ\n\n"
        "Курс ЦБ РФ я получу автоматически."
    )


async def handle_car_message(update: Update, context) -> int:
    """Process incoming car info message and start conversation."""
    text = update.message.text
    if not text:
        await update.message.reply_text("Пожалуйста, пришлите текстовое сообщение с информацией об автомобиле.")
        return ConversationHandler.END

    car = parse_car_message(text)
    context.user_data["car"] = car
    context.user_data["raw_text"] = text

    # Show what was parsed
    month_names = {
        1: "январь", 2: "февраль", 3: "март", 4: "апрель",
        5: "май", 6: "июнь", 7: "июль", 8: "август",
        9: "сентябрь", 10: "октябрь", 11: "ноябрь", 12: "декабрь",
    }
    year_display = "не найден"
    if car.year:
        if car.month:
            year_display = f"{month_names.get(car.month, '')} {car.year}"
        else:
            year_display = str(car.year)

    parsed_info = (
        f"📋 Распознано:\n"
        f"• Автомобиль: {car.display_name}\n"
        f"• Год: {year_display}\n"
        f"• Объём: {car.engine_cc if car.engine_cc else 'не найден'} см³\n"
        f"• Мощность: {car.hp if car.hp > 0 else 'не найдена'} л.с.\n"
        f"• Пробег: {str(car.mileage_km) + ' км' if car.has_mileage else 'не найден'}\n"
        f"• Тип двигателя: {car.engine_type}\n"
        f"• Цена: {car.price_cny if car.price_cny > 0 else 'не найдена'} CNY\n"
    )

    missing = []
    if car.year == 0:
        missing.append("год выпуска")
    if car.engine_cc == 0:
        missing.append("объём двигателя (см³)")
    if car.price_cny == 0:
        missing.append("цена в юанях (CNY)")

    if missing:
        await update.message.reply_text(
            parsed_info + "\n"
            f"❌ Не удалось определить: {', '.join(missing)}.\n"
            "Пожалуйста, пришлите сообщение с полной информацией об авто."
        )
        return ConversationHandler.END

    if not car.has_hp:
        await update.message.reply_text(
            parsed_info + "\n"
            "❓ Не найдена мощность двигателя.\n"
            "Укажите мощность в лошадиных силах (например: 150):"
        )
        return WAITING_HP

    if not car.has_mileage:
        await update.message.reply_text(
            parsed_info + "\n"
            "❓ Не найден пробег автомобиля.\n"
            "Укажите пробег в км (например: 45000):"
        )
        return WAITING_MILEAGE

    await update.message.reply_text(
        parsed_info + "\n"
        "❓ Укажите курс покупки юаня ВТБ (например: 11.87):"
    )
    return WAITING_VTB_RATE


async def handle_hp_input(update: Update, context) -> int:
    """Receive horsepower from user."""
    text = update.message.text.strip().replace(",", ".")
    # Extract just the number
    import re
    m = re.search(r'(\d+(?:\.\d+)?)', text)
    if not m:
        await update.message.reply_text("❌ Не могу распознать число. Укажите мощность в л.с. (например: 150):")
        return WAITING_HP

    try:
        hp = Decimal(m.group(1))
    except InvalidOperation:
        await update.message.reply_text("❌ Не могу распознать число. Укажите мощность в л.с. (например: 150):")
        return WAITING_HP

    if hp <= 0 or hp > 2000:
        await update.message.reply_text("❌ Мощность должна быть от 1 до 2000 л.с. Попробуйте ещё раз:")
        return WAITING_HP

    car: CarInfo = context.user_data["car"]
    car.hp = hp
    context.user_data["car"] = car

    if not car.has_mileage:
        await update.message.reply_text(
            f"✅ Мощность: {hp} л.с.\n\n"
            "❓ Укажите пробег автомобиля в км (например: 45000):"
        )
        return WAITING_MILEAGE

    await update.message.reply_text(
        f"✅ Мощность: {hp} л.с.\n\n"
        "❓ Укажите курс покупки юаня ВТБ (например: 11.87):"
    )
    return WAITING_VTB_RATE


async def handle_mileage_input(update: Update, context) -> int:
    """Receive mileage from user."""
    text = update.message.text.strip().replace(" ", "").replace("\u00a0", "")
    import re
    m = re.search(r'(\d+)', text)
    if not m:
        await update.message.reply_text("❌ Не могу распознать число. Укажите пробег в км (например: 45000):")
        return WAITING_MILEAGE

    try:
        mileage = int(m.group(1))
    except ValueError:
        await update.message.reply_text("❌ Не могу распознать число. Укажите пробег в км (например: 45000):")
        return WAITING_MILEAGE

    if mileage < 0:
        await update.message.reply_text("❌ Пробег не может быть отрицательным. Попробуйте ещё раз:")
        return WAITING_MILEAGE

    car: CarInfo = context.user_data["car"]
    car.mileage_km = mileage
    context.user_data["car"] = car

    await update.message.reply_text(
        f"✅ Пробег: {mileage} км\n\n"
        "❓ Укажите курс покупки юаня ВТБ (например: 11.87):"
    )
    return WAITING_VTB_RATE


async def handle_vtb_rate_input(update: Update, context) -> int:
    """Receive VTB exchange rate and perform calculation."""
    text = update.message.text.strip().replace(",", ".")
    import re
    m = re.search(r'(\d+(?:\.\d+)?)', text)
    if not m:
        await update.message.reply_text("❌ Не могу распознать курс. Укажите курс ВТБ (например: 11.87):")
        return WAITING_VTB_RATE

    try:
        vtb_rate = Decimal(m.group(1))
    except InvalidOperation:
        await update.message.reply_text("❌ Не могу распознать курс. Укажите курс ВТБ (например: 11.87):")
        return WAITING_VTB_RATE

    if vtb_rate <= 0 or vtb_rate > 100:
        await update.message.reply_text("❌ Курс должен быть от 0.01 до 100. Попробуйте ещё раз:")
        return WAITING_VTB_RATE

    await update.message.reply_text("⏳ Получаю курсы ЦБ РФ и считаю...")

    try:
        cbr = fetch_cbr_rates()
    except Exception as e:
        logger.error(f"CBR fetch error: {e}")
        await update.message.reply_text(
            "❌ Не удалось получить курсы ЦБ РФ. Попробуйте позже."
        )
        return ConversationHandler.END

    car: CarInfo = context.user_data["car"]

    now = datetime.now()
    try:
        result = calculate(
            price_cny=car.price_cny,
            vtb_rate=vtb_rate,
            eur_cbr=cbr["EUR"],
            cny_cbr=cbr["CNY"],
            engine_cc=car.engine_cc,
            hp=car.hp,
            year=car.year,
            engine_type=car.engine_type,
            current_year=now.year,
            month=car.month,
            current_month=now.month,
        )
    except Exception as e:
        logger.error(f"Calculation error: {e}")
        await update.message.reply_text(f"❌ Ошибка расчёта: {e}")
        return ConversationHandler.END

    result["car_name"] = car.display_name
    result["mileage_km"] = car.mileage_km
    result["brand"] = car.brand

    # Send calculation breakdown
    calc_text = format_calculation(result, cbr["date"])
    await update.message.reply_text(
        calc_text,
        parse_mode=ParseMode.HTML,
    )

    # Send header as separate message
    await update.message.reply_text(
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "📝  <b>ГОТОВЫЙ ПОСТ ДЛЯ TELEGRAM</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "👇 Скопируйте следующее сообщение целиком:",
        parse_mode=ParseMode.HTML,
    )

    # Send ready post as a clean separate message for easy copy
    post_text = format_telegram_post(result, car.display_name)
    await update.message.reply_text(
        post_text,
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True,
    )

    return ConversationHandler.END


async def cancel(update: Update, context) -> int:
    await update.message.reply_text("Расчёт отменён. Пришлите новую информацию об авто для нового расчёта.")
    return ConversationHandler.END


def main() -> None:
    # Start health-check HTTP server immediately for Render free-tier
    from health import start_health_server
    start_health_server(port=int(os.environ.get("PORT", 10000)))

    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN environment variable is not set")

    app = Application.builder().token(token).build()

    conv_handler = ConversationHandler(
        entry_points=[
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_car_message),
        ],
        states={
            WAITING_HP: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_hp_input),
            ],
            WAITING_MILEAGE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_mileage_input),
            ],
            WAITING_VTB_RATE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_vtb_rate_input),
            ],
        },
        fallbacks=[
            CommandHandler("cancel", cancel),
            CommandHandler("start", start),
        ],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv_handler)

    logger.info("Bot started")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
