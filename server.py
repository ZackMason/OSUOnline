from flask import Flask, redirect, url_for, render_template
from connection import connect

app = Flask(__name__)

local = True

PORT = 18345
HOST = '127.0.0.1' if local else '0.0.0.0'

@app.route('/')
def home_page():
    res = ""
      
    return render_template("homepage.html", content=res)

@app.route('/login/<name>')
def login(name=None):
    return "Hello %s, how are you?" % name

if __name__ == '__main__':
    app.run(host=HOST, port=PORT)
