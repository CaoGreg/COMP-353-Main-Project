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


@app.route('/add_job_application', methods=['GET', 'POST'])
def add_job_application():
    usercategory = check_user_category()
    print(usercategory[0][0])

    if request.method == 'POST':
        posting_id = request.form['posting_id']
        email = request.form['email']
        if usercategory[0][0] == 'User Basic':
            return render_template('add_job_application.html', msg="YOU CANNOT APPLY TO JOBS AS A BASIC USER")
        else:
            if usercategory[0][0] == 'User Prime':
                num_of_applications = check_user_num_of_application()
                if num_of_applications[0][0] >= 5:
                    return render_template('add_job_application.html', msg="YOU CANNOT APPLY TO ANY MORE JOBS AS A PRIME USER, 5 APPLICATIONS MADE ALREADY")
                else:
                    return render_template('add_job_application.html',
                                           application_result=add_application_job(posting_id, email),
                                           msg="YOU SUCCESSFULLY APPLIED TO THE JOB")
            # else they are gold, unlimited application
            else:
                return render_template('add_job_application.html', application_result=add_application_job(posting_id, email), msg="YOU SUCCESSFULLY APPLIED TO THE JOB")
    else:
        return render_template('add_job_application.html')


@app.route('/add_job_posting', methods=['GET', 'POST'])
def add_job_posting():
    if request.method == 'POST':
        email = request.form['email']
        job_title = request.form['job_title']
        description = request.form['description']
        category = request.form['category']
        return render_template('add_job_posting.html', posting_result=add_posting_job(email, job_title, description, category))
    else:
        return render_template('add_job_posting.html')


if __name__ == "__main__":
    app.run(debug=True)

