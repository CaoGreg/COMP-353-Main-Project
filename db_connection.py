from dotenv import load_dotenv
from flask import session
from sshtunnel import SSHTunnelForwarder
from datetime import date
import pymysql
import os

load_dotenv()
encs_user = os.getenv("ENCS_USR")
encs_password = os.getenv("ENCS_PWD")
db_user = os.getenv("DB_USR")
db_password = os.getenv("DB_PWD")
db_host = 'oxc353.encs.concordia.ca'
server = SSHTunnelForwarder(
    ('login.encs.concordia.ca', 22),
    ssh_username=encs_user,
    ssh_password=encs_password,
    remote_bind_address=(db_host, 3306))

server.start()

db_connection = pymysql.connect(
    host='localhost', port=server.local_bind_port, db='oxc353_1', user=db_user,
    password=db_password, charset='utf8mb4')


def register_user(email, password, name, user_type):
    is_active = 1
    is_admin = 0
    cursor = db_connection.cursor()
    cursor.execute("USE oxc353_1")
    cursor.execute("""INSERT INTO MP_User(email, password, name, is_active, user_type, is_admin)
                VALUES(%s, %s, %s, %s, %s, %s)""",
                   (email, password, name, is_active, user_type, is_admin))
    cursor.execute("""INSERT INTO MP_User_balance(email, balance, is_suffering)
                VALUES(%s, 0.00, 0)""",
                   (email))
    if user_type == 'Employee':
        cursor.execute("""INSERT INTO MP_Subscribed_to(email, category)
                VALUES(%s, %s)""",
                       (email, 'User Basic' ))
    else:
        cursor.execute("""INSERT INTO MP_Subscribed_to(email, category)
                VALUES(%s, %s)""",
                       (email, 'Employer Prime'))
    cursor.close()
    db_connection.commit()
    return

def register_employer(email,phone):
    cursor = db_connection.cursor()
    cursor.execute("USE oxc353_1")
    cursor.execute("""INSERT INTO MP_Employer(email, phone)
                VALUES(%s, %s)""",
                   (email, phone))
    cursor.close()
    db_connection.commit()
    return

def get_login(email, password):
    cursor = db_connection.cursor()
    cursor.execute("USE oxc353_1")
    cursor.execute('SELECT * FROM MP_User WHERE email = %s AND password = %s',
                   (email, password,))
    account = cursor.fetchone()
    cursor.close()
    return account


def get_forgotten(email, name):
    print(str(email) + " " + str(name))
    cursor = db_connection.cursor()
    cursor.execute("USE oxc353_1")
    cursor.execute('SELECT password FROM MP_User WHERE email = %s AND name = %s',
                   (email, name,))
    password = cursor.fetchone()
    cursor.close()
    print(password)
    return password


def get_all_users(active_only):
    query = "SELECT email, name, is_active, user_type, is_admin FROM MP_User"
    if active_only:
        query += " WHERE MP_User.is_active = 1;"
    cursor = db_connection.cursor()
    cursor.execute("USE oxc353_1")
    print(query)
    cursor.execute(query)
    data = []
    for row in cursor:
        data.append(row)
    cursor.close()
    return data


def get_job_applications(email):
    query = "SELECT * FROM MP_Job_application " \
            "WHERE MP_Job_application.email = '" + email + "';"
    cursor = db_connection.cursor()
    cursor.execute("USE oxc353_1")
    cursor.execute(query)
    data = []
    for row in cursor:
        data.append(row)
    cursor.close()
    return data


def get_applications_by_posting(posting_id):
    query = "SELECT * FROM MP_Job_application WHERE posting_id=%s"
    cursor = db_connection.cursor()
    cursor.execute("USE oxc353_1")
    cursor.execute(query, posting_id)
    data = []
    for row in cursor:
        print(row)
        data.append(row)
    cursor.close()
    return data


def get_job_postings(user_id):
    query = "SELECT * FROM MP_Job_posting " \
            "WHERE MP_Job_posting.email = '" + user_id + "';"
    cursor = db_connection.cursor()
    cursor.execute("USE oxc353_1")
    cursor.execute(query)
    data = []
    for row in cursor:
        data.append(row)
    cursor.close()
    return data


def search_postings(title, category):
    data = []
    cursor = db_connection.cursor()
    cursor.execute("USE oxc353_1")
    query = "SELECT * FROM MP_Job_posting " \
            "WHERE job_title LIKE '% " + title + "%' " \
            "AND category LIKE '%" + category+"%';"
    cursor.execute(query)
    for row in cursor:
        data.append(row)
    cursor.close()
    return data


def get_postings():
    data = []
    cursor = db_connection.cursor()
    cursor.execute("USE oxc353_1")
    query = "SELECT posting_id,MP_Job_posting.email,job_title,description,posting_date,status,category,phone " \
            "FROM MP_Job_posting,MP_Employer " \
            "WHERE MP_Job_posting.email = MP_Employer.email;"
    cursor.execute(query)
    for row in cursor:
        data.append(row)
    cursor.close()
    return data


def remove_job_application(application_id):
    query = "DELETE FROM MP_Job_application "\
            "WHERE MP_Job_application.application_id = " + application_id + ";"
    cursor = db_connection.cursor()
    cursor.execute("USE oxc353_1")
    cursor.execute(query)
    cursor.close()
    db_connection.commit()
    return


def modify_job_posting(posting_id, job_title, description, category):
    query = "UPDATE MP_Job_posting SET job_title=%s, description=%s, category=%s WHERE posting_id=%s"
    cursor = db_connection.cursor()
    cursor.execute("USE oxc353_1")
    cursor.execute(query, (job_title, description, category, posting_id))
    cursor.close()
    db_connection.commit()
    return


def remove_job_posting(posting_id):
    query = "DELETE FROM MP_Job_posting "\
            "WHERE MP_Job_posting.posting_id = " + posting_id + ";"
    cursor = db_connection.cursor()
    cursor.execute("USE oxc353_1")
    cursor.execute(query)
    cursor.close()
    db_connection.commit()
    return


def set_posting_active(posting_id):
    query = "UPDATE MP_Job_posting SET status=%s WHERE posting_id=%s"
    cursor = db_connection.cursor()
    cursor.execute("USE oxc353_1")
    cursor.execute(query, ('active', posting_id))
    cursor.close()
    db_connection.commit()
    return


def set_posting_inactive(posting_id):
    query = "UPDATE MP_Job_posting SET status=%s WHERE posting_id=%s"
    cursor = db_connection.cursor()
    cursor.execute("USE oxc353_1")
    cursor.execute(query, ('inactive', posting_id))
    cursor.close()
    db_connection.commit()
    return


def accept_job_application(application_id):
    query = "UPDATE MP_Job_application SET status=%s WHERE application_id=%s"
    cursor = db_connection.cursor()
    cursor.execute("USE oxc353_1")
    cursor.execute(query, ('accepted', application_id))
    cursor.close()
    db_connection.commit()
    return


def reject_job_application(application_id):
    query = "UPDATE MP_Job_application SET status=%s WHERE application_id=%s"
    cursor = db_connection.cursor()
    cursor.execute("USE oxc353_1")
    cursor.execute(query, ('rejected', application_id))
    cursor.close()
    db_connection.commit()
    return


def add_application_job(posting_id, email):
    data = []
    today = date.today()
    cursor = db_connection.cursor()
    cursor.execute("USE oxc353_1")
    cursor.execute("""INSERT INTO MP_Job_application(posting_id, email, application_date, status)
                VALUES(%s, %s, %s, %s)""",
                (posting_id, email, today.strftime("%Y-%m-%d"), 'pending'))
    for row in cursor:
        data.append(row)
        print(row)
    cursor.close()
    db_connection.commit()
    return data


def change_password(email, new_password):
    query = "UPDATE MP_User SET MP_User.password='" + new_password + "'"\
            "WHERE MP_User.email='" + email + "';"
    cursor = db_connection.cursor()
    cursor.execute("USE oxc353_1")
    cursor.execute(query)
    cursor.close()
    db_connection.commit()
    return


def change_name(email, new_name):
    query = "UPDATE MP_User SET MP_User.name='" + new_name + "'"\
            "WHERE MP_User.email='" + email + "';"
    cursor = db_connection.cursor()
    cursor.execute("USE oxc353_1")
    cursor.execute(query)
    cursor.close()
    db_connection.commit()
    return


def delete_account(email):
    mp_user_query = "DELETE FROM MP_User "\
                    "WHERE MP_User.email='" + email + "';"
    mp_bill_query = "DELETE FROM MP_Bill " \
                    "WHERE MP_Bill.email='" + email + "';"
    mp_job_application_query = "DELETE FROM MP_Job_application " \
                               "WHERE MP_Job_application.email='" + email + "';"
    mp_job_offer_query = "DELETE FROM MP_Job_offer " \
                         "WHERE MP_Job_offer.email='" + email + "';"
    mp_paid_using_query = "DELETE FROM MP_Paid_using " \
                          "WHERE MP_Paid_using.email='" + email + "';"
    mp_sub_to_query = "DELETE FROM MP_Subscribed_to " \
                      "WHERE MP_Subscribed_to.email='" + email + "';"
    mp_user_balance_query = "DELETE FROM MP_User_balance " \
                            "WHERE MP_User_balance.email='" + email + "';"

    cursor = db_connection.cursor()
    cursor.execute("USE oxc353_1")
    cursor.execute(mp_bill_query)
    cursor.execute(mp_job_application_query)
    cursor.execute(mp_job_offer_query)
    cursor.execute(mp_paid_using_query)
    cursor.execute(mp_sub_to_query)
    cursor.execute(mp_user_balance_query)
    cursor.execute(mp_user_query)
    cursor.close()
    db_connection.commit()
    return
  
  
def add_posting_job(email, job_title, description, category):
    data = []
    today = date.today()
    cursor = db_connection.cursor()
    cursor.execute("USE oxc353_1")
    cursor.execute("""INSERT INTO MP_Job_posting(email, job_title, description, posting_date, status, category)
                VALUES(%s, %s, %s, %s, %s, %s)""",
                (email, job_title, description, today.strftime("%Y-%m-%d"), 'active', category))
    for row in cursor:
        data.append(row)
        print(row)
    cursor.close()
    db_connection.commit()
    return data


def check_user_category():
    data = []
    today = date.today()
    email = session['email']
    cursor = db_connection.cursor()
    cursor.execute("USE oxc353_1")
    cursor.execute("""SELECT category FROM MP_Subscribed_to
    WHERE email = %s
    """,
        (email))
    for row in cursor:
        data.append(row)
    cursor.close()
    db_connection.commit()
    return data


def check_user_num_of_application():
    data = []
    today = date.today()
    email = session['email']
    cursor = db_connection.cursor()
    cursor.execute("USE oxc353_1")
    cursor.execute("""SELECT COUNT(*) FROM MP_Job_application
    WHERE email = %s
    """, email)
    for row in cursor:
        data.append(row)
    cursor.close()
    db_connection.commit()
    return data


def check_employer_num_of_posting():
    data = []
    today = date.today()
    email = session['email']
    cursor = db_connection.cursor()
    cursor.execute("USE oxc353_1")
    cursor.execute("""SELECT COUNT(*) FROM MP_Job_posting
    WHERE email = %s
    """, email)
    for row in cursor:
        data.append(row)
    cursor.close()
    db_connection.commit()
    return data


def update_user_category(new_category):
    data = []
    today = date.today()
    email = session['email']
    cursor = db_connection.cursor()
    cursor.execute("USE oxc353_1")
    cursor.execute("""UPDATE MP_Subscribed_to
    SET category = %s
    WHERE email = %s
    """,
        (new_category, email))
    for row in cursor:
        data.append(row)
    cursor.close()
    db_connection.commit()
    return data


def activate_user(email, is_active):
    query = "UPDATE MP_User SET MP_User.is_active=" + is_active + " "\
            "WHERE MP_User.email='" + email + "';"
    cursor = db_connection.cursor()
    cursor.execute("USE oxc353_1")
    cursor.execute(query)
    cursor.close()
    db_connection.commit()
    return


def get_frozen(email):
    query = "SELECT * FROM MP_User_balance " \
            "WHERE MP_User_balance.email='" + email + "';"
    cursor = db_connection.cursor()
    cursor.execute("USE oxc353_1")
    cursor.execute(query)
    is_suffering = cursor.fetchone()
    cursor.close()
    return is_suffering


def get_payment():
    data = []
    query = "SELECT MP_Payment_type.payment_number,payment_type,withdrawal_type FROM MP_Paid_using, MP_Payment_type "\
            "WHERE MP_Paid_using.payment_number = MP_Payment_type.payment_number and email = '" + session['email'] + "';"
    cursor = db_connection.cursor()
    cursor.execute("USE oxc353_1")
    cursor.execute(query)
    for row in cursor:
        data.append(row)
    cursor.close()
    cursor.close()
    return data


def remove_payment_method(payment_id):
    query1 = "DELETE FROM MP_Paid_using WHERE payment_number = '" + payment_id + "';"
    query2 = "DELETE FROM MP_Payment_type WHERE payment_number = '" + payment_id + "';"
    cursor = db_connection.cursor()
    cursor.execute("USE oxc353_1")
    cursor.execute(query1)
    cursor.execute(query2)
    cursor.close()
    db_connection.commit()
    return


def insert_payment_method(payment_number, payment_type, withdrawal_type):
    query1 = "INSERT INTO MP_Payment_type(payment_number, payment_type, withdrawal_type) VALUES "\
             "('" + payment_number + "', '" + payment_type + "', '" + withdrawal_type + "');"
    query2 = "INSERT INTO MP_Paid_using(email, payment_number) VALUES "\
             "('" + payment_number + "', '" + session['email'] + "');"
    cursor = db_connection.cursor()
    cursor.execute("USE oxc353_1")
    cursor.execute(query1)
    cursor.execute(query2)
    cursor.close()
    db_connection.commit()
    return
