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
from connection import *

import os
from random import *
import string

import secrets

secret_key = secrets.token_hex(16)
login_name = str(os.environ.get('LOGIN', 'your_login'))
login_pswd = str(os.environ.get('DB_PASS', 'your_password'))
login_db = str(os.environ.get('DATABASE', 'login_again'))


def get_entities():
    attributes = ['ID', 'name', 'description']
    query = "SELECT * FROM player;"
    with connect(login_name, login_pswd, login_db) as connection:
        with execute_query(connection, query) as cursor:
            results = json.dumps(cursor.fetchall())
            res = json.loads(results)
            entities = [{
                'ID': res[i]["player_id"],
                'name': res[i]["name"],
                'description': res[i]["email"],
            } for i in range(len(res))]
            return attributes, entities


def get_players():
    attributes = ['name', 'health', 'email', 'level', 'experience', 'current_map']
    query = "SELECT * FROM player;"
    with connect(login_name, login_pswd, login_db) as connection:
        with execute_query(connection, query) as cursor:
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
    attributes = ['name', 'description', 'experience_reward']
    query = "SELECT * FROM quest;"
    with connect(login_name, login_pswd, login_db) as connection:
        with execute_query(connection, query) as cursor:
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
    attributes = ['name', 'description', 'quality', 'sprite']
    query = "SELECT * FROM items;"
    with connect(login_name, login_pswd, login_db) as connection:
        with execute_query(connection, query) as cursor:
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
    attributes = ['name', 'map_sprite']
    query = "SELECT * FROM map;"
    with connect(login_name, login_pswd, login_db) as connection:
        with execute_query(connection, query) as cursor:
            results = json.dumps(cursor.fetchall())
            res = json.loads(results)
            entities = [{
                'ID': res[i]["map_id"],
                'name': res[i]["name"],
                'sprite': res[i]["map_sprite"] + '.png',
            } for i in range(len(res))]
            return attributes, entities


def get_npcs():
    attributes = [ 'name', 'description', 'faction']
    query = "SELECT * FROM npc;"
    with connect(login_name, login_pswd, login_db) as connection:
        with execute_query(connection, query) as cursor:
            results = json.dumps(cursor.fetchall())
            res = json.loads(results)
            entities = [{
                'ID': res[i]["npc_id"],
                'name': res[i]["name"],
                'description': res[i]["description"],
                'faction': res[i]["faction"],
            } for i in range(len(res))]
            return attributes, entities


app = Flask(__name__)

app.config['SECRET_KEY'] = secret_key


def handle_post_request(request, table='df', attr='df', id=None):
    if request.method == 'POST':
        print('post recieved')
        if not request.form.get('query_type'):
            table_token = '%s %s' % (table, tuple(attr))
            table_token = table_token.replace("'", '')
            data = [request.form.get(a) for a in attr]
            values_token = '%s' % data
            values_token = values_token.replace("", '').replace('[', '(').replace(']', ')')
            if '' in data:
                print('empty field')
            else:
                query = "INSERT INTO %s VALUES %s;" % (table_token, values_token)
                with connect(login_name, login_pswd, login_db) as connection:
                    with execute_query(connection, query) as cursor:
                        pass
            flash('Post request %s' % str(request.form))
        elif request.form.get('query_type') == 'UPDATE':
            query = 'UPDATE %s SET %s WHERE %s=%s'
            data = json.loads(request.form.get('data'))
            set_query = ''
            first = True
            for key, val in data.items():
                if val == '': continue
                if not first:
                    set_query += ', '
                set_query += "%s='%s'" % (key, val) 
                first = False
            query = query % (table, set_query, id, request.form.get('id'))
            with connect(login_name, login_pswd, login_db) as connection:
                with execute_query(connection, query) as cursor:
                    pass
            flash('Update request: %s ' % str(request.form))
        elif request.form.get('query_type') == 'DELETE':
            print('delete recieved')
            query = "DELETE FROM %s WHERE %s=%s;" % (table, id, request.form.get('id'))
            print(query)
            with connect(login_name, login_pswd, login_db) as connection:
                with execute_query(connection, query) as cursor:
                    pass 


@app.route('/players', methods=['GET', 'POST'])
def players():
    attributes, entities = get_players()

    handle_post_request(request, table='player', attr=attributes, id='player_id')

    return render_template('table_page.html', title='Players', attributes=attributes, results=entities,
                           form_attributes=attributes)


@app.route('/quests', methods=['GET', 'POST'])
def quests():
    attributes, entities = get_quests()

    handle_post_request(request, table='quest', attr=attributes, id='quest_id')
    return render_template('table_page.html', title='Quests', attributes=attributes, results=entities,
                           form_attributes=attributes)


@app.route('/items', methods=['GET', 'POST'])
def items():
    attributes, entities = get_items()

    handle_post_request(request, table='items', attr=attributes, id='item_id')

    return render_template('table_page.html', title='Items', attributes=attributes, results=entities,
                           form_attributes=attributes)


@app.route('/npcs', methods=['GET', 'POST'])
def npcs():
    attributes, entities = get_npcs()

    handle_post_request(request, table='npc', attr=attributes, id='npc_id')

    return render_template('table_page.html', title='NPCs', attributes=attributes, results=entities,
                           form_attributes=attributes)


@app.route('/maps', methods=['GET', 'POST'])
def maps():
    attributes, entities = get_maps()

    handle_post_request(request, table='map', attr=attributes, id='map_id')

    return render_template('table_page.html', title='Maps', attributes=attributes, results=entities,
                           form_attributes=attributes)


@app.route('/player_inventory', methods=['GET', 'POST'])
def player_inventory():
    attributes = ['pid', 'ItemID']
    query = "SELECT * FROM player_inventory;"
    with connect(login_name, login_pswd, login_db) as connection:
        with execute_query(connection, query) as cursor:
            results = json.dumps(cursor.fetchall())
            res = json.loads(results)
            entities = [{'pid': res[i]["player_id"],
                         'ItemID': res[i]["item_id"]
                         } for i in range(len(res))]

    if request.method == 'POST':
        pass
    elif request.method == 'GET':
        pass

    return render_template('table_page.html', title='Player Inventory', attributes=attributes, results=entities,form_attributes=attributes)


@app.route('/player_quests', methods=['GET', 'POST'])
def player_quests():
    attributes = ['pid', 'qid']
    query = "SELECT * FROM player_active_quests;"
    with connect(login_name, login_pswd, login_db) as connection:
        with execute_query(connection, query) as cursor:
            results = json.dumps(cursor.fetchall())
            res = json.loads(results)
            entities = [{'pid': res[i]["player_id"],
                         'qid': res[i]["quest_id"]
                         } for i in range(len(res))]

    if request.method == 'POST':
        flash('Post request: ' + str(request.form))
    elif request.method == 'GET':
        pass

    return render_template('table_page.html', title='Player Quests', attributes=attributes, results=entities,form_attributes=attributes)


@app.route('/npc_droptable', methods=['GET', 'POST'])
def npc_droptable():
    attributes = ['pid', 'ItemID']
    query = "SELECT * FROM npc_drop_table;"
    with connect(login_name, login_pswd, login_db) as connection:
        with execute_query(connection, query) as cursor:
            results = json.dumps(cursor.fetchall())
            res = json.loads(results)
            entities = [{
                'pid': res[i]["npc_id"],
                'ItemID': res[i]["item_id"]}
                for i in range(len(res))]

    if request.method == 'POST':
        flash('Post request: ' + str(request.form))
    elif request.method == 'GET':
        pass

    return render_template('table_page.html', title='NPC Drop Table', attributes=attributes, results=entities,form_attributes=attributes)


@app.route('/npc_spawned', methods=['GET', 'POST'])
def npc_spawned():
    attributes = ['pid', 'mid']
    query = "SELECT * FROM spawned_npc;"
    with connect(login_name, login_pswd, login_db) as connection:
        with execute_query(connection, query) as cursor:
            results = json.dumps(cursor.fetchall())
            res = json.loads(results)
            entities = [{'pid': res[i]["npc_id"],
                         'mid': res[i]["map_id"]
                         } for i in range(len(res))]

    if request.method == 'POST':
        flash('Post request: ' + str(request.form))
    elif request.method == 'GET':
        pass

    return render_template('table_page.html', title='NPCs Spawned', attributes=attributes, results=entities,form_attributes=attributes)


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
@app.route('/homepage', methods=['GET', 'POST'])
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    attributes, entities = get_entities()
    return render_template('dashboard.html', attributes=attributes, results=entities)


if __name__ == '__main__':
    local = bool(os.environ.get('LOCAL', True))

    PORT = int(os.environ.get('PORT', 18345))
    HOST = '127.0.0.1' if local else '0.0.0.0'

    # connection = connect.connect(login_name, login_pswd, login_db)
    app.run(host=HOST, port=PORT)
