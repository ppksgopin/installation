#! /bin/bash

sudo dnf install {kernel-headers,kernel-devel} -y
sudo dnf update -y


sudo dnf install epel-release -y
sudo dnf install https://download1.rpmfusion.org/free/el/rpmfusion-free-release-9.noarch.rpm -y
sudo yum install vlc -y

sudo dnf install ntfs-3g -y


sudo dnf install https://dl.fedoraproject.org/pub/epel/epel-release-latest-9.noarch.rpm -y
sudo dnf install pass -y
sudo dnf config-manager --add-repo https://download.docker.com/linux/rhel/docker
sudo dnf install docker-ce docker-ce-cli containerd.io -y
sudo systemctl start docker && sudo systemctl enable --now docker
