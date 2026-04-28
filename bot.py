"""Telegram bot for customs duty calculation on cars imported from China."""

import logging
import os
import time
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

WAITING_HP = 1
WAITING_MILEAGE = 2
WAITING_VTB_RATE = 3


async def start(update: Update, context) -> None:
    if not update.message:
        return

    await update.message.reply_text(
        "👋 Привет! Я бот-калькулятор растаможки авто из Китая.\n\n"
        "Пришлите информацию об автомобиле."
    )


async def handle_car_message(update: Update, context) -> int:
    if not update.message or not update.message.text:
        return ConversationHandler.END

    text = update.message.text

    car = parse_car_message(text)
    context.user_data["car"] = car

    if car.year == 0 or car.engine_cc == 0 or car.price_cny == 0:
        await update.message.reply_text("❌ Не хватает данных об авто")
        return ConversationHandler.END

    if not car.has_hp:
        await update.message.reply_text("Введите мощность (л.с.):")
        return WAITING_HP

    if not car.has_mileage:
        await update.message.reply_text("Введите пробег (км):")
        return WAITING_MILEAGE

    await update.message.reply_text("Введите курс ВТБ:")
    return WAITING_VTB_RATE


async def handle_hp_input(update: Update, context) -> int:
    if not update.message:
        return ConversationHandler.END

    text = update.message.text
    import re
    m = re.search(r'(\d+)', text)
    if not m:
        return WAITING_HP

    car: CarInfo = context.user_data["car"]
    car.hp = Decimal(m.group(1))
    context.user_data["car"] = car

    await update.message.reply_text("Введите пробег:")
    return WAITING_MILEAGE


async def handle_mileage_input(update: Update, context) -> int:
    if not update.message:
        return ConversationHandler.END

    text = update.message.text
    import re
    m = re.search(r'(\d+)', text)
    if not m:
        return WAITING_MILEAGE

    car: CarInfo = context.user_data["car"]
    car.mileage_km = int(m.group(1))
    context.user_data["car"] = car

    await update.message.reply_text("Введите курс ВТБ:")
    return WAITING_VTB_RATE


async def handle_vtb_rate_input(update: Update, context) -> int:
    if not update.message:
        return ConversationHandler.END

    text = update.message.text
    import re
    m = re.search(r'(\d+(?:\.\d+)?)', text)
    if not m:
        return WAITING_VTB_RATE

    vtb_rate = Decimal(m.group(1))

    try:
        cbr = fetch_cbr_rates()
    except Exception as e:
        logger.error(e)
        return ConversationHandler.END

    car: CarInfo = context.user_data["car"]

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
        )
    except Exception as e:
        logger.error(e)
        return ConversationHandler.END

    text = format_calculation(result, cbr["date"])
    await update.message.reply_text(text, parse_mode=ParseMode.HTML)

    return ConversationHandler.END


def main():
    while True:
        try:
            token = os.environ.get("TELEGRAM_BOT_TOKEN")
            if not token:
                raise RuntimeError("TOKEN NOT SET")

            app = Application.builder().token(token).build()

            conv_handler = ConversationHandler(
                entry_points=[MessageHandler(filters.TEXT, handle_car_message)],
                states={
                    WAITING_HP: [MessageHandler(filters.TEXT, handle_hp_input)],
                    WAITING_MILEAGE: [MessageHandler(filters.TEXT, handle_mileage_input)],
                    WAITING_VTB_RATE: [MessageHandler(filters.TEXT, handle_vtb_rate_input)],
                },
                fallbacks=[],
            )

            app.add_handler(CommandHandler("start", start))
            app.add_handler(conv_handler)

            logger.info("Bot started")
            app.run_polling()

        except Exception as e:
            logger.error(f"CRASH: {e}")
            time.sleep(5)


if __name__ == "__main__":
    main()
