
import os

from flask import Flask
import pymysql

db_user = 'master_capsum'
db_password = 'aiccsql@2020'
db_name = 'capsum_db'
db_connection_name = 'capsum-project-292904:us-central1:capsum-sql'

app = Flask(__name__)


@app.route('/')
def main():
    # When deployed to App Engine, the `GAE_ENV` environment variable will be
    # set to `standard`
    if os.environ.get('GAE_ENV') == 'standard':
        # If deployed, use the local socket interface for accessing Cloud SQL
        unix_socket = '/cloudsql/{}'.format(db_connection_name)
        cnx = pymysql.connect(user=db_user, password=db_password,
                              unix_socket=unix_socket, db=db_name)
    else:
        # If running locally, use the TCP connections instead
        # Set up Cloud SQL Proxy (cloud.google.com/sql/docs/mysql/sql-proxy)
        # so that your application can use 127.0.0.1:3306 to connect to your
        # Cloud SQL instance
        host = '35.222.218.28'
        cnx = pymysql.connect(user=db_user, password=db_password,
                              host=host, db=db_name)

    with cnx.cursor() as cursor:
        cursor.execute('select * from user;')
        result = cursor.fetchall()
        current_msg = result[0][0]
    cnx.close()

    return str(current_msg)
# [END gae_python37_cloudsql_mysql]


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)