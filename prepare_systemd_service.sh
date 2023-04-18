# to run as root on the real raspberry with pi user

cat <<EOF >/etc/systemd/system/concerteur.service
[Unit]
Description=Concerteur application

[Service]
Type=simple
WorkingDirectory=/home/pi/concerteurReboot
ExecStart=/bin/bash /home/pi/concerteurReboot/start-dev.sh
StandardOutput=append:/var/log/concerteur.log
StandardError=append:/var/log/concerteur.log


[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable concerteur
sudo systemctl start concerteur