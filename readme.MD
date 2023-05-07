# Ice Dream Notifier
## Установка
1. cd /var/docker_volumes
2. git clone https://github.com/kleorn/icedream_notifier
2. chmod -R 777 icedream_notifier
3. cd icedream_notifier
3. docker build . --tag icedream_notifier
4. docker run -v /var/docker_volumes/icedream_notifier:/var/icedream_notifier --restart unless-stopped icedream_notifier