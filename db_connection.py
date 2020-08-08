from dotenv import load_dotenv
from sshtunnel import SSHTunnelForwarder
import pymysql
import os


def get_all_users():
    load_dotenv()
    encs_user = os.getenv("ENCS_USR")
    encs_password = os.getenv("ENCS_PWD")
    db_user = os.getenv("DB_USR")
    db_password = os.getenv("DB_PWD")
    db_host = 'oxc353.encs.concordia.ca'
    with SSHTunnelForwarder(
        ('login.encs.concordia.ca', 22),
        ssh_username=encs_user,
        ssh_password=encs_password,
        remote_bind_address=(db_host, 3306)
    ) as tunnel:
        port = tunnel.local_bind_port
        db_connection = pymysql.connect(
            host='localhost', port=port, db='oxc353_1', user=db_user,
            password=db_password, charset='utf8mb4')
        cursor = db_connection.cursor()
        cursor.execute("USE oxc353_1")
        cursor.execute("SELECT email, name, is_active, user_type, is_admin FROM MP_User")
        data = []
        for row in cursor:
            print(row)
            data.append(row)
        db_connection.close()
        return data
