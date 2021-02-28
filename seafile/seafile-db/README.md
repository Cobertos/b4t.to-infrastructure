# b4t.to infra - Seafile DB

`seafile-db` is a MariaDB container + a Python script for backing up the Seafile tables according to their documentation. Read more https://manual.seafile.com/maintain/backup_recovery/

There's a `/seafile-backup` endpoint with Authentication that, when hitting, will backup the DBs
