import sys

from flask import Flask, render_template, request, redirect, Response, url_for
import random, json

import stock_data
import twitter_data
import prediction
import time



app = Flask(__name__)

company = []

@app.route('/')
def homepage():
	# serve index template
	return render_template('index.html')

@app.route('/stock')
def visualizations():
	return render_template('index2.html')



@app.route('/company', methods=["POST"])
def data():
	global company
	
	name = request.form['company']
	if stock_data.is_valid_company(name):
		company.append(name)
		json_data()
		return redirect("/stock")
	else:
		return redirect("/")

@app.route("/json_data", methods=["POST", "GET"])
def json_data():
	global company

	pred = str(prediction.get_Prediction(company[len(company) - 1]))

	return pred

if __name__ == '__main__':
    app.run(debug = True)
