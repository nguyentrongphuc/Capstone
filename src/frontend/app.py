import os
from flask import Flask, render_template, redirect, url_for, request, jsonify, abort
from flask_cors import CORS
import requests
import config

app = Flask(__name__)
app.config.from_object('config')
CORS(app)


@app.route('/')
def home():
    url = 'http://127.0.0.1:5000/makes'
    response = requests.get(url)
    makes=response.json()["makes"]
    return render_template('home.html', 
            makes=makes,
            active_make = makes[0],
            models=makes[0]["models"]
        )

@app.route('/login')
def login():
    link = build_login_link('login_result')
 
    return redirect(link)

@app.route('/login_result')
def login_result():
    return render_template('login_result.html')

@app.route('/logout')
def logout():
    return render_template('logout.html')

def build_login_link(callbackPath = ''):
    link = 'https://'
    link += config.auth0_url + '.auth0.com'
    link += '/authorize?'
    link += 'audience=' + config.auth0_audience + '&'
    link += 'response_type=token&'
    link += 'client_id=' + config.auth0_clientId + '&'
    link += 'redirect_uri=' +config.auth0_callbackURL + callbackPath
    return link;
