#!/usr/bin/python3

# Logic that requires multiple containers to talk to each other

# TODO: It'd be nice if on abort or success, this sent all the log output
# that's non-sensitive to the console so the other side can see it when
# curling

import subprocess
import os
from flask import Flask, abort, request, Blueprint
from cheroot.wsgi import Server as WSGIServer
from cheroot.wsgi import PathInfoDispatcher as WSGIPathInfoDispatcher
from dotenv import dotenv_values, find_dotenv

bp = Blueprint('batto-scripts', __name__)

env = dotenv_values(find_dotenv())
if "BATTO_SCRIPT_AUTH" not in env:
    raise RuntimeError("BATTO_SCRIPT_AUTH environment variable not in .env file")
authSecret = env["BATTO_SCRIPT_AUTH"]
seafileMysqlPwd = env["SEAFILE_MYSQL_PASSWORD"]

@bp.route('/backup')
def backup():
    """
    Runs backup script if header is present
    """

    # "Bearer XXXXXX"
    if 'Authorization' not in request.headers:
        abort(403)

    authParts = request.headers['Authorization'].split(" ")
    if len(authParts) != 2 or authParts[1] != authSecret:
        abort(403)

    print("Dumping seafile mysql databases")
    os.makedirs("/opt/batto-cave/seafile-data/backup/", exist_ok=True)
    # Dump each seafile DB into seafile directory for backup
    # per https://seafile.gitbook.io/seafile-server-manual/administration/backup-and-recovery
    # Specific for MariaDB Seafile
    ret = subprocess.run(f"docker-compose exec seafile-db mysqldump --host=seafile-db --user=root --password='{seafileMysqlPwd}' ccnet_db > /opt/batto-cave/seafile-data/backup/ccnet-db.sql && \
docker-compose exec seafile-db mysqldump --host=seafile-db --user=root --password='{seafileMysqlPwd}' seafile_db > /opt/batto-cave/seafile-data/backup/seafile-db.sql && \
docker-compose exec seafile-db mysqldump --host=seafile-db --user=root --password='{seafileMysqlPwd}' seahub_db > /opt/batto-cave/seafile-data/backup/seahub-db.sql", shell=True).returncode

    if ret != 0:
        abort(500, f"Mysql dump failed with code '{ret}'")

    return "success"

if __name__ == "__main__":
    app = Flask(__name__)
    app.register_blueprint(bp, url_prefix="/batto-scripts")

    # Flask dev server, don't use in production
    #app.run()

    # Cheroot (Cherrypy webserver) WSGI server. Use for prod
    d = WSGIPathInfoDispatcher({'/': app})
    server = WSGIServer(('0.0.0.0', 7998), d)
    print("Starting seafile batto-script server on port 7998")
    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()
