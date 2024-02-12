from flask import Flask, render_template_string, render_template, jsonify
#import requests
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(__name__)  

# Fonction pour récupérer les données sur les commits depuis l'API GitHub

def get_commit_data():
    url = 'https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

# Fonction pour extraire les minutes d'une date formatée

@app.route('/extract-minutes/<date_string>')
def extract_minutes(date_string):
    date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
    minutes = date_object.minute
    return jsonify({'minutes': minutes})

# Route pour afficher les données des commits
@app.route('/commits/')
def commits():
    commit_data = get_commit_data()
    if commit_data:
        commits_per_minute = {}
        for commit in commit_data:
            date_string = commit['commit']['author']['date']
            minutes = extract_minutes(date_string).json['minutes']
            if minutes in commits_per_minute:
                commits_per_minute[minutes] += 1
            else:
                commits_per_minute[minutes] = 1
        return jsonify(commits_per_minute)
    else:
        return "Erreur lors de la récupération des données sur les commits."



@app.route('/')
def hello_world():
    return render_template('hello.html')                                                                                                                
                                                                                                                                       
@app.route('/contact/')
def MaPremiereAPI():
    return render_template("contact.html")


@app.route('/paris/')
def meteo():
    response = urlopen('https://api.openweathermap.org/data/2.5/forecast/daily?q=Paris,fr&cnt=16&appid=bd5e378503939ddaee76f12ad7a97608')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('temp', {}).get('day') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)


@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogramme/")
def monhistogramme():
    return render_template("histogramme.html")

  
if __name__ == "__main__":
  app.run(debug=True)
