#! /bin/bash

PATH=/bin

dnf install https://dl.fedoraproject.org/pub/epel/epel-release-latest-9.noarch.rpm -y

dnf install pass -y

dnf config-manager --add-repo https://download.docker.com/linux/rhel/docker

dnf install docker-ce docker-ce-cli containerd.io -y

systemctl start docker && systemctl enable --now docker
