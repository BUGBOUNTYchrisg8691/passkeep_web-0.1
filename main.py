#!/bin/env python3

# sample password manager written in python utilizing a mysql database;


from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import os


app = Flask(__name__)

app.secret_key = os.environ.get('APP_KEY')

app.config['MYSQL_HOST'] = os.environ.get('SQL_HOST')
app.config['MYSQL_USER'] = os.environ.get('SQL_USER')
app.config['MYSQL_PASSWORD'] = os.environ.get('SQL_PASS')
app.config['MYSQL_DB'] = os.environ.get('SQL_DB')

# set these if you dont want to use env variables
#app.secret_key = ''

#app.config['MYSQL_HOST'] = ''
#app.config['MYSQL_USER'] = ''
#app.config['MYSQL_PASSWORD'] = ''
#app.config['MYSQL_DB'] = ''

mysql = MySQL(app)

@app.route('/passkeep_sql/', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s;', (username, password,))

        account = cursor.fetchone()

        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            return redirect(url_for('home'))
        else:
            msg = 'Incorrect username/password'

    return render_template('index.html', msg='')

@app.route('/passkeep_sql/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)

    return redirect(url_for('login'))

@app.route('/passkeep_sql/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and \
        'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s;', (username,))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only alphanumeric characters!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s);', (username, password, email,))
            mysql.connection.commit()
            msg = 'You have successfully registered!'

    elif request.method == 'POST':
        msg = 'Please fill out the form!'

    return render_template('register.html', msg=msg)

@app.route('/passkeep_sql/home')
def home():
    if 'loggedin' in session:
        return render_template('home.html', username=session['username'])

    return redirect(url_for('login'))

@app.route('/passkeep_sql/profile')
def profile():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
        account = cursor.fetchone()

        return render_template('profile.html', account=account)

    return redirect(url_for('login'))

@app.route('/passkeep_sql/add_entry', methods=['GET', 'POST'])
def add_entry():
    msg = ''
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
        account = cursor.fetchone()

        if request.method == 'POST' and 'service' in request.form and 'username' in request.form and \
            'password' in request.form:
            service = request.form['service']
            username = request.form['username']
            password = request.form['password']

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT id, service, username, password FROM entries WHERE account_id = %s;',
                           (account['id'],))
            entries = cursor.fetchall()
            for entry in entries:
                print(entry)

            if any(service in entry for entry in entries):
                msg = 'Entry already exists!'
            else:
                cursor.execute('INSERT INTO entries VALUES (NULL, %s, %s, %s, %s);', (account['id'], service, username,
                                                                                      password,))
                mysql.connection.commit()
                msg = 'Your entry was successfully saved!'

        elif request.method == 'POST':
            msg = 'Please fill out the form!'

    return render_template('add_entry.html', msg=msg, account=account)

@app.route('/passkeep_sql/find_entry')
def find_entry():
    msg = ''
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
        account = cursor.fetchone()

    return render_template('add_entry.html', msg=msg, account=account)