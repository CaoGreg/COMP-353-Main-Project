from dotenv import load_dotenv
from sshtunnel import SSHTunnelForwarder
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
    remote_bind_address=(db_host, 3306),
    local_bind_address=('127.0.0.1', 3306))

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
        print(row)
        data.append(row)
    cursor.close()
    return data


def search_postings(title, category):
    if title is None:
        title = ""
    if category is None:
        category = ""
    data = []
    cursor = db_connection.cursor()
    cursor.execute("USE oxc353_1")
    query = "SELECT * FROM MP_Job_posting " \
            "WHERE job_title LIKE '% " + title + "%' " \
            "OR category LIKE '%" + category+"%';"
    cursor.execute(query)
    for row in cursor:
        data.append(row)
    cursor.close()
    return data
