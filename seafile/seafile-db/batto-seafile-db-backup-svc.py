#!/usr/bin/python

import subprocess
import os
from functools import partial
from flask import Flask, abort, request, Blueprint
from cheroot.wsgi import Server as WSGIServer
from cheroot.wsgi import PathInfoDispatcher as WSGIPathInfoDispatcher
from prometheus_client import make_wsgi_app
# Force flush to get it to print in Docker
# TODO: Maybe prefer the python CLI flag that does this?
fprint = partial(print, flush=True)

bp = Blueprint('batto-scripts', __name__)

if "BATTO_SVC_AUTH" not in os.environ:
    raise RuntimeError("BATTO_SVC_AUTH environment variable not set")
authSecret = os.environ["BATTO_SVC_AUTH"]
rootMysqlPwd = os.environ["MYSQL_ROOT_PASSWORD"]

def requiresAuthSecret(func):
  '''
  Function that wraps an endpoint to require the BATTO_SVC_AUTH secret as an
  Authorization Bearer token
  '''
  def abortIfNoAuth(*args, **kwargs):
      # "Bearer XXXXXX"
      if 'Authorization' not in request.headers:
          abort(403)

      authParts = request.headers['Authorization'].split(" ")
      if len(authParts) != 2 or authParts[1] != authSecret:
          abort(403)

      # Run the func like normal
      return func(*args, **kwargs)
  return abortIfNoAuth

@bp.route('/seafile-backup')
@requiresAuthSecret
def seafile_backup():
    """
    Runs a backup on the seafile specific tables
    """
    fprint("Dumping seafile mysql databases")
    os.makedirs("/opt/batto-cave/seafile-data/backup/", exist_ok=True)
    # Dump each seafile DB into seafile directory for backup (for MariaDB Seafile specifically)
    # per https://manual.seafile.com/maintain/backup_recovery/#backing-up-databases
    ret = subprocess.run(f"mysqldump --host=localhost --user=root --password='{rootMysqlPwd}' ccnet_db > /backup/ccnet-db.sql && \
mysqldump --host=localhost --user=root --password='{rootMysqlPwd}' seafile_db > /backup/seafile-db.sql && \
mysqldump --host=localhost --user=root --password='{rootMysqlPwd}' seahub_db > /backup/seahub-db.sql", shell=True).returncode
    fprint(f"Dumping seafile mysql databases finished with code '{ret}'")

    if ret != 0:
        abort(500, description=f"Mysqldump failed with code '{ret}'")

    return "success"

@bp.route('/ping')
def ping():
    """
    Returns pong
    """
    return "pong"

if __name__ == "__main__":
    app = Flask(__name__)
    app.register_blueprint(bp)#, url_prefix="/batto-scripts")

    # Flask dev server, don't use in production
    #app.run()

    # Cheroot (Cherrypy webserver) WSGI server. Use for prod
    d = WSGIPathInfoDispatcher({
        '/': app,
        '/metrics': make_wsgi_app()
    })
    server = WSGIServer(('0.0.0.0', 34770), d)
    fprint("Starting python service on 34770")
    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()
