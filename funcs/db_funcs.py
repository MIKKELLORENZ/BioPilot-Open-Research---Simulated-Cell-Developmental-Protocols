import os

def get_db_creds():

    db_d = {}
    db_d['user'] = os.getenv('DB_USER')
    db_d['password'] = os.getenv('DB_PW')
    db_d['ip'] = os.getenv('DB_IP')
    db_d['db'] = os.getenv('DB_NAME')

    return db_d
