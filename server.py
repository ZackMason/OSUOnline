'''
###############################################################################
Server.py

Description:
    The backend for the website

Notes:
    The port is specified using the environment variable PORT
    The host is specified using the environment variable LOCAL

###############################################################################
'''

import os

from flask import Flask, redirect, url_for, render_template
from connection import connect

import os
from random import *
import string

def get_fake_entities():
    attributes = ['ID', 'name', 'description']
    entities = [ {
        'ID': randint(0,100), 
        'name':''.join(choice(string.ascii_letters) for i in range(randint(4,12))),
        'description': ''.join(choice(string.ascii_letters) for i in range(randint(10,42))),
        } for i in range(20)]
    return attributes, entities


def get_fake_players():
    attributes = ['ID', 'name', 'description', 'email', 'level', 'experience', 'health', 'current_map']
    entities = [ {
        'ID': randint(0,100), 
        'name':''.join(choice(string.ascii_letters) for i in range(randint(4,12))),
        'description': ''.join(choice(string.ascii_letters) for i in range(randint(10,42))),
        'email': 'email@email.com',
        'level': 1,
        'experience': 0,
        'current_map': 0
        } for i in range(20)]
    return attributes, entities


def get_fake_quests():
    attributes = ['ID', 'name', 'description', 'experience_reward']
    entities = [ {
        'ID': randint(0,100), 
        'name':''.join(choice(string.ascii_letters) for i in range(randint(4,12))),
        'description': ''.join(choice(string.ascii_letters) for i in range(randint(10,42))),
        'experience_reward': randint(0,15555),
        } for i in range(20)]
    return attributes, entities

def get_fake_items():
    attributes = ['ID', 'name', 'description', 'quality', 'sprite']
    entities = [ {
        'ID': randint(0,100), 
        'name':''.join(choice(string.ascii_letters) for i in range(randint(4,12))),
        'description': ''.join(choice(string.ascii_letters) for i in range(randint(10,42))),
        'quality': randint(0,5),
        'sprite': ''.join(choice(string.ascii_letters) for i in range(randint(4,12))) + '.png',
        } for i in range(20)]
    return attributes, entities

def get_fake_maps():
    attributes = ['ID', 'name', 'description', 'sprite']
    entities = [ {
        'ID': randint(0,100), 
        'name':''.join(choice(string.ascii_letters) for i in range(randint(4,12))),
        'description': ''.join(choice(string.ascii_letters) for i in range(randint(10,42))),
        'sprite': ''.join(choice(string.ascii_letters) for i in range(randint(4,12))) + '.png',
        } for i in range(20)]
    return attributes, entities


def get_fake_npcs():
    attributes = ['ID', 'name', 'description', 'faction']
    entities = [ {
        'ID': randint(0,100), 
        'name':''.join(choice(string.ascii_letters) for i in range(randint(4,12))),
        'description': ''.join(choice(string.ascii_letters) for i in range(randint(10,42))),
        'faction': randint(0,4),
        } for i in range(20)]
    return attributes, entities



app = Flask(__name__)

@app.route('/players')
def players():
    attributes, entities = get_fake_players()
    return render_template('players.html', title='Players', attributes=attributes, results=entities)

@app.route('/quests')
def quests():
    attributes, entities = get_fake_quests()
    return render_template('quests.html', title='Quests', attributes=attributes, results=entities)

@app.route('/items')
def items():
    attributes, entities = get_fake_items()
    return render_template('items.html', title='Items', attributes=attributes, results=entities)

@app.route('/npcs')
def npcs():
    attributes, entities = get_fake_npcs()
    return render_template('npcs.html', title='NPCs', attributes=attributes, results=entities)

@app.route('/maps')
def maps():
    attributes, entities = get_fake_maps()
    return render_template('maps.html', title='Maps', attributes=attributes, results=entities)

@app.route('/')
@app.route('/home')
@app.route('/homepage')
@app.route('/dashboard')
def dashboard():
    attributes, entities = get_fake_entities()
    return render_template('dashboard.html', attributes=attributes, results=entities)

if __name__ == '__main__':
    local = bool(os.environ.get('LOCAL', True))

    PORT = int(os.environ.get('PORT', 18345))
    HOST = '127.0.0.1' if local else '0.0.0.0'

    app.run(host=HOST, port=PORT)