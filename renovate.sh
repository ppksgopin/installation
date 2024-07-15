#! /bin/bash

dnf install {kernel-headers,kernel-devel} -y
dnf update -y

dnf config-manager --add-repo=https://download.docker.com/linux/centos/docker-ce.repo
dnf install -y yum-utils
dnf install -y docker-ce docker-ce-cli containerd.io
systemctl start docker && sudo systemctl enable --now docker

dnf install epel-release
dnf install ntfs-3g -y

sudo dnf install https://download1.rpmfusion.org/free/el/rpmfusion-free-release-9.noarch.rpm -y
sudo yum install vlc -y
