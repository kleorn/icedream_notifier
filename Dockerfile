FROM python:3.11.3-bullseye
# ��������� ������� �����
WORKDIR /var/icedream_notifier
COPY ./crontab /etc/
# �������� ��� ����� ������� � ��������� -  ����������������, �.�. ���������� docker volumes
#COPY . /var/icedream_notifier
#EXPOSE 8080
RUN pip install requests lxml xmldiff
CMD cd /var/icedream_notifier && python3 main.py