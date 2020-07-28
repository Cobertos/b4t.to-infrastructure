#!/bin/bash

# TODO: This should use the docker host hostname if possible
curl 192.168.240.1:7998/batto-scripts/backup --fail -H "Authorization: Bearer $BATTO_SCRIPT_AUTH"