from flask import Flask, render_template, redirect, request, url_for
import requests

app = Flask(__name__)

@app.route('/', methods = ["GET"])
def index():
  return redirect('/logg_inn')

@app.route("/logg_inn", methods = ["GET","POST"])
def logg_inn():
  if request.method == "GET":
    return render_template("index.html")
  
  if request.method == "POST":
    navn = request.form.get("fornavn")
    content = requests.get('http://127.0.0.1:5020/logg_inn', json={"navn": navn}).json()
    if content["Status"] == "A user":
      return redirect(url_for('home_page', bruker_id=content["bruker_id"]))
    return render_template("index.html", feil="Fant ikke bruker i systemet")

@app.route("/home_page/<bruker_id>", methods = ["GET"])
def home_page(bruker_id):
  data = requests.get('http://127.0.0.1:5020/get_todos', json={"bruker_id": bruker_id}).json()
  return render_template("home.html", bruker_id=bruker_id, data=data)

@app.route("/todo_post/<bruker_id>", methods = ["POST"])
def todo_post(bruker_id):
  task = request.form.get("task")
  requests.post('http://127.0.0.1:5020/legg_til_todo', json={"bruker_id": bruker_id, "task": task})
  return redirect(url_for('home_page', bruker_id=bruker_id))

@app.route('/slett_todo/<bruker_id>/<todo_id>', methods = ["POST"])
def slett_todo(bruker_id, todo_id):
  requests.delete('http://127.0.0.1:5020/slett_todo', json={"id": todo_id})
  return redirect(url_for('home_page', bruker_id=bruker_id))

@app.route('/rediger_todo/<bruker_id>/<todo_id>', methods = ["GET", "POST"])
def rediger_todo(bruker_id, todo_id):
  if request.method == "GET":
    data = requests.get('http://127.0.0.1:5020/rediger_todo', json={"id": todo_id}).json()
    return render_template('rediger.html', bruker_id=bruker_id, todo_id=data["id"], todo=data["todo"])
  
  if request.method == "POST":
    task = request.form.get("task")
    requests.put('http://127.0.0.1:5020/rediger_todo', json={"id": todo_id, "task": task})
    return redirect(url_for('home_page', bruker_id=bruker_id))

if __name__ == '__main__': 
  app.run(debug=True, port=5010)