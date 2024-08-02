#! /bin/bash
sudo docker run -d --init --restart=always -v /home/ppksgopin/downloads/jdownloader:/opt/JDownloader/Downloads -v /home/ppksgopin/downloads/jdownloader/config:/opt/JDownloader/app/cfg --name jdownloader -p 3129:3129 -e MYJD_USER=ppksgopin@gmail.com -e MYJD_PASSWORD=Azxpolmppk0215 -e MYJD_DEVICE_NAME=ppksgopin jaymoulin/jdownloader 
