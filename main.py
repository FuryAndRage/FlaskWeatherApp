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
	return res


def get_api_byloc(lat,lon):
	city = 'Auckland'
	api_key = secret_api_key()
	url = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}'
	req = requests.get(url)
	res = []
	for chave, valor in req.json().items():
		res.append({chave: valor})
	return res

def convert_time(res):
	timestamp = ''
	if len(res) == 14:
		timestamp = datetime.datetime.fromtimestamp(res[8]['dt'])
	elif len(res) == 13:
		timestamp = datetime.datetime.fromtimestamp(res[7]['dt'])
	else:
		timestamp = datetime.datetime.fromtimestamp(res[6]['dt'])
	date_time = timestamp.strftime('%d/%m/%Y')
	time_time = timestamp.strftime('%H:%M')
	time = {'date': date_time, 'time':time_time}
	return time

	# print({chave:valor for (chave, valor) in req_json.items()})

@app.route('/', methods=['POST','GET'])
def home():
	res = get_api()
	lat = request.form.get('lat')
	lon = request.form.get('lon')

	if request.method == 'POST':
		lat = request.form.get('lat')
		lon = request.form.get('lon')
		res = get_api_byloc(lat,lon)
	
	current_temp = int(res[3]['main']['temp'] - 273.15 )
	feel = int(res[3]['main']['feels_like'] - 273.15)
	temp_min = int(res[3]['main']['temp_min'] - 273.15)
	temp_max = int(res[3]['main']['temp_max'] - 273.15 )

	return render_template('index.html', res = res, temp={'current':current_temp,'feel':feel,'temp_min':temp_min, 'temp_max':temp_max, 'time':convert_time(res)}  )

if __name__ == '__main__':
	app.run(debug=True)


#api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={your api key}
#East being at 90 degrees, South at 180 degrees, West at 270 degrees, and North at 360 degrees (or zero degrees).
#North East (45 degrees), East (90 degrees), South East (135 degrees), South (180 degrees), 
#South West (225 degrees), West (270 degrees), and North West (315 degrees).