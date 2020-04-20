FROM infiniteproject/icecast

COPY "icecast.xml" "/usr/share/icecast/icecast.xml"
COPY "silence.mp3" "/usr/share/icecast/web/silence.mp3"

RUN chown -R icecast /usr/share/icecast

VOLUME ["/usr/share/icecast"]

CMD ["icecast", "-c", "/usr/share/icecast/icecast.xml"]
