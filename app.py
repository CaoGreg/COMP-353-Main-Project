from flask import Flask, render_template,session, abort, url_for, redirect, request
from flask_bootstrap import Bootstrap
import sshtunnel
from dotenv import load_dotenv
from sshtunnel import SSHTunnelForwarder
import pymysql
import os

from db_connection import search_postings

app = Flask(__name__)
bootstrap = Bootstrap()

# sshtunnel.SSH_TIMEOUT = 45

# tunnel = SSHTunnelForwarder(
#     ('login.encs.concordia.ca', 22),
#     ssh_username='', 
#     ssh_password='',
#     remote_bind_address=('oxc353.encs.concordia.ca', 3306) ) 
# tunnel.start()

# # change to name of your database; add path if necessary


# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
#     username="",
#     password="",
#     hostname="oxc353.encs.concordia.ca",
#     databasename="oxc353_1",
# )
# app.config["SQLALCHEMY_POOL_RECYCLE"] = 2997
# app.config['SQLALCHEMY_POOL_TIMEOUT'] = 60
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# engine = create_engine("mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
#     username="oxc353_1",
#     password="bobatea1",
#     hostname="oxc353.encs.concordia.ca",
#     databasename="oxc353_1",
# ))

# this variable, db, will be used for all SQLAlchemy commands
# db = SQLAlchemy(app)

# user = db.Table('MP_User', db.metadata, autoload=True, autoload_with=db.engine)

@app.route('/')
def index():
    # db = SQLAlchemy(app)
    # results = db.session.query(user).all()
    # for r in results: 
    #     print(r.name)
    return render_template('index.html')


@app.route('/postings', methods=['GET', 'POST'])
def postings():
    title = None
    category = None

    if request.method == 'POST':
        title = request.form['title_search']
        category = request.form['category_search']
        postings = search_postings(title, category)
    # for rows in postings:

    return render_template('postings.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('index'))

    return render_template('login.html', error=error)

@app.route('/registration', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('index'))
    return render_template('registration.html', error=error)

if __name__ == "__main__":
    app.run(debug=True)

