import { NextResponse } from "next/server";

export async function POST(request: Request) {
  try {
    const { name, phone } = await request.json();

    if (!name || !phone) {
      return NextResponse.json(
        { error: "Имя и телефон обязательны" },
        { status: 400 }
      );
    }

    const botToken = process.env.TELEGRAM_BOT_TOKEN;
    const chatId = process.env.TELEGRAM_CHAT_ID;

    if (botToken && chatId) {
      const text = `🚗 Новая заявка с сайта!\n\n👤 Имя: ${name}\n📱 Телефон: ${phone}\n\n📅 ${new Date().toLocaleString("ru-RU", { timeZone: "Europe/Moscow" })}`;

      await fetch(
        `https://api.telegram.org/bot${botToken}/sendMessage`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            chat_id: chatId,
            text,
            parse_mode: "HTML",
          }),
        }
      );
    }

    return NextResponse.json({ success: true });
  } catch {
    return NextResponse.json(
      { error: "Ошибка сервера" },
      { status: 500 }
    );
  }
}
