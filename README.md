# b4t.to cave

My home server, maintained with Docker Compose!

## Services
#### Public
* [statping](https://statping.b4t.to) - Uptime monitoring
* [mopidy](https://mopidy.b4t.to) - WIP Mopidy + MPD + Icecast streaming to stream Spotify, YouTube, SoundCloud, and my local files in one service.

#### Private
* [seafile](https://seafile.b4t.to) - Dropbox replacement with way better configs for ignoring files
* [freshrss](https://freshrss.b4t.to) - RSS feed reader
* [duplicati](https://duplicati.b4t.to) - Backups
* [wireguard](b4t.to:51820) - VPN

#### Plumbing
* [icecast](https://icecast.b4t.to) - The icecast server for streaming from mopidy
* [portainer](https://portainer.b4t.to) - Container management and monitoring
* [traefik](https://traefik.b4t.to) - Reverse proxy for all HTTP, manages all HTTPS and subdomain routing
* cloudflare-ddns - Syncs dynamic IP to the A records on cloudflare

## TODO - (add link to Notion.so list)
* Configure backups
* Configure statping