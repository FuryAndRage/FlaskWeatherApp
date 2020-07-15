from flask import Flask, render_template, redirect, request
import requests
from secret import secret_api_key
import datetime
app = Flask(__name__, static_url_path='/static')


def get_api():
	city = 'Auckland'
	api_key = secret_api_key()
	url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
	req = requests.get(url)
	res = []
	for chave, valor in req.json().items():
		res.append({chave: valor})
	#(32 °F − 32) × 5/9 = 0 °C
	
	temp = int(300 - res[3]['main']['temp'])
	print(temp)
	return res

def convert_time():
	res = get_api()
	timestamp = datetime.datetime.fromtimestamp(res[8]['dt'])
	date_time = timestamp.strftime('%d/%m/%Y')
	time_time = timestamp.strftime('%H:%M:%S')
	time = {'date': date_time, 'time':time_time}
	return time

	# print({chave:valor for (chave, valor) in req_json.items()})

@app.route('/')
def home():
	res = get_api()
	current_temp = int(res[3]['main']['temp'] - 273.15 )
	feel = int(res[3]['main']['feels_like'] - 273.15)
	temp_min = int(res[3]['main']['temp_min'] - 273.15)
	temp_max = int(res[3]['main']['temp_max'] - 273.15 )

	return render_template('index.html', res = res, temp={'current':current_temp,'feel':feel,'temp_min':temp_min, 'temp_max':temp_max, 'time':convert_time()}  )

if __name__ == '__main__':
	app.run(debug=True)