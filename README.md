# b4t.to infrastructure

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
* [seafile](./seafile) - Dropbox replacement with way better configs for ignoring files
* [wireguard](b4t.to:51820) - VPN

#### Monitoring
* [prometheus](https://prometheus.b4t.to) - Short term metric collection + alerts
* [grafana](https://grafana.b4t.to) - Long term metric visualizations

#### Plumbing
* [icecast](https://icecast.b4t.to) - The icecast server for streaming from mopidy
* [traefik](https://traefik.b4t.to) - Reverse proxy for all HTTP, manages all HTTPS and subdomain routing
* cloudflare-ddns - Syncs dynamic IP to the A records on cloudflare

#### TODO
* Add self-hosted analytics service (ShyNet? - https://github.com/milesmcc/shynet , seems to be the most robust of all the self-hosted options, with fallbacks) or maybe (https://github.com/PostHog/posthog)
* Add OSX Docker container if possible (https://github.com/sickcodes/Docker-OSX )