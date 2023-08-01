import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def alpha_trend(close, high, low, coeff=0.7, AP=21, novolumedata=False):
    # Function code here
    ATR = np.mean(np.abs(high - low))
    upT = low - ATR * coeff
    downT = high + ATR * coeff

    if novolumedata:
        condition = (pd.Series(close).rolling(window=AP).mean() >= 50)
    else:
        hlc3 = (high + low + close) / 3
        condition = (pd.Series(hlc3).rolling(window=AP).mean() >= 50)

    AlphaTrend = np.zeros_like(close)

    for i in range(1, len(close)):
        if condition[i]:
            if upT[i] < AlphaTrend[i - 1]:
                AlphaTrend[i] = AlphaTrend[i - 1]
            else:
                AlphaTrend[i] = upT[i]
        else:
            if downT[i] > AlphaTrend[i - 1]:
                AlphaTrend[i] = AlphaTrend[i - 1]
            else:
                AlphaTrend[i] = downT[i]

    return AlphaTrend

# Sembolü belirtin ve veri aralığını seçin
symbol = "BTC-USD"
start_date = "2023-03-05"
end_date = "2023-08-31"

# Verileri alın
df = yf.download(symbol, start=start_date, end=end_date)

# Fiyat verilerini çıkarın
close_prices = df["Close"].values
high_prices = df["High"].values
low_prices = df["Low"].values

# AlphaTrend hesapla
alpha_trend_values = alpha_trend(close_prices, high_prices, low_prices, coeff=0.7, AP=21, novolumedata=False)

# Grafiği çiz
plt.figure(figsize=(10, 6))
plt.plot(alpha_trend_values, label='AlphaTrend', color='blue', linewidth=2)
plt.axhline(100, color='gray', linestyle='--', label='Upper Band', linewidth=1)
plt.axhline(0, color='gray', linestyle='--', label='Lower Band', linewidth=1)

# Alış uyarısı vermek için eşik değeri
buy_threshold = 24500

# AlphaTrend değerleri eşik değerini aşarsa alış uyarısı ver
if alpha_trend_values[-1] > buy_threshold:
    buy_alert = "Alış uyarısı: AlphaTrend değeri 24500'nin üzerine çıktı!"
    plt.axhline(buy_threshold, color='green', linestyle='--', label='Buy Threshold', linewidth=1)
    plt.text(len(alpha_trend_values) - 1, buy_threshold, buy_alert, color='green')

# Satış uyarısı vermek için eşik değeri
sell_threshold = 24000

# AlphaTrend değerleri eşik değerinin altına düşerse satış uyarısı ver
if alpha_trend_values[-1] < sell_threshold:
    sell_alert = "Satış uyarısı: AlphaTrend değeri 24000'nin altına düştü!"
    plt.axhline(sell_threshold, color='red', linestyle='--', label='Sell Threshold', linewidth=1)
    plt.text(len(alpha_trend_values) - 1, sell_threshold, sell_alert, color='red')

plt.legend()
plt.title('AlphaTrend Indicator for ' + symbol)
plt.xlabel('Time')
plt.ylabel('AlphaTrend Values')
plt.grid(True)

# Daha kritik destek ve dirençlerin belirlenmesi için ekleme
critical_support = 23000
critical_resistance = 25500
plt.axhline(critical_support, color='orange', linestyle='--', label='Critical Support', linewidth=1)
plt.axhline(critical_resistance, color='purple', linestyle='--', label='Critical Resistance', linewidth=1)

plt.show()
