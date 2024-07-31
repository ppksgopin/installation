#!/bin/bash
apt-get update -y && apt-get upgrade -y
apt-get install ibus-chewing -y

install -d -m 0755 /etc/apt/keyrings
wget -q https://packages.mozilla.org/apt/repo-signing-key.gpg -O- | tee /etc/apt/keyrings/packages.mozilla.org.asc > /dev/null
gpg -n -q --import --import-options import-show /etc/apt/keyrings/packages.mozilla.org.asc | awk '/pub/{getline; gsub(/^ +| +$/,""); print "\n"$0"\n"}'
echo "deb [signed-by=/etc/apt/keyrings/packages.mozilla.org.asc] https://packages.mozilla.org/apt mozilla main" | tee -a /etc/apt/sources.list.d/mozilla.list > /dev/null
echo 'Package: * Pin: origin packages.mozilla.org Pin-Priority: 1000' | tee /etc/apt/preferences.d/mozilla
apt-get install firefox -y
apt-get update -y && apt-get upgrade -y

apt install vlc -y
apt-get update -y && apt-get upgrade -y

apt-get install ca-certificates curl -y
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
chmod a+r /etc/apt/keyrings/docker.asc

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null

apt-get update -y && apt-get upgrade -y
apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y
systemctl start docker && systemctl enable --now docker
apt-get update -y && apt-get upgrade -y

apt install -y qemu-kvm libvirt-daemon-system virt-manager libvirt-clients bridge-utils virtinst -y
systemctl start libvirtd && systemctl enable --now libvirtd

nmcli conn add type bridge autoconnect no con-name kvmbr0 ifname kvmbr0
nmcli conn modify kvmbr0 ipv4.address 192.168.1.179/24 gw4 192.168.1.1 ipv4.method manual
nmcli conn add type bridge-slave autoconnect yes con-name enp0s3 ifname enp0s3 master kvmbr0

apt-get update -y && apt-get upgrade -y
apt install gdebi
wget https://zoom.us/download?os=linux
apt install ./zoom_amd64.deb

apt-get update -y && apt-get upgrade -y
reboot
