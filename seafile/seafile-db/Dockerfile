FROM mariadb:10.1

RUN apt-get update && \
  apt-get install -y --no-install-recommends apt-utils python3.8 python3-pip

RUN pip3 install --no-cache-dir cheroot flask prometheus_client
COPY "batto-seafile-db-backup-svc.py" "/batto-seafile-db-backup-svc.py"
RUN chmod +x /batto-seafile-db-backup-svc.py

COPY "start.sh" "/start.sh"
RUN chmod +x /start.sh

EXPOSE 34770
ENTRYPOINT ["/start.sh"]
# Seemingly need to put this, it can't inherit from the parent?
CMD ["mysqld"]