import time
from binance import Client
import numpy as np
from config import api_key, api_secret

client = Client(api_key, api_secret)

interval = Client.KLINE_INTERVAL_1HOUR

# Установка начальной цены и начальной временной метки
initial_price = float(client.futures_symbol_ticker(symbol='ETHUSDT')['price'])
initial_timestamp = time.time()

while True:
    try:
        # Получаем текущую цену и время
        current_price = float(client.futures_symbol_ticker(symbol='ETHUSDT')['price'])
        current_timestamp = time.time()

        # Получаем информацию о ценах за последние 60 минут
        klines = client.futures_klines(symbol='ETHUSDT', interval=interval, limit=60)

        # Извлечение цен из данных klines
        prices = np.array([float(kline[4]) for kline in klines])

        price_change = (current_price - initial_price) / initial_price * 100

        # Расчет коэффициента корреляции
        btc_prices = np.array(
            [float(kline[4]) for kline in client.futures_klines(symbol='BTCUSDT', interval=interval, limit=60)])
        correlation = np.corrcoef(prices, btc_prices)[0][1]

        if abs(price_change) > 1 and abs(correlation) < 0.5:
            print("За последний час цена изменилась более чем на 1%: ", current_price)

        initial_price = current_price
        initial_timestamp = current_timestamp

        time.sleep(60)

    except Exception as e:
        print(e)
