from datetime import datetime
import pytz
from flask import Flask
import os

app = Flask(__name__)
SERVER_NAME = os.getenv("SERVER_NAME")
DNS_CONFIG_FILE = '/home/db.cognitive-equinox.com'
FORMAT = "%d/%m/%Y %H:%M:%S"
TZ = pytz.timezone('Europe/Madrid')


class FileHandler:

    def __init__(self, filename: str):
        self.__filename = filename

    def write_host(self, hostname: str, host: str):
        with open(self.__filename, mode='a') as file:
            file.write('\n%s.cognitive-equinox.com.        IN      A      %s' % (hostname, host))

    def delete_host(self, hostname: str):
        with open(self.__filename, 'r+') as file:
            lines = file.readlines()
            file.seek(0)
            for line in lines:
                if hostname + '.cognitive-equinox.com.' not in line:
                    file.write(line)
            file.truncate()

    def list_host(self):
        hosts = {}
        read = False
        with open(self.__filename, 'r') as file:
            for line in file:
                if '; name servers - A records' in line:
                    read = True
                elif read:
                    host = line.split('IN')[0].rsplit()[0]
                    ip = line.split('A')[1].rsplit()[0]
                    hosts[host] = ip
        return hosts


file_handler = FileHandler(DNS_CONFIG_FILE)


@app.route('/')
def root_path():
    return 'Call to /hello'


@app.route('/hello')
def hello():
    return {'name': SERVER_NAME, 'time': datetime.now(TZ).strftime(FORMAT)}


@app.route('/hosts')
def list_hosts():
    return file_handler.list_host()


@app.route('/host/<hostname>', methods=['GET', 'POST', 'DELETE'])
def crud_host(request):
    response = None
    hostname = request.view_args['hostname']

    if request.method == 'GET':
        hosts = file_handler.list_host()
        response = hosts.get(hostname, {})

    elif request.method == 'POST':
        # data = {"ip": "....."}
        data = request.json
        new_ip = data.get('ip', None)
        if new_ip:
            file_handler.write_host(hostname=hostname, host=new_ip)
            response = {'msg': 'Added new host "%s" with ip "%s"' % (hostname, new_ip)}
        else:
            response = 404, {'msg': 'Invalid body param: ip'}

    elif request.method == 'DELETE':
        file_handler.delete_host(hostname=hostname)
        response = {'msg': 'Removed host "%s"!' % hostname}

    return response
