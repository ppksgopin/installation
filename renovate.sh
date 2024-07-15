#! /bin/bash

dnf install {kernel-headers,kernel-devel} -y
dnf update -y

dnf config-manager --add-repo=https://download.docker.com/linux/centos/docker-ce.repo
dnf install -y yum-utils
dnf install -y docker-ce docker-ce-cli containerd.io
systemctl start docker && sudo systemctl enable --now docker

dnf install epel-release -y
dnf install ntfs-3g -y

sudo dnf install https://download1.rpmfusion.org/free/el/rpmfusion-free-release-9.noarch.rpm -y
sudo dnf install vlc -y

dnf install {virt-install,virt-viewer,libvirt,virt-manager,virt-top,libguestfs-tools} -y
systemctl start libvirtd && systemctl enable --now libvirtd

nmcli conn add type bridge autoconnect no con-name kvmbr0 ifname kvmbr0
nmcli conn modify kvmbr0 ipv4.address 192.168.1.179/24 gw4 192.168.1.1 ipv4.method manual
nmcli conn add type bridge-slave autoconnect yes con-name enp0s3 ifname enp0s3 master kvmbr0

reboot
