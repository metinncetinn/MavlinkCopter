import requests

api_key = "api"
city = "London"
url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
response = requests.get(url)
weather_data = response.json()
print(weather_data)
