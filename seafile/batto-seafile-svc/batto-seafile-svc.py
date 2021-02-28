#!/usr/bin/python

# Logic that requires multiple containers to talk to each other

# TODO: It'd be nice if on abort or success, this sent all the log output
# that's non-sensitive to the console so the other side can see it when
# curling

import subprocess
import os
import requests
from functools import partial
from flask import Flask, abort, request, Blueprint
from cheroot.wsgi import Server as WSGIServer
from cheroot.wsgi import PathInfoDispatcher as WSGIPathInfoDispatcher
from prometheus_client import make_wsgi_app, Gauge, Counter
# Force flush to get it to print in Docker
# TODO: Maybe prefer the python CLI flag that does this?
fprint = partial(print, flush=True)

bp = Blueprint('batto-scripts', __name__)

if "BATTO_SVC_AUTH" not in os.environ:
    raise RuntimeError("BATTO_SVC_AUTH environment variable not set")
authSecret = os.environ["BATTO_SVC_AUTH"]

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

def getRcloneJobRunning(jobId):
    if jobId == None:
        return False

    resp = requests.post("http://test:test@seafile-backups:5572/job/status", data={
        'jobid': jobId
    }, headers={
        'Authorization': 'Basic dGVzdDp0ZXN0'
    })
    json = resp.json()
    fprint(json)
    return json["finished"]

jobStatusGauge = Gauge('batto_seafile_svg_rclone_job_status', 'Whether the rclone job is running, 0 if not, 1 if running', ['rclone_job'])
jobIds = {
    "remote": None,
    "local": None,
    # "dbRemote": None,
    # "dbLocal": None
}

def updateRcloneJobStatus():
    """
    Updates the status of our variables from rclone
    """
    global jobIds, jobStatusGauge

    # Check if the jobs are running, update the variables
    for jobName, jobId in jobIds.items():
        jobIsRunning = getRcloneJobRunning(jobId)
        jobIds[jobName] = jobId if jobIsRunning else None
        jobStatusGauge.labels(rclone_job=jobName).set(1 if jobIsRunning else 0)

@bp.route('/seafile-backup')
@requiresAuthSecret
def seafile_backup():
    """
    Runs a Seafile/Rclone backup
    """
    global jobIds

    updateRcloneJobStatus()

    if any(jobId != None for _, jobId in jobIds.items()):
        abort(423, "A job is already running")

    # First, backup the databases (per Seafile documentation)
    # https://manual.seafile.com/maintain/backup_recovery/#backup-order-database-first-or-data-directory-first
    # requests.post("http://seafile-db:34770/seafile-backup", headers={
    #     Authorization: f'Bearer {authSecret}'
    # })

    # Second, queue all the rclone jobs
    fprint("Queue'ing up rclone jobs")
    jobsData = {
        # Backup all the seafile files to remote (backblze B2)
        "remote": {
            "srcFs": 'battoseafile:',
            "dstFs": 'battob2:b4tto-seafile-backup-2',
        },
        # Backup all the seafile files to local backup
        "local": {
            "srcFs": 'battoseafile:',
            "dstFs": '/backup-local-dest/files',
        },
        # TODO: Readd the backups for the db and db data
        # Probably need their own bucket
        # Backup all the seafile db and config files to remote (backblaze B2)
        # "dbRemote": {
        #     "srcFs": 'battoseafile:',
        #     "dstFs": 'battob2:b4tto-seafile-backup-2',
        # },
        # # Backup all the seafile db and config files to local
        # "dbLocal": {
        #     "srcFs": 'battoseafile:',
        #     "dstFs": 'battob2:b4tto-seafile-backup-2',
        # }
        # ... and the data ones
    }
    for jobName, jobData in jobsData.items():
        fprint(f"Queue'ing up rclone job '{jobName}'")
        resp = requests.post("http://test:test@seafile-backups:5572/sync/sync", data={
            **jobsData,
            "_async": True
        }, headers={
            'Authorization': 'Basic dGVzdDp0ZXN0'
        })
        json = resp.json()
        fprint(json)
        jobIds[jobName] = json["jobid"]
        fprint(f"Rclone job '{jobName}' got id '{jobIds[jobName]}'")

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
    server = WSGIServer(('0.0.0.0', 80), d)
    fprint("Starting batto-seafile-backup-svc")
    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()
