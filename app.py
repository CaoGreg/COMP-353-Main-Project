from flask import Flask, render_template, session, abort, url_for, redirect, request, flash
from flask_bootstrap import Bootstrap
from db_connection import *

app = Flask(__name__)
bootstrap = Bootstrap()


@app.route('/')
def index():
    return render_template('index.html')



@app.route('/delete_application', methods=['GET', 'POST'])
def del_application():
    application_id = None

    if request.method == 'POST':
        application_id = request.form['application_id']
        remove_job_application(application_id)
        return applied_jobs()


@app.route('/applied_jobs', methods=['GET', 'POST'])
def applied_jobs():
    email = 'aoyama@weeb.com'

    return render_template('applied-jobs-results.html', list_of_job_applications=get_job_applications(email))


@app.route('/user-profile', methods=['GET', 'POST'])
def settings():
    return render_template('user-profile.html')


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


@app.route('/users')
def users():
    return render_template('users.html', list_of_users=get_all_users())


@app.route('/postings', methods=['GET', 'POST'])
def postings():
    title = ""
    category = ""
    if request.method == 'POST':
        title = request.form['title_search']
        category = request.form['category_search']
    return render_template('postings.html', list_of_postings=search_postings(title, category))


@app.route('/jobapplication', methods=['GET', 'POST'])
def jobapplication():
    if request.method == 'POST':
        posting_id = request.form['posting_id']
        email = request.form['email']
        return render_template('jobapplication.html', application_result=application_job(posting_id, email))
    else:
        return render_template('jobapplication.html')


if __name__ == "__main__":
    app.run(debug=True)

