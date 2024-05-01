from flask import Flask, request
import sqlite3

app = Flask(__name__)

con = sqlite3.connect("database.db")
cur = con.cursor()

cur.execute("""
            CREATE TABLE IF NOT EXISTS brukere(
            id int primary key,
            navn text
            )
            """)
cur.execute("""
            CREATE TABLE IF NOT EXISTS todo(
            id int primary key,
            bruker_id int,
            task text
            )
            """)

if __name__ == "__main__":
  app.run(debug=True, port=5020)