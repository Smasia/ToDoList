from flask import Flask, request
import sqlite3

app = Flask(__name__)

con = sqlite3.connect("database.db", check_same_thread=False)
cur = con.cursor()

cur.execute("""
            CREATE TABLE IF NOT EXISTS brukere(
            id integer primary key,
            navn text
            )
            """)
cur.execute("""
            CREATE TABLE IF NOT EXISTS todo(
            id integer primary key,
            bruker_id integer,
            task text
            )
            """)

cur.execute("DELETE from brukere")

brukere = ["Sander", "Kjell", "Harald"]

cur.executemany("""
            INSERT INTO brukere(navn)
            VALUES(?)
            """, [(navn,) for navn in brukere])
con.commit()

@app.route("/logg_inn", methods = ["GET"])
def logg_inn():
  navn = request.get_json()["navn"]
  cur.execute("SELECT * from brukere WHERE navn = ?", (navn,))
  content = cur.fetchone()
  if content == None:
    return {"Status": "Not a user"}
  else:
    return {"Status": "A user", "bruker_id": content[0], "bruker_navn": content[1]}

@app.route('/get_todos', methods = ["GET"])
def get_todos():
  bruker_id = request.get_json()["bruker_id"]
  cur.execute("SELECT todo.id, todo.task FROM brukere INNER JOIN todo ON todo.bruker_id = brukere.id WHERE brukere.id = ?", (bruker_id,))

  data = cur.fetchall()
  content = []
  for todo in data:
    content.append({"id": todo[0], "todo": todo[1]})
  print(content)
  return content

@app.route('/legg_til_todo', methods = ["POST"])
def legg_til_todo():
  task = request.get_json()["task"]
  bruker_id = request.get_json()["bruker_id"]
  cur.execute("INSERT INTO todo(bruker_id, task) VALUES(?,?)", (bruker_id, task))
  con.commit()
  return {"Status": "no error"}

if __name__ == "__main__":
  app.run(debug=True, port=5020)