# -*- coding: utf-8 -*-
import os
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
render_template, flash

app = Flask(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'sannyas.db'),
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))

app.config.from_envvar('SANNYAS_SETTINGS', silent=True)

def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def init_db():
    """Initializes the database."""
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    """Creates the database tables."""
    init_db()
    print('Initialized the database.')

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
            g.sqlite_db.close()

@app.route('/')
def show_names():
    db = get_db()
    cur = db.execute('select name_male, '
                     '       script_male, '
                     '       name_female, '
                     '       script_female, '
                     '       meaning, '
                     '       first_name, '
                     '       second_name, '
                     '       language, '
                     '       source, '
                     '       note, '
                     '       confirmation, '
                     '       popularity '
                     'from   names '
                     'order by id desc')
    names = cur.fetchall()
    return render_template('show_names.html', names=names)

@app.route('/add', methods=['POST'])
def add_name():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('insert into names ('
               'name_male, '
               'script_male, '
               'name_female, '
               'script_female, '
               'meaning, '
               'first_name, '
               'second_name, '
               'language, '
               'source, '
               'note, '
               'confirmation, '
               'popularity '
               ') values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
               [request.form['name_male'],
                request.form['script_male'],
                request.form['name_female'],
                request.form['script_female'],
                request.form['meaning'],
                request.form['first_name'],
                request.form['second_name'],
                request.form['language'],
                request.form['source'],
                request.form['confirmation'],
                request.form['popularity'],
                request.form['note']])
    db.commit()
    flash('New name was successfully posted')
    return redirect(url_for('show_names'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_names'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_names'))

