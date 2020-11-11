# Twitter Sentiment Stock Predictor

## Overview
Twitter Sentiment Stock Predictor is a full-stack app that allows the user to input a company name and view the percentage of positive and negative feedback on Twitter about that company's stock, the stock's closing prices over the past 5 days, as well as whether or not the user should buy or sell stock in that company. This app uses a Twitter Sentiment machine learning model, trained with Twitter sentiment data gathered from an API call to Twitter using the tweepy library. The model is trained to predict whether the user should buy or sell stock in the company. The app also retrieves the closing price data using the Yahoo Finance (yfinance) library. When the user inputs a company name, the app retrieves the company's data if the name is present in a csv file with a list of over 3000 top companies. Once the name can be verified from the list, the API call is made to Twitter to retrieve sentiment data for the Twitter Sentiment model, and closing price data is retrieved from the yfinance library. The user is then prompted to another page to view the model's analysis ("Buy" or "Sell"), as well as visualizations of the Twitter sentiment and closing price data for the company's stock. 
![alt text](https://github.com/IsabellaAguilera/Twitter-Sentiment-Stock-Predictor/blob/master/images/home_page.png?raw=true)


## Technologies/Frameworks
Front End
* HTML/CSS
* JavaScript
* BootStrap

Back End
* Python
* Flask

## Libraries
* Plotly.js
* TensorFlow.py

