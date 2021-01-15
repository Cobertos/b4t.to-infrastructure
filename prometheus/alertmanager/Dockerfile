
FROM quay.io/prometheus/alertmanager
ARG GMAIL_ACCOUNT_USERNAME
ARG GMAIL_ACCOUNT_PASSWORD
ADD alertmanager.yml /etc/alertmanager/

# alertmanager doesn't support environment variables in it's yaml config so we have
# to do it in the Dockerfile build with a string replace
RUN sed -i "s|__GMAIL_ACCOUNT_USERNAME__|${GMAIL_ACCOUNT_USERNAME}|g" /etc/alertmanager/alertmanager.yml
RUN sed -i "s|__GMAIL_ACCOUNT_PASSWORD__|${GMAIL_ACCOUNT_PASSWORD}|g" /etc/alertmanager/alertmanager.yml
