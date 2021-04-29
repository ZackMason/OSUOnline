from flask import Flask, redirect, url_for, render_template
from connection import connect

app = Flask(__name__)

<<<<<<< Updated upstream
local = True

PORT = 18345
HOST = '127.0.0.1' if local else '0.0.0.0'

@app.route('/')
def home_page():
    res = ""
      
    return render_template("homepage.html", content=res)
=======
>>>>>>> Stashed changes

@app.route('/players')
def players():
    return render_template("players.html")

@app.route('/quests')
def quests():
    return render_template("quests.html")

@app.route('/items')
def items():
    return render_template("items.html")

@app.route('/npcs')
def npcs():
    return render_template("npcs.html")

@app.route('/player/<name>')
def login(name=None):
    return "Hello %s, how are you?" % name

@app.route('/')
@app.route('/homepage')
@app.route('/home')
def home_page():
    return render_template("homepage.html")

if __name__ == '__main__':
<<<<<<< Updated upstream
    app.run(host=HOST, port=PORT)
=======
    local = bool(os.environ.get('LOCAL', True))

    PORT = int(os.environ.get('PORT', 18345))
    HOST = '127.0.0.1' if local else '0.0.0.0'

    app.run(host=HOST, port=PORT)
>>>>>>> Stashed changes
