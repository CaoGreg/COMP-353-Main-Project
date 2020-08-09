from dotenv import load_dotenv
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


def get_all_users():
    cursor = db_connection.cursor()
    cursor.execute("USE oxc353_1")
    cursor.execute("SELECT email, name, is_active, user_type, is_admin FROM MP_User")
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


def remove_job_application(application_id):
    query = "DELETE FROM MP_Job_application "\
            "WHERE MP_Job_application.application_id = " + application_id + ";"
    cursor = db_connection.cursor()
    cursor.execute("USE oxc353_1")
    cursor.execute(query)
    cursor.close()
    db_connection.commit()
    return

  
def application_job(posting_id, email):
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
    query = "DELETE FROM MP_User "\
            "WHERE MP_User.email='" + email + "';"
    cursor = db_connection.cursor()
    cursor.execute("USE oxc353_1")
    cursor.execute(query)
    cursor.close()
    db_connection.commit()
    return
