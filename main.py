from flask import Flask, render_template, redirect, request
import requests
from secret import secret_api_key

app = Flask(__name__, static_url_path='/static')


def get_api():
	city = 'Auckland'
	api_key = secret_api_key()
	url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
	req = requests.get(url)
	res = []
	for item in req.json().values():
		res.append(item)
	print(res[1][0]['icon'])
	return res

	# print({chave:valor for (chave, valor) in req_json.items()})

@app.route('/')
def home():
	
	return render_template('index.html', res = get_api())

if __name__ == '__main__':
	app.run(debug=True)