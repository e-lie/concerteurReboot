

# Installer tout le concerteur à partir de raspiOS vierge


- prendre raspiOS 64 bit, installer avec l'utilisateur `pi` (quelques chemins absolus encore)

- `curl -fssL https://get.docker.com o get-docker.sh && bash get-docker.sh`
- `pip3 install docker-compose && echo 'export PATH="$PATH:/home/pi/.local/bin"' | tee -a ~/.bashrc`
- `git clone github.com/ .... wiringPi && cd wiringPi && ./build`

- `git clone https://github.com/e-lie/concerteurReboot.git`
- `cd concerteurReboot`
- `docker-compose up -d`