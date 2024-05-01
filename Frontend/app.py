from flask import Flask, render_template, redirect, request, url_for
import requests

app = Flask(__name__)

@app.route('/', methods = ["GET"])
def index():
  return render_template('index.html')

@app.route("/logg_inn", methods = ["POST"])
def logg_inn():
  navn = request.form.get("fornavn")
  print(navn)
  content = requests.get('http://127.0.0.1:5020/logg_inn', json={"navn": navn}).json()
  if content["Status"] == "A user":
    return redirect(url_for('home_page', bruker_navn=content["bruker_navn"]))
  return render_template("index.html", feil="Fant ikke bruker i systemet")

@app.route("/home_page/<bruker_navn>", methods = ["GET"])
def home_page(bruker_navn):
  
  return render_template("home.html")

if __name__ == '__main__':
  app.run(debug=True, port=5010)