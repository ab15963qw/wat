from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = ''

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def weather():
    city = request.form.get('city')
    if city:
        weather_data = get_weather(city)
        if weather_data:
            return render_template('weather.html', weather=weather_data, city=city)
        else:
            return render_template('weather.html', error="無法獲取天氣資訊，請確認城市名稱。")
    return render_template('weather.html', error="請輸入一個城市名稱。")

def get_weather(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather = {
            'temperature': data['main']['temp'],
            'description': data['weather'][0]['description'],
            'humidity': data['main']['humidity'],
            'wind_speed': data['wind']['speed']
        }
        return weather
    return None

if __name__ == '__main__':
    app.run(debug=True)
