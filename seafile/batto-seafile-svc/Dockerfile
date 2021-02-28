FROM python:3.8-slim-buster

RUN pip install --no-cache-dir cheroot flask prometheus_client requests
COPY "batto-seafile-svc.py" "/batto-seafile-svc.py"
RUN chmod +x /batto-seafile-svc.py

EXPOSE 80
CMD [ "python", "/batto-seafile-svc.py" ]
