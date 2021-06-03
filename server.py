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
    attributes = ['player_id', 'name', 'email', 'level']
    query = "SELECT * FROM player;"
    with connect(login_name, login_pswd, login_db) as connection:
        with execute_query(connection, query) as cursor:
            results = json.dumps(cursor.fetchall())
            res = json.loads(results)
            entities = [{
                'player_id': res[i]["player_id"],
                'name': res[i]["name"],
                'email': res[i]["email"],
                'level': res[i]["level"],
            } for i in range(len(res))]
            return attributes, entities


def get_players():
    attributes = ['name', 'health', 'email', 'level', 'experience', 'current_map']
    form_attributes = ['name', 'health', 'email', 'level', 'experience']
    query = "SELECT * FROM player;"
    maps = ['map_id', 'name']
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

    query = 'SELECT map_id, name from map;'
    with connect(login_name, login_pswd, login_db) as connection:
        with execute_query(connection, query) as cursor:
            results = json.dumps(cursor.fetchall())
            maps = json.loads(results)
    return attributes, entities, maps, form_attributes


def get_quests():
    attributes = ['name', 'description', 'experience_reward', 'item_reward', 'quest_giver']
    query = "SELECT * FROM quest;"
    form_attributes = ['name', 'description', 'experience_reward']
    with connect(login_name, login_pswd, login_db) as connection:
        with execute_query(connection, query) as cursor:
            results = json.dumps(cursor.fetchall())
            res = json.loads(results)
            entities = [{
                'ID': res[i]["quest_id"],
                'name': res[i]["name"],
                'description': res[i]["description"],
                'experience_reward': res[i]["experience_reward"],
                'item_reward': res[i]["item_reward"],
                'quest_giver': res[i]["quest_giver"],
            } for i in range(len(res))]

            query = 'SELECT item_id, name from item;'
            with execute_query(connection, query) as cursor:
                results = json.dumps(cursor.fetchall())
                res = json.loads(results)
                items_reward = [{
                    'item_id': "*NULL*",
                    'name': "NONE",
                }]
                for i in range(0, len(res)):
                    item = {
                        'item_id': res[i]["item_id"],
                        'name': res[i]["name"]
                    }
                    items_reward.append(item)

            query = 'SELECT npc_id, name from npc;'
            with execute_query(connection, query) as cursor:
                results = json.dumps(cursor.fetchall())
                res = json.loads(results)
                quest_giver = [{
                    'npc_id': "*NULL*",
                    'name': "NONE",
                }]
                for i in range(0, len(res)):
                    item = {
                        'npc_id': res[i]["npc_id"],
                        'name': res[i]["name"]
                    }
                    quest_giver.append(item)

            return attributes, entities, form_attributes, items_reward, quest_giver


def get_items():
    attributes = ['name', 'description', 'quality', 'sprite']
    query = "SELECT * FROM item;"
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
    attributes = ['name', 'sprite']
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
    attributes = ['name', 'description', 'faction']
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
            data = [request.form.get(a) for a in attr]
            table_token = '%s %s' % (table, tuple(attr))
            table_token = table_token.replace("'", '')

            values_token = '%s' % data
            values_token = values_token.replace("", '').replace('[', '(').replace(']', ')')
            if '' in data:
                print('empty field')
            else:
                query = "INSERT INTO %s VALUES %s;" % (table_token, values_token)
                query = query.replace("'*", '').replace("*'", '')
                with connect(login_name, login_pswd, login_db) as connection:
                    with execute_query(connection, query) as cursor:
                        pass
        elif request.form.get('query_type') == 'UPDATE':
            query = 'UPDATE %s SET %s WHERE %s=%s'
            data = json.loads(request.form.get('data'))
            set_query = ''
            first = True
            for key, val in data.items():
                if val == '': continue
                if val is None: continue
                if not first:
                    set_query += ', '
                set_query += "%s='%s'" % (key, val)
                first = False
            query = query % (table, set_query, id, request.form.get('id'))
            query = query.replace("'*", '').replace("*'", '')
            with connect(login_name, login_pswd, login_db) as connection:
                with execute_query(connection, query) as cursor:
                    pass
        elif request.form.get('query_type') == 'DELETE':
            print('delete recieved')
            query = "DELETE FROM %s WHERE %s=%s;" % (table, id, request.form.get('id'))
            print(query)
            with connect(login_name, login_pswd, login_db) as connection:
                with execute_query(connection, query) as cursor:
                    pass


def handle_many_post_request(request, table='df', attr='df'):
    if request.method == 'POST':
        print('post recieved')
        if not request.form.get('query_type'):
            data = [request.form.get(a) for a in attr]
            table_token = '%s %s' % (table, tuple(attr))
            table_token = table_token.replace("'", '')

            values_token = '%s' % data
            values_token = values_token.replace("", '').replace('[', '(').replace(']', ')')
            if '' in data:
                print('empty field')
            else:
                query = "INSERT INTO %s VALUES %s;" % (table_token, values_token)
                with connect(login_name, login_pswd, login_db) as connection:
                    with execute_query(connection, query) as cursor:
                        pass
        elif request.form.get('query_type') == 'UPDATE':
            query = 'UPDATE %s SET %s WHERE %s'
            data = json.loads(request.form.get('data'))
            ids = request.form.get('id').split("&")
            set_query = ''
            first = True
            for key, val in data.items():
                if val == '': continue
                if val is None: continue
                if not first:
                    set_query += ', '
                set_query += "%s='%s'" % (key, val)
                first = False

            where_query = ''
            first = True
            index = 0
            for key, val in data.items():
                if not first:
                    where_query += ' AND '
                where_query += "%s.%s= %s" % (table, key, ids[index])
                index += 1
                first = False

            query = query % (table, set_query, where_query)
            with connect(login_name, login_pswd, login_db) as connection:
                with execute_query(connection, query) as cursor:
                    pass
        elif request.form.get('query_type') == 'DELETE':
            print('delete recieved')
            ids = request.form.get('id').split("&")
            where_query = ''
            first = True
            index = 0
            for key in attr:
                if not first:
                    where_query += ' AND '
                where_query += "%s.%s= %s" % (table, key, ids[index])
                index += 1
                first = False
            query = "DELETE FROM %s WHERE %s;" % (table, where_query)
            print(query)
            with connect(login_name, login_pswd, login_db) as connection:
                with execute_query(connection, query) as cursor:
                    pass


def handle_order_by_request(request):
    attributes = ['player_id', 'name', 'email', 'level']
    query = "SELECT p1.* FROM player AS p1 " \
            "LEFT JOIN (SELECT * FROM player GROUP BY player.player_id) " \
            "as p2 ON p1.player_id = p2.player_id " \
            "order by p1.%s;" % (request.form.get('type'))
    print(query)
    with connect(login_name, login_pswd, login_db) as connection:
        with execute_query(connection, query) as cursor:
            results = json.dumps(cursor.fetchall())
            res = json.loads(results)
            entities = [{
                'player_id': res[i]["player_id"],
                'name': res[i]["name"],
                'email': res[i]["email"],
                'level': res[i]["level"],
            } for i in range(len(res))]
        return attributes, entities


def find_name(list, id, id_name):
    for i in range(len(list)):
        if list[i][id_name] == id:
            return list[i]['name']
    return None


@app.route('/players', methods=['GET', 'POST'])
def players():
    attributes, entities, map_results, form_attributes = get_players()

    handle_post_request(request, table='player', attr=attributes, id='player_id')

    attributes, entities, map_results, form_attributes = get_players()

    return render_template('players.html', title='Players', attributes=attributes, results=entities,
                           form_attributes=form_attributes, maps=map_results)


@app.route('/quests', methods=['GET', 'POST'])
def quests():
    attributes, entities, form_attributes, q_items, q_npcs = get_quests()

    handle_post_request(request, table='quest', attr=attributes, id='quest_id')

    attributes, entities, form_attributes, q_items, q_npcs = get_quests()

    return render_template('quests.html', title='Quests', attributes=attributes, results=entities,
                           form_attributes=form_attributes, q_items=q_items, q_npcs=q_npcs)


@app.route('/items', methods=['GET', 'POST'])
def items():
    attributes, entities = get_items()
    handle_post_request(request, table='item', attr=attributes, id='item_id')
    attributes, entities = get_items()
    return render_template('table_page.html', title='Items', attributes=attributes, results=get_items()[1],
                           form_attributes=attributes)


@app.route('/npcs', methods=['GET', 'POST'])
def npcs():
    attributes, entities = get_npcs()
    handle_post_request(request, table='npc', attr=attributes, id='npc_id')
    attributes, entities = get_npcs()
    return render_template('table_page.html', title='NPCs', attributes=attributes, results=entities,
                           form_attributes=attributes)


@app.route('/maps', methods=['GET', 'POST'])
def maps():
    attributes, entities = get_maps()
    handle_post_request(request, table='map', attr=attributes, id='map_id')
    attributes, entities = get_maps()
    return render_template('table_page.html', title='Maps', attributes=attributes, results=entities,
                           form_attributes=attributes)


@app.route('/player_inventory', methods=['GET', 'POST'])
def player_inventory():
    attributes = ['player_id', 'item_id']
    names = ['name1', 'name2']

    handle_many_post_request(request, table="player_inventory", attr=attributes)

    query = "SELECT * FROM player_inventory;"
    with connect(login_name, login_pswd, login_db) as connection:
        with execute_query(connection, query) as cursor:
            query = 'SELECT player_id, name from player;'
            with execute_query(connection, query) as cursor:
                results = json.dumps(cursor.fetchall())
                players = json.loads(results)
            query = 'SELECT item_id, name from item;'
            with execute_query(connection, query) as cursor:
                results = json.dumps(cursor.fetchall())
                items = json.loads(results)
            query = "SELECT * FROM player_inventory;"
            with execute_query(connection, query) as cursor:
                results = json.dumps(cursor.fetchall())
                res = json.loads(results)
            entities = [{'player_id': res[i]["player_id"],
                         'item_id': res[i]["item_id"],
                         'name1': find_name(players, res[i]["player_id"], "player_id"),
                         'name2': find_name(items, res[i]["item_id"], "item_id")
                         } for i in range(len(res))]

    return render_template('m:m_page.html', title='Player Inventory', attributes=attributes, results=entities,
                           form_attributes=attributes, names=names, list1=players, list2=items)


@app.route('/player_quests', methods=['GET', 'POST'])
def player_quests():
    attributes = ['player_id', 'quest_id']
    names = ['name1', 'name2']

    handle_many_post_request(request, table="player_active_quests", attr=attributes)

    query = "SELECT * FROM player_active_quests;"
    with connect(login_name, login_pswd, login_db) as connection:
        with execute_query(connection, query) as cursor:
            query = 'SELECT player_id, name from player;'
            with execute_query(connection, query) as cursor:
                results = json.dumps(cursor.fetchall())
                players = json.loads(results)
            query = 'SELECT quest_id, name from quest;'
            with execute_query(connection, query) as cursor:
                results = json.dumps(cursor.fetchall())
                quests = json.loads(results)
            query = "SELECT * FROM player_active_quests;"
            with execute_query(connection, query) as cursor:
                results = json.dumps(cursor.fetchall())
                res = json.loads(results)
            entities = [{'player_id': res[i]["player_id"],
                         'quest_id': res[i]["quest_id"],
                         'name1': find_name(players, res[i]["player_id"], "player_id"),
                         'name2': find_name(quests, res[i]["quest_id"], "quest_id")
                         } for i in range(len(res))]

    return render_template('m:m_page.html', title='Player Quests', attributes=attributes, results=entities,
                           list1=players, list2=quests, names=names)


@app.route('/npc_droptable', methods=['GET', 'POST'])
def npc_droptable():
    attributes = ['npc_id', 'item_id']
    names = ['name1', 'name2']

    handle_many_post_request(request, table="npc_drop_table", attr=attributes)

    query = "SELECT * FROM npc_drop_table;"
    with connect(login_name, login_pswd, login_db) as connection:
        with execute_query(connection, query) as cursor:
            query = 'SELECT npc_id, name from npc;'
            with execute_query(connection, query) as cursor:
                results = json.dumps(cursor.fetchall())
                npcs = json.loads(results)
            query = 'SELECT item_id, name from item;'
            with execute_query(connection, query) as cursor:
                results = json.dumps(cursor.fetchall())
                items = json.loads(results)
            query = "SELECT * FROM npc_drop_table;"
            with execute_query(connection, query) as cursor:
                results = json.dumps(cursor.fetchall())
                res = json.loads(results)
            entities = [{'npc_id': res[i]["npc_id"],
                         'item_id': res[i]["item_id"],
                         'name1': find_name(npcs, res[i]["npc_id"], "npc_id"),
                         'name2': find_name(items, res[i]["item_id"], "item_id")
                         } for i in range(len(res))]

    return render_template('m:m_page.html', title='NPC Drop Table', attributes=attributes, results=entities,
                           list1=npcs, list2=items, names=names)


@app.route('/npc_spawned', methods=['GET', 'POST'])
def npc_spawned():
    attributes = ['npc_id', 'map_id']
    names = ['name1', 'name2']

    handle_many_post_request(request, table="spawned_npc", attr=attributes)

    query = "SELECT * FROM spawned_npc;"
    with connect(login_name, login_pswd, login_db) as connection:
        with execute_query(connection, query) as cursor:
            query = 'SELECT npc_id, name from npc;'
            with execute_query(connection, query) as cursor:
                results = json.dumps(cursor.fetchall())
                npcs = json.loads(results)
            query = 'SELECT map_id, name from map;'
            with execute_query(connection, query) as cursor:
                results = json.dumps(cursor.fetchall())
                maps = json.loads(results)
            query = "SELECT * FROM spawned_npc;"
            with execute_query(connection, query) as cursor:
                results = json.dumps(cursor.fetchall())
                res = json.loads(results)
            entities = [{'npc_id': res[i]["npc_id"],
                         'map_id': res[i]["map_id"],
                         'name1': find_name(npcs, res[i]["npc_id"], "npc_id"),
                         'name2': find_name(maps, res[i]["map_id"], "map_id")
                         } for i in range(len(res))]

    return render_template('m:m_page.html', title='Spawned NPCs', attributes=attributes, results=entities,
                           list1=npcs, list2=maps, names=names)


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
@app.route('/homepage', methods=['GET', 'POST'])
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST' and request.form.get('type'):
        attributes, entities = handle_order_by_request(request)
    else:
        attributes, entities = get_entities()
    return render_template('homepage.html', attributes=attributes, results=entities)


if __name__ == '__main__':
    local = bool(os.environ.get('LOCAL', True))

    PORT = int(os.environ.get('PORT', 18300))
    HOST = '127.0.0.1' if local else '0.0.0.0'
    app.run(host=HOST, port=PORT)
