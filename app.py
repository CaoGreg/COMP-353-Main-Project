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
    if request.method == 'POST':
        application_id = request.form['application_id']
        remove_job_application(application_id)
        return applied_jobs()


@app.route('/applied_jobs')
def applied_jobs():
    #update with email once session is done
    email = 'aoyama@weeb.com'

    return render_template('applied-jobs-results.html', list_of_job_applications=get_job_applications(email))


@app.route('/user-profile', methods=['GET', 'POST'])
def user_profile():
    user_category = check_user_category()
    user_type = user_category[0][0].split(" ")[0:][0]
    print("user_type ", user_type)
    if request.method == 'POST':
        update_user_category(request.form['optradio'])
        return render_template('user-profile.html', user_type=user_type, msg="SUCCESSFULLY UPDATED YOUR USER CATEGORY")
    else:
        return render_template('user-profile.html', user_type=user_type)


@app.route('/modify_user_profile', methods=['GET', 'POST'])
def change_user_profile():
    return render_template('user-profile.html')


@app.route('/delete_user_account', methods=['POST', 'GET'])
def delete_user_account():
    # update with email once session is done
    email = 'dummy@weeb.com'
    delete_account(email)
    return redirect(url_for('index'))


@app.route('/modify_password', methods=['POST', 'GET'])
def change_user_password():
    # update with email once session is done
    email = 'aoyama@weeb.com'
    password = request.form['new_password']
    print(password)
    if password != "":
        change_password(email, password)
    return render_template('user-profile.html')


@app.route('/modify_name', methods=['POST', 'GET'])
def change_user_name():
    # update with email once session is done
    email = 'aoyama@weeb.com'
    new_name = request.form['new_name']
    if new_name != "":
        change_name(email, new_name)
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
            # or they are employer
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

