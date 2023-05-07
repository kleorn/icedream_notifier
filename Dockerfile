FROM python:3.11.3-bullseye
# Указываем рабочую папку
WORKDIR /var/icedream_notifier
COPY ./crontab /etc/
# Копируем все файлы проекта в контейнер -  закомментировано, т.к. используем docker volumes
#COPY . /var/icedream_notifier
#EXPOSE 8080
RUN pip install requests lxml xmldiff
CMD cd /var/icedream_notifier && python3 main.py