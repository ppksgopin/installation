
dnf install https://dl.fedoraproject.org/pub/epel/epel-release-latest-9.noarch.rpm -y

dnf install pass -y

dnf install docker-ce docker-ce-cli containerd.io -y

systemctl start docker && systemctl enable --now docker