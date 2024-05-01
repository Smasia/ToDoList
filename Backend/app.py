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

if __name__ == "__main__":
  app.run(debug=True, port=5020)