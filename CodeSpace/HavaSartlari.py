import requests

api_key = "99c3a681bc8bc5a9f7cb26db1f21b18e"
city = "London"
url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
response = requests.get(url)
weather_data = response.json()
print(weather_data)
