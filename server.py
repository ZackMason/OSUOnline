from flask import Flask, redirect, url_for, render_template
from connection import connect

import os
from random import *
import string

def get_fake_entities():
    attributes = ['id', 'name', 'description']
    entities = [ {
        'id': randint(0,100), 
        'name':''.join(choice(string.ascii_letters) for i in range(randint(0,12))),
        'description': ''.join(choice(string.ascii_letters) for i in range(randint(0,22))),
        } for i in range(20)]
    return attributes, entities

app = Flask(__name__)

@app.route('/players')
def players():
    attributes, entities = get_fake_entities()
    return render_template('dashboard.html', title='Players', attributes=attributes, results=entities)

@app.route('/quests')
def quests():
    attributes, entities = get_fake_entities()
    return render_template('dashboard.html', title='Quests', attributes=attributes, results=entities)

@app.route('/items')
def items():
    attributes, entities = get_fake_entities()
    return render_template('dashboard.html', title='Items', attributes=attributes, results=entities)

@app.route('/npcs')
def npcs():
    attributes, entities = get_fake_entities()
    return render_template('dashboard.html', title='NPCs', attributes=attributes, results=entities)

@app.route('/maps')
def maps():
    attributes, entities = get_fake_entities()
    return render_template('dashboard.html', title='Maps', attributes=attributes, results=entities)


@app.route('/player/<name>')
def login(name=None):
    return "Hello %s, how are you?" % name

@app.route('/dashboard')
def dashboard():
    attributes, entities = get_fake_entities()
    return render_template('dashboard.html', attributes=attributes, results=entities)

@app.route('/')
@app.route('/homepage')
@app.route('/home')
def home_page():
    return render_template("homepage.html")

if __name__ == '__main__':
    local = bool(os.environ.get('LOCAL', True))

    PORT = int(os.environ.get('PORT', 18345))
    HOST = '127.0.0.1' if local else '0.0.0.0'

    app.run(host=HOST, port=PORT)
