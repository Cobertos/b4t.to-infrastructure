FROM infiniteproject/icecast

COPY "entrypoint.sh" "/entrypoint.sh"
COPY "icecast.xml" "/usr/share/icecast/icecast.xml"
COPY "silence.mp3" "/usr/share/icecast/web/silence.mp3"
RUN chmod +x /entrypoint.sh

RUN chown -R icecast /usr/share/icecast

VOLUME ["/usr/share/icecast"]

ENTRYPOINT ["/entrypoint.sh"]
CMD ["icecast", "-c", "/usr/share/icecast/icecast.xml"]
