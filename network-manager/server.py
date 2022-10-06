import copy
from datetime import datetime
import pytz
import requests
from flask import Flask, request, render_template
import os

app = Flask(__name__)
SERVER_NAME = os.getenv("SERVER_NAME")
DNS_CONFIG_FILE = '/home/db.cognitive-equinox.com'
DOMAIN = '.cognitive-equinox.com.'
FORMAT = "%d/%m/%Y %H:%M:%S"
TZ = pytz.timezone('Europe/Madrid')


class HostManager:
    def __init__(self):
        self.__dns_handler = DnsHostHandler(filename=DNS_CONFIG_FILE, domain=DOMAIN)
        self.__host_mapper = self.__dns_handler.list_host()

    def update_hosts(self):
        self.__host_mapper = {host: self.__host_mapper.get(host, info_host)
                              for host, info_host in self.__dns_handler.list_host().items()}

    @property
    def host_mapper(self):
        self.update_hosts()
        return copy.deepcopy(self.__host_mapper)

    def run_test(self, host):
        self.update_hosts()
        if host in self.__host_mapper:
            path = host
            if host[-1] == '.':
                path = host[:-1]
            self.__host_mapper[host]['test'] = requests.get('http://%s/hello' % path).text


class DnsHostHandler:

    def __init__(self, filename: str, domain: str):
        self.__filename = filename
        self.__domain = domain

    def check_exist_dns(self, hostname: str) -> bool:
        with open(self.__filename, mode='r') as file:
            for line in file:
                if hostname + self.__domain in line:
                    return True
        return False

    def append_host(self, hostname: str, ip: str):
        with open(self.__filename, mode='a') as file:
            file.write('%s%s        IN      A      %s\n' % (hostname, self.__domain, ip))

    def write_host(self, hostname: str, ip: str) -> None:
        if not self.check_exist_dns(hostname=hostname):
            self.append_host(hostname=hostname, ip=ip)
        else:
            self.delete_host(hostname=hostname)
            self.append_host(hostname=hostname, ip=ip)

    def delete_host(self, hostname: str) -> None:
        if self.check_exist_dns(hostname=hostname):
            definition_hosts = False
            with open(self.__filename, 'r') as f:
                lines = f.readlines()
            with open(self.__filename, 'w') as f:
                for line in lines:
                    if '; name servers - A records' in line:
                        definition_hosts = True
                    if not definition_hosts:
                        f.write(line)
                    elif hostname + self.__domain not in line:
                        f.write(line)

    def list_host(self) -> dict:
        hosts = {}
        read = False
        with open(self.__filename, 'r') as file:
            for line in file:
                if '; name servers - A records' in line:
                    read = True
                elif read:
                    if line.strip():
                        host = line.split('IN')[0].rsplit()[0]
                        ip = line.split('A')[1].rsplit()[0]
                        hosts[host] = {'ip': ip}
        return hosts


host_manager = HostManager()


@app.route('/', methods=('GET', 'POST'))
def root_path():
    if request.method == 'POST':
        host_manager.run_test(host=request.form['host'])

    return render_template('index.html', title='Index - Cognitive Equinox', dict_hosts=host_manager.host_mapper)

"""
@app.route('/hello')
def hello():
    return {'name': SERVER_NAME, 'time': datetime.now(TZ).strftime(FORMAT)}


@app.route('/hosts')
def list_hosts():
    return dns_handler.list_host()


@app.route('/host', methods=['POST'])
def new_host():
    # data = {"hostname": ".....", "ip": "....."}
    data = request.json
    hostname = data.get('hostname', None)

    new_ip = data.get('ip', None)
    if hostname and new_ip:
        parsed_hostname = hostname.replace(DOMAIN, '')
        dns_handler.write_host(hostname=parsed_hostname, ip=new_ip)
        response = {'msg': 'Added new host "%s" with ip "%s"' % (hostname, new_ip)}
    else:
        response = 404, {'msg': 'Invalid body'}
    return response


@app.route('/host/<hostname>', methods=['GET'])
def get_host(hostname):
    hosts = dns_handler.list_host()
    parsed_hostname = hostname.replace(DOMAIN, '') + DOMAIN
    host_ip = hosts.get(parsed_hostname, None)
    if host_ip:
        response = {'hostname': parsed_hostname, 'ip': host_ip}
    else:
        response = {}
    return response


@app.route('/host/<hostname>', methods=['DELETE'])
def remove_host(hostname):
    parsed_hostname = hostname.replace(DOMAIN, '')
    dns_handler.delete_host(hostname=parsed_hostname)
    return {'msg': 'Removed host "%s"!' % hostname}
"""