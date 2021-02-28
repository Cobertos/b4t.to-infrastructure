# b4t.to infra - Seafile

These are the configurations for Seafile, but they're not hooked up directly, because the data directory is volume'd out to the disk, so it all gets overlaid anyway?

Currently we do a couple of changes
* Up the max upload size
* Enable WebDAV
* Setup the WebDAV nginx configuration updates for WSGI (but we still have FastCGI enabled, I cant remember why)

### TODO

* Find a way to hook these configurations up directly to the container
* There's a bunch of PRs that fix a lot of issues wtih Docker Seafile that aren't merged. See https://github.com/haiwen/seafile-docker