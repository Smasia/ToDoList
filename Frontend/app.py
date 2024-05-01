from flask import Flask, render_template, redirect, request
import requests

app = Flask(__name__)

@app.route('/', methods = ["GET"])
def home_page():
  return render_template('index.html')


if __name__ == '__main__':
  app.run(debug=True, port=5010)