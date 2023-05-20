# to run as root on the real raspberry with pi user
# cat <<EOF >/etc/wireguard/wg-con-certeur.conf
# [Interface]
# Address = 20.20.0.2/32
# PrivateKey = <concerter privkey a generer et remplacer aussi la pubkey dans la conf server>
#PostUp = iptables -A FORWARD -i wg0 -j ACCEPT; iptables -t nat -A POSTROUTING -o ens18 -j MASQUERADE
#PostDown = iptables -D FORWARD -i wg0 -j ACCEPT; iptables -t nat -D POSTROUTING -o ens18 -j MASQUERADE

# Server
# [Peer]
# PublicKey = cVYFNw3EsZvX21+pz+pel0TqZewQSxoeNToxvLBeujs=
# Endpoint = <ip-server>:51820
# AllowedIPs = 20.20.0.0/16
# PersistentKeepalive = 25
# EOF

# sudo systemctl enable wg-quick@wg-con-certeur
# sudo systemctl start wg-quick@wg-con-certeur

cat <<EOF >/etc/systemd/system/concerteur.service
[Unit]
Description=Concerteur application

[Service]
Type=simple
WorkingDirectory=/home/fuz/Bureau/concerteurReboot
ExecStart=/bin/bash /home/fuz/Bureau/concerteurReboot/start-dev.sh
StandardOutput=append:/var/log/concerteur.log
StandardError=append:/var/log/concerteur.log


[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable concerteur
sudo systemctl start concerteur

