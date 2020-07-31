# Seafile Recovery from Backup

### To recover Seafile from a Duplicati backup

1. Download all the files through Duplicati to get them onto the server unencrypted
 * Note: You can only download to folders mounted to Duplicati, so you'll have to put it in Duplicati's data folder as data-to-backup is read-only for now
2. Copy all the files to the /opt/batto-cave folder (the seafile-data and seafile-mysql folders)
3. Point the docker-compose containers at these new folders

### If you need to start from a fresh slate of Docker containers

1. `docker-compose exec seafile bash` into the main container
2. Delete `/opt/seafile/conf/` and `/opt/seafile/ccnet/`
3. Run `/opt/seafile/seafile-server-latest/setup-seafile-mysql.sh`
4. Type in all the server and DB information again, recreate DBs
5. `docker-compose exec seafile-db bash` into the mysql container
6. Restore the Mysql tables from the backup files:

```
mysql -u[username] -p[password] ccnet_db < ccnet-db.sql.2013-10-19-16-00-05
mysql -u[username] -p[password] seafile_db < seafile-db.sql.2013-10-19-16-00-20
mysql -u[username] -p[password] seahub_db < seahub-db.sql.2013-10-19-16-01-05
```

Make sure that the DB names are correct!
From: https://seafile.gitbook.io/seafile-server-manual/administration/backup-and-recovery#restore-from-backup

### If you need to manually create the DBs for some reason

1. Run the mysql container
2. `docker-compose exec seafile-db bash` into the mysql container
3. Login to the mysql shell
4. Use `SHOW DATABASES;` `SELECT user FROM mysql.user;` to see things
5. Run the following commands to generate the database manually if necessary:

```
create database `ccnet_db` character set = 'utf8';
create database `seafile_db` character set = 'utf8';
create database `seahub_db` character set = 'utf8';

create user 'seafile'@'%' identified by 'SEAFILE_MYSQL_PASSWORD_HERE';

GRANT ALL PRIVILEGES ON `ccnet_db`.* to `seafile`@'%';
GRANT ALL PRIVILEGES ON `seafile_db`.* to `seafile`@'%';
GRANT ALL PRIVILEGES ON `seahub_db`.* to `seafile`@'%';
```

Making sure that the DB names are correct!
From: https://seafile.gitbook.io/seafile-server-manual/deploying-seafile-under-linux/deploying-seafile-with-mysql#prepare-mysql-databases

But localhost => % to connect from all hosts