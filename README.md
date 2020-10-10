# b4t.to cave

My home server, maintained with Docker Compose!

## Setup

* `docker-compose up --build -d`

You might need to configure some of the services manually, but eventually all necessary configuration should be in this repo

## Services
### Public (personal/non-production grade)
* [statping](https://statping.b4t.to) - Uptime monitoring
* [mopidy](https://mopidy.b4t.to) - WIP Mopidy + MPD + Icecast streaming to stream Spotify, YouTube, SoundCloud, and my local files in one service.
* [netdata](https://nd.b4t.to) - Netdata instance
* [shieldsio](https://shields.b4t.to) - Shields.io instance

### Private
* [seafile](https://seafile.b4t.to) - Dropbox replacement with way better configs for ignoring files
* [freshrss](https://freshrss.b4t.to) - RSS feed reader
* [duplicati](https://duplicati.b4t.to) - Backups
* [wireguard](b4t.to:51820) - VPN

#### Monitoring
* [prometheus](https://prometheus.b4t.to) - Short term metric collection + alerts
* [grafana](https://grafana.b4t.to) - Long term metric visualizations

#### Plumbing
* [icecast](https://icecast.b4t.to) - The icecast server for streaming from mopidy
* [traefik](https://traefik.b4t.to) - Reverse proxy for all HTTP, manages all HTTPS and subdomain routing
* cloudflare-ddns - Syncs dynamic IP to the A records on cloudflare
