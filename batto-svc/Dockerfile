FROM python:3.8-slim-buster

# Install docker for querying via mounted docker socket
# from https://docs.docker.com/engine/install/debian/
COPY "install-docker.sh" "/install-docker.sh"
RUN chmod +x /install-docker.sh
RUN /install-docker.sh


RUN pip install --no-cache-dir cheroot flask
COPY "batto-svc.py" "/batto-svc.py"
RUN chmod +x /batto-svc.py

EXPOSE 80
CMD [ "python", "/batto-svc.py" ]
