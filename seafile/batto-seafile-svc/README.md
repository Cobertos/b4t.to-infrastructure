# b4t.to infra - Batto Seafile Svc

Small service to allow us for orchestrating Seafile tasks, like backups

### TODO

* Currently this only clones the files themselves to B2 and to local, but doesn't actually backup the Seafile DB or configurations. This means in case of a catastrophic failure we would have to reload everything into Seafile, which, tbh, not that worrisome rn... As long as the files are protected