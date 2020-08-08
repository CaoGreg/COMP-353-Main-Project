from flask import Flask, render_template,session, abort, url_for, redirect, request
from flask_bootstrap import Bootstrap
from db_connection import *


from db_connection import search_postings

app = Flask(__name__)
bootstrap = Bootstrap()


@app.route('/')
def index():
    return render_template('index.html')



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
    title = None
    category = None
    open('templates/postings-results.html', 'w').close()

    if request.method == 'POST':
        title = request.form['title_search']
        category = request.form['category_search']

        file = open('templates/postings-results.html', 'w')
        html = """
        {% extends 'base.html' %}{% block body %}
        <div class="container"><h1>Job Search Page</h1><br><form id="job-search-engine" action="" method="post"><input type="text" placeholder="Job Title" name="title_search"><input type="text" placeholder="Category" name="category_search"><input class="btn btn-success" type="submit" value="Search"></form><br><br></div>
        <div class="container">
            <table class="table" id="posting-table">
              <thead>
                <tr>
                  <th scope="col">Posting ID</th>
                  <th scope="col">Email</th>
                  <th scope="col">Job Title</th>
                  <th scope="col">Description</th>
                  <th scope="col">Posting Date</th>
                  <th scope="col">Status</th>
                  <th scope="col">Category</th>
                </tr>
              </thead>
              <tbody>
        """
        results = search_postings(title, category)

        for rows in results:
            html += "<tr>"
            for col in rows:
                html += "<td>" + str(col) + "</td>\n"
            html += "</tr>"
        html += """
            </tbody>
        </table>
        </div>
        {% endblock %}
        """
        return render_template('postings.html', list_of_postings=search_postings(title, category))
    else:
        return render_template('postings.html', list_of_postings=search_postings("", ""))


@app.route('/jobapplication', methods=['GET', 'POST'])
def jobapplication():
    if request.method == 'POST':

        return render_template('jobapplication.html')
    else:
        return render_template('jobapplication.html')


if __name__ == "__main__":
    app.run(debug=True)

