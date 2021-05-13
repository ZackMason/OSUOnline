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

from flask import Flask, redirect, url_for, render_template, request, flash, json
import connection as connect

import os
from random import *
import string

import secrets

secret_key = secrets.token_hex(16)


def get_entities():
    attributes = ['ID', 'name', 'description']
    query = "SELECT * FROM player;"
    cursor = connect.execute_query(connection, query)
    results = json.dumps(cursor.fetchall())
    res = json.loads(results)
    entities = [{
        'ID': res[i]["player_id"],
        'name': res[i]["name"],
        'description':res[i]["email"],
    } for i in range(len(res))]
    return attributes, entities


def get_players():
    attributes = ['ID', 'name', 'description', 'email', 'level', 'experience', 'health', 'current_map']
    query = "SELECT * FROM player;"
    cursor = connect.execute_query(connection, query)
    results = json.dumps(cursor.fetchall())
    res = json.loads(results)
    entities = [{
        'ID': res[i]["player_id"],
        'name': res[i]["name"],
        'health': res[i]["health"],
        'email': res[i]["email"],
        'level': res[i]["level"],
        'experience': res[i]["experience"],
        'current_map': res[i]["current_map"]
    } for i in range(0, len(res))]
    return attributes, entities


def get_quests():
    attributes = ['ID', 'name', 'description', 'experience_reward']
    query = "SELECT * FROM quest;"
    cursor = connect.execute_query(connection, query)
    results = json.dumps(cursor.fetchall())
    res = json.loads(results)
    entities = [{
        'ID': res[i]["quest_id"],
        'name': res[i]["name"],
        'description': res[i]["description"],
        'experience_reward': res[i]["experience_reward"],
    } for i in range(len(res))]
    return attributes, entities


def get_items():
    attributes = ['ID', 'name', 'description', 'quality', 'sprite']
    query = "SELECT * FROM items;"
    cursor = connect.execute_query(connection, query)
    results = json.dumps(cursor.fetchall())
    res = json.loads(results)
    entities = [{
        'ID': res[i]["item_id"],
        'name': res[i]["name"],
        'description': res[i]["description"],
        'quality': res[i]["quality"],
        'sprite': res[i]["sprite"] + '.png',
    } for i in range(len(res))]
    return attributes, entities


def get_maps():
    attributes = ['ID', 'name', 'description', 'sprite']
    query = "SELECT * FROM map;"
    cursor = connect.execute_query(connection, query)
    results = json.dumps(cursor.fetchall())
    res = json.loads(results)
    entities = [{
        'ID': res[i]["map_id"],
        'name': res[i]["name"],
        'description': None,
        'sprite': res[i]["map_sprite"] + '.png',
    } for i in range(len(res))]
    return attributes, entities


def get_npcs():
    attributes = ['ID', 'name', 'description', 'faction']
    query = "SELECT * FROM npc;"
    cursor = connect.execute_query(connection, query)
    results = json.dumps(cursor.fetchall())
    res = json.loads(results)
    entities = [{
        'ID': res[i]["npc_id"],
        'name':res[i]["name"],
        'description': res[i]["description"],
        'faction': res[i]["faction"],
    } for i in range(len(res))]
    return attributes, entities


app = Flask(__name__)

app.config['SECRET_KEY'] = secret_key


@app.route('/players', methods=['GET', 'POST'])
def players():
    attributes, entities = get_players()

    if request.method == 'POST':
        flash('Post request: ' + str(request.form))
    elif request.method == 'GET':
        pass

    return render_template('players.html', title='Players', attributes=attributes, results=entities)


@app.route('/quests')
def quests():
    attributes, entities = get_quests()

    if request.method == 'POST':
        flash('Post request: ' + str(request.form))
    elif request.method == 'GET':
        pass
    return render_template('quests.html', title='Quests', attributes=attributes, results=entities)


@app.route('/items')
def items():
    attributes, entities = get_items()

    if request.method == 'POST':
        flash('Post request: ' + str(request.form))
    elif request.method == 'GET':
        pass

    return render_template('items.html', title='Items', attributes=attributes, results=entities)


@app.route('/npcs')
def npcs():
    attributes, entities = get_npcs()

    if request.method == 'POST':
        flash('Post request: ' + str(request.form))
    elif request.method == 'GET':
        pass

    return render_template('npcs.html', title='NPCs', attributes=attributes, results=entities)


@app.route('/maps')
def maps():
    attributes, entities = get_maps()

    if request.method == 'POST':
        flash('Post request: ' + str(request.form))
    elif request.method == 'GET':
        pass

    return render_template('maps.html', title='Maps', attributes=attributes, results=entities)


@app.route('/player_inventory')
def player_inventory():
    attributes = ['pid', 'ItemID']
    entities = [{'pid': randrange(0, 100), 'ItemID': randrange(0, 100)} for i in range(20)]

    if request.method == 'POST':
        flash('Post request: ' + str(request.form))
    elif request.method == 'GET':
        pass

    return render_template('player_inventory.html', title='Player Inventory', attributes=attributes, results=entities)


@app.route('/player_quests')
def player_quests():
    attributes = ['pid', 'qid']
    entities = [{'pid': randrange(0, 100), 'qid': randrange(0, 100)} for i in range(20)]

    if request.method == 'POST':
        flash('Post request: ' + str(request.form))
    elif request.method == 'GET':
        pass

    return render_template('player_inventory.html', title='Player Quests', attributes=attributes, results=entities)


@app.route('/npc_droptable')
def npc_droptable():
    attributes = ['pid', 'ItemID']
    entities = [{'pid': randrange(0, 100), 'ItemID': randrange(0, 100)} for i in range(20)]

    if request.method == 'POST':
        flash('Post request: ' + str(request.form))
    elif request.method == 'GET':
        pass

    return render_template('player_inventory.html', title='NPC Drop Table', attributes=attributes, results=entities)


@app.route('/npc_spawned')
def npc_spawned():
    attributes = ['pid', 'mid']
    entities = [{'pid': randrange(0, 100), 'mid': randrange(0, 100)} for i in range(20)]

    if request.method == 'POST':
        flash('Post request: ' + str(request.form))
    elif request.method == 'GET':
        pass

    return render_template('player_inventory.html', title='NPCs Spawned', attributes=attributes, results=entities)


@app.route('/')
@app.route('/home')
@app.route('/homepage')
@app.route('/dashboard')
def dashboard():
    attributes, entities = get_entities()
    return render_template('dashboard.html', attributes=attributes, results=entities)


if __name__ == '__main__':
    local = bool(os.environ.get('LOCAL', True))

    PORT = int(os.environ.get('PORT', 18345))
    HOST = '127.0.0.1' if local else '0.0.0.0'
    connection = connect.connect('your login', 'your_password', 'login_again')
    app.run(host=HOST, port=PORT)
