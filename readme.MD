# Ice Dream Notifier
## Установка
1. cd /var/docker_volumes
1. git clone https://github.com/kleorn/icedream_notifier
1. Скопировать по FTP файл settings_secret.py ключом отправки e-mail и адресами для рассылки
1. chmod -R 777 icedream_notifier
1. cd icedream_notifier
1. docker build . --tag icedream_notifier
1. docker run -v /var/docker_volumes/icedream_notifier:/var/icedream_notifier --restart unless-stopped icedream_notifier
1. #docker run -it -v /var/docker_volumes/icedream_notifier:/var/icedream_notifier --restart unless-stopped icedream_notifier