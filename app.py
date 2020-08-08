from flask import Flask, render_template,session, abort, url_for, redirect, request
from flask_bootstrap import Bootstrap
from db_connection import *

from db_connection import *

app = Flask(__name__)
bootstrap = Bootstrap()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/postings')
def postings():
    return render_template('postings.html')


@app.route('/delete_application', methods =['GET', 'POST'])
def del_application():
    application_id = None

    if request.method == 'POST':
        application_id = request.form['application_id']
        remove_job_application(application_id)
        return applied_jobs()


@app.route('/applied_jobs', methods=['GET', 'POST'])
def applied_jobs():
    html = ""
    email = 'aoyama@weeb.com'
    open('templates/applied-jobs-results.html', 'w').close()

    file = open('templates/applied-jobs-results.html', 'w')
    html = """
    {% extends 'base.html' %}

    {% block head %}
    <style>
        h1 {text-align: center;}
    </style>
    {% endblock %}

    {% block body %}
    <div class="container">
        <h1>My Applications</h1>
        <br>
        <table class="table">
          <thead>
            <tr>
              <th scope="col">Application ID</th>
              <th scope="col">Posting ID</th>
              <th scope="col">Email</th>
              <th scope="col">Application Date</th>
              <th scope="col">Status</th>
            </tr>
          </thead>
          <tbody>
    """
    results = get_job_applications(email)

    for rows in results:
        html += "<tr>"
        for col in rows:
            html += "<td>" + str(col) + "</td>\n"
        html += "</tr>"

    html += """             
      </tbody>
    </table>
    <br>
    <h1>Remove Applications</h1>
    <br>
    <form  id="application_id_form" method="post" action="/delete_application"><div class="form-group">
      <div class="form-group">
        <input type="text" class="form-control" name="application_id" value="" placeholder="Application ID" id="application_id">
      </div>
      <div class="text-center">
      <br>
      <button type="submit" class="btn btn-success mb-2">Withdraw Application</button>
    </form>
    </div>
    {% endblock %}
    """

    file.write(html)
    file.close()
    return render_template('applied-jobs-results.html')


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    return render_template('settings.html')


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


if __name__ == "__main__":
    app.run(debug=True)

