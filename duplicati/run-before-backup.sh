#!/bin/bash

curl batto-svc:7998/backup --fail --silent -H "Authorization: Bearer $BATTO_SCRIPT_AUTH"