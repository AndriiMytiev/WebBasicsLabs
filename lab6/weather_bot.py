import requests
import asyncio
import datetime
from aiogram import Bot, types, Dispatcher
from aiogram.filters.command import Command

open_weather_token = "633ade863aee1f1084495796be2c2ad3"
bot_token = "6914854735:AAH3Hb5SSjHJ7hqpNBVavyaICD2n8Ffc9NA"

bot = Bot(token=bot_token)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.reply("Вітаю! Напиши мені назву міста і я надам дані про погоду!")


@dp.message()
async def get_weather(message: types.Message):
    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Хмарно \U00002601",
        "Rain": "Дощ \U00002614",
        "Drizzle": "Невеликий дощ \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Сніг \U0001F328",
        "Mist": "Туман \U0001F32B"
    }

    try:
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
        )
        data = r.json()

        city = data["name"]
        cur_weather = data["main"]["temp"]

        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Подивись у вікно, не втямлю, що там за погода!"

        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
            data["sys"]["sunrise"])

        await message.reply(f"Дата: {datetime.datetime.now().strftime('%Y-%m-%d  Час: %H:%M')}\n"
                            f"Погода в місті: {city}\n"
                            f"Температура: {cur_weather}C° {wd}\n"
                            f"Вологість: {humidity}%\n"
                            f"Тиск: {pressure} мм.рт.ст\n"
                            f"Вітер: {wind} м/с\n"
                            f"Схід сонця: {sunrise_timestamp}\n"
                            f"Захід сонця: {sunset_timestamp}\n"
                            f"Тривалість дня: {length_of_the_day}\n"
                            )

    except:
        await message.reply("\U00002620 Перевірте назву міста \U00002620")


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())