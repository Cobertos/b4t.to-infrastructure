# b4t.to cave

My home server, maintained with Docker Compose!

## Services
#### Public
* [statping](statping.b4t.to) - Uptime monitoring
* [mopidy](mopidy.b4t.to) - WIP Mopidy + MPD + Icecast streaming to stream Spotify, YouTube, SoundCloud, and my local files in one service.

#### Private
* [seafile](seafile.b4t.to) - Dropbox replacement with way better configs for ignoring files
* [miniflux](miniflux.b4t.to) - RSS feed reader
* [wireguard](b4t.to:51820) - VPN

#### Plumbing
* [icecast](icecast.b4t.to) - The icecast server for streaming from mopidy
* [portainer](portainer.b4t.to) - Container management and monitoring
* [traefik](traefik.b4t.to) - Reverse proxy for all HTTP, manages all HTTPS and subdomain routing
* namecheap-ddns - Syncs dynamic IP to the A records on namecheap

## TODO - (add link to Notion.so list)
* Configure backups
* Configure statping