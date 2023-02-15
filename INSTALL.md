

# Installer tout le concerteur à partir de raspiOS vierge


- prendre raspiOS 64 bit, installer avec l'utilisateur `pi` (quelques chemins absolus encore)

- `curl -fssL https://get.docker.com o get-docker.sh && bash get-docker.sh`
- `pip3 install docker-compose && echo 'export PATH="$PATH:/home/pi/.local/bin"' | tee -a ~/.bashrc`
- `git clone github.com/ .... wiringPi && cd wiringPi && ./build`

- `sudo apt install python3-gst-1.0 # necessary for playsound library`

- `git clone https://github.com/e-lie/concerteurReboot.git`
- `cd concerteurReboot`
- `docker-compose up -d`