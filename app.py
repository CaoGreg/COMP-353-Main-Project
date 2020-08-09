from flask import Flask, flash, render_template,session, abort, url_for, redirect, request, session
from flask_bootstrap import Bootstrap

from db_connection import *

app = Flask(__name__)
bootstrap = Bootstrap()


@app.route('/')
def postings():
    title = ""
    category = ""
    if request.method == 'POST':
        title = request.form['title_search']
        category = request.form['category_search']
        return render_template('postings.html', list_of_postings=search_postings(title, category), is_search='true')
    else:
        return render_template('postings.html', list_of_postings=get_postings(), is_search='false')


@app.route('/delete_application/<application_id>', methods=['GET', 'POST'])
def delete_application(application_id):
    if request.method == 'POST':
        remove_job_application(application_id)
        file = open("log.txt", "a")
        file.write("\n" + str(date.today()) + " Job application removed: " + session['email'] + ", Application: " + application_id)
        file.close()
        return redirect('/applied_jobs')


@app.route('/applied_jobs')
def applied_jobs():
    email = session['email']
    return render_template('applied-jobs-results.html', list_of_job_applications=get_job_applications(email))


@app.route('/employer_postings')
def employer_postings():
    email = session['email']
    return render_template('employer-postings.html', list_of_job_postings=get_job_postings(email))


@app.route('/modify_posting/<posting_id>', methods=['GET', 'POST'])
def modify_posting(posting_id):
    if request.method == 'POST':
        job_title = request.form['job_title']
        description = request.form['description']
        category = request.form['category']
        modify_job_posting(posting_id, job_title, description, category)
        file = open("log.txt", "a")
        file.write("\n" + str(date.today()) + " Posting Modified: " + session['email'] + ", Posting: " + posting_id + ", " + job_title + ", " + description + ", " + category)
        file.close()
        return redirect('/employer_postings')
    else:
        return render_template('modify_posting.html')


@app.route('/delete_posting/<posting_id>', methods=['GET', 'POST'])
def delete_posting(posting_id):
    if request.method == 'POST':
        remove_job_posting(posting_id)
        file = open("log.txt", "a")
        file.write("\n" + str(date.today()) + " Posting Removed: " + session['email'] + ", Posting ID: " + posting_id)
        file.close()
        return redirect('/employer_postings')


@app.route('/set_active/<posting_id>', methods=['GET', 'POST'])
def set_active(posting_id):
    if request.method == 'POST':
        set_posting_active(posting_id)
        file = open("log.txt", "a")
        file.write("\n" + str(date.today()) + " Posting status change to active: " + session['email'] + ", Posting: " + posting_id)
        file.close()
        return redirect('/employer_postings')


@app.route('/set_inactive/<posting_id>', methods=['GET', 'POST'])
def set_inactive(posting_id):
    if request.method == 'POST':
        set_posting_inactive(posting_id)
        file = open("log.txt", "a")
        file.write("\n" + str(date.today()) + " Posting status change to inactive: " + session['email'] + ", Posting: " + posting_id)
        file.close()
        return redirect('/employer_postings')


@app.route('/view_applications/<posting_id>', methods=['GET', 'POST'])
def view_applications(posting_id):
    return render_template('view-applications.html', list_of_applications=get_applications_by_posting(posting_id))


@app.route('/accept_application/<posting_id>/<application_id>', methods=['GET', 'POST'])
def accept_application(posting_id, application_id):
    if request.method == 'POST':
        accept_job_application(application_id)
        return redirect('/view_applications/' + str(posting_id))


@app.route('/reject_application/<posting_id>/<application_id>', methods=['GET', 'POST'])
def reject_application(posting_id, application_id):
    if request.method == 'POST':
        reject_job_application(application_id)
        return redirect('/view_applications/' + str(posting_id))


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
    email = session['email']
    delete_account(email)
    file = open("log.txt", "a")
    file.write("\n" + str(date.today()) + " User deleted: " + session['email'] + ", " + session['user_type'])
    file.close()
    return redirect(url_for('postings'))


@app.route('/modify_password', methods=['POST', 'GET'])
def change_user_password():
    email = session['email']
    password = request.form['new_password']
    print(password)
    if password != "":
        change_password(email, password)
        file = open("log.txt", "a")
        file.write("\n" + str(date.today()) + " User password changed: " + session['email'])
        file.close()
    return render_template('user-profile.html')


@app.route('/modify_name', methods=['POST', 'GET'])
def change_user_name():
    email = session['email']
    new_name = request.form['new_name']
    if new_name != "":
        change_name(email, new_name)
        file = open("log.txt", "a")
        file.write("\n" + str(date.today()) + " User name changed: " + session['email'] + ", " + new_name)
        file.close()
    return render_template('user-profile.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    # form fields
    if request.method == 'POST':

        email = request.form['username']
        password = request.form['password']
        account = get_login(email, password)
        is_frozen = get_frozen(email)

        if account:
            if account[4] == 0:
                error = 'Your account is deactivated. Please contact a system administrator'
                return render_template('login.html', error=error)

            session['logged_In'] = True
            session['userID'] = account[0]
            session['email'] = account[1]
            session['user_type'] = account[5]
            session['is_admin'] = account[6]
            session['is_suffering'] = is_frozen[2]
            flash('logged in successfully')

            file = open("log.txt", "a")
            file.write("\n" + str(date.today()) + " User logged in: " + session['email'] + ", " + session['user_type'])
            file.close()
            return redirect(url_for('postings'))
        else:
            error = 'Invalid Credentials. Please try again.'
    return render_template('login.html', error=error)


@app.route('/forgot', methods=['GET', 'POST'])
def forgot_password():
    error = None
    # form fields
    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        password = get_forgotten(email, name)
        flash('password is: ' + str(password[0]))
    else:
        error = 'Invalid Credentials. Please try again.'
    return render_template('forgot.html', error=error)


@app.route('/registration', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        user_type = request.form['user_type']
        account = get_login(email, password)
        if account:
            flash('email' + str(account[1]) + 'already registered')
        else:
            register_user(email, password, name, user_type)
            file = open("log.txt", "a")
            file.write("\n" + str(date.today()) + " New User added: " + name + ", " + email + ", " + user_type)
            file.close()
            return render_template('registration.html', msg="USER CREATION SUCCESS")
    return render_template('registration.html', error=error)


@app.route('/users')
def users():
    return render_template('users.html', list_of_users=get_all_users(active_only=True))


@app.route('/logout')
def logout():
    file = open("log.txt", "a")
    file.write("\n" + str(date.today()) + " User signed out: " + session['email'])
    file.close()
    session.pop('userID', None)
    session.pop('email', None)
    session.pop('logged_In', None)
    flash('You are logged out.')
    session['logged_In'] = False
    return redirect('/')


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
                    file = open("log.txt", "a")
                    file.write("\n" + str(date.today()) + " New job application: " + session['email'] + ", Posting: " + posting_id)
                    file.close()
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
        email = session['email']
        job_title = request.form['job_title']
        description = request.form['description']
        category = request.form['category']
        add_posting_job(email, job_title, description, category)
        file = open("log.txt", "a")
        file.write("\n" + str(date.today()) + " New job Posting: " + email + ", Posting: " + job_title + ", " + description + ", " + category)
        file.close()
        return redirect('/employer_postings')
    else:
        return render_template('add_job_posting.html')


@app.route('/activate_user', methods=['GET', 'POST'])
def admin_activate_user():
    if request.method == 'POST':
        email = request.form['email']
        is_active = request.form['is_active']
        activate_user(email, is_active)

        if is_active == "1":
            status = "active"
        else:
            status = "inactive"
        file = open("log.txt", "a")
        file.write("\n" + str(date.today()) + session['email'] + " updated user: " + "Email: " + email + ", Status: " + status)
        file.close()
    return render_template('admin-activate-user.html', list_of_users=get_all_users(False))


@app.route('/system_activity')
def show_system_activity():
    with open('log.txt', 'r') as file:
        logs = file.read()
    return render_template('admin-system-history.html', log=logs)


if __name__ == "__main__":
    app.secret_key = 'secret123'
    app.run(debug=True)

