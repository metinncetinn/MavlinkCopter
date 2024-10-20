import requests
from datetime import datetime
import key

api_key = key.api_key
city = "Konya"

# API çağrısını yap
url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
response = requests.get(url)
weather_data = response.json()

#Tüm sonuçlar.
#print(weather_data)

# Sıcaklığı C cinsine çevir
kelvin_temp = weather_data['main']['temp']
celsius_temp = kelvin_temp - 273.15

# Gün doğumu ve gün batımı zamanlarını al ve dönüştür
sunrise_time = datetime.fromtimestamp(weather_data['sys']['sunrise'])
sunset_time = datetime.fromtimestamp(weather_data['sys']['sunset'])

#Rüzgar hızı m/s geliyor km/h çeviriliyor.
windSpeed = weather_data['wind']['speed'] * 3.6

#Rüzgarın hızı kontrol ediliyor
def RuzgarKontrol(maxRuzgar):
    if windSpeed < maxRuzgar:
        print("Ucus icin ruzgar uygun")
        return True
    else:
        print("Ruzgar ucus icin çok fazla")
        return False


"""
# Sonuçları yazdır
print(f"Sicaklik: {celsius_temp:.2f} °C")
print(f"Ruzgar Hizi: {windSpeed:.2f} km/h")
print(f"Gün doğumu: {sunrise_time.strftime('%H:%M:%S')}")
print(f"Gün batimi: {sunset_time.strftime('%H:%M:%S')}")
"""