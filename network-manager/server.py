from datetime import datetime
import pytz
from flask import Flask, request
import os

app = Flask(__name__)
SERVER_NAME = os.getenv("SERVER_NAME")
DNS_CONFIG_FILE = '/home/db.cognitive-equinox.com'
DOMAIN = '.cognitive-equinox.com.'
FORMAT = "%d/%m/%Y %H:%M:%S"
TZ = pytz.timezone('Europe/Madrid')


class FileHandler:

    def __init__(self, filename: str, domain: str):
        self.__filename = filename
        self.__domain = domain

    def write_host(self, hostname: str, host: str):
        with open(self.__filename, mode='a') as file:
            file.write('\n%s.cognitive-equinox.com.        IN      A      %s' % (hostname, host))

    def delete_host(self, hostname: str):
        with open(self.__filename, 'r+') as file:
            lines = file.readlines()
            file.seek(0)
            for line in lines:
                if hostname + self.__domain not in line:
                    file.write(line)
            file.truncate()

    def list_host(self):
        hosts = {}
        read = False
        with open(self.__filename, 'r') as file:
            for line in file:
                print(line)
                if '; name servers - A records' in line:
                    read = True
                elif read:
                    host = line.split('IN')[0].rsplit()[0]
                    ip = line.split('A')[1].rsplit()[0]
                    hosts[host] = ip
        return hosts


file_handler = FileHandler(filename=DNS_CONFIG_FILE, domain=DOMAIN)


@app.route('/')
def root_path():
    return 'Call to /hello'


@app.route('/hello')
def hello():
    return {'name': SERVER_NAME, 'time': datetime.now(TZ).strftime(FORMAT)}


@app.route('/hosts')
def list_hosts():
    return file_handler.list_host()


@app.route('/host', methods=['POST'])
def new_host():
    # data = {"hostname": ".....", "ip": "....."}
    data = request.json
    hostname = data.get('hostname', None)

    new_ip = data.get('ip', None)
    if hostname and new_ip:
        parsed_hostname = hostname.replace('.cognitive-equinox.com.')
        file_handler.write_host(hostname=parsed_hostname, host=new_ip)
        response = {'msg': 'Added new host "%s" with ip "%s"' % (hostname, new_ip)}
    else:
        response = 404, {'msg': 'Invalid body'}
    return response


@app.route('/host/<hostname>', methods=['GET'])
def get_host(hostname):
    hosts = file_handler.list_host()
    host_ip = hosts.get(hostname, None)
    if host_ip:
        response = {'hostname': hostname, 'ip': host_ip}
    else:
        response = {}
    return response


@app.route('/host/<hostname>', methods=['DELETE'])
def remove_host(hostname):
    file_handler.delete_host(hostname=hostname)
    return {'msg': 'Removed host "%s"!' % hostname}
