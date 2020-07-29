#!/bin/sh

# from https://docs.docker.com/engine/install/debian/
apt-get update

apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common

curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add -

apt-key fingerprint 0EBFCD88

add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/debian \
   $(lsb_release -cs) \
   stable"

apt-get update
# TODO: Match to parent docker version automatically
apt-get install -y \
    docker-ce=5:19.03.8~3-0~debian-buster \
    docker-ce-cli=5:19.03.8~3-0~debian-buster \
    containerd.io

# Delete cached files
apt-get clean
rm -rf /var/lib/apt/lists/*