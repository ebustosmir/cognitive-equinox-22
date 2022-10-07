import copy
import threading
import pytz
import requests
from flask import render_template
import queue
from flask import Flask, request
from watchfiles import watch
import time
import os

app = Flask(__name__)
SERVER_NAME = os.getenv("SERVER_NAME")
DNS_CONFIG_FILE = '/home/db.cognitive-equinox.com'
DNS_LOG_CONFIG_FILE = '/home/logs/query'
DOMAIN = '.cognitive-equinox.com.'
FORMAT = "%d/%m/%Y %H:%M:%S"
TZ = pytz.timezone('Europe/Madrid')
MAX_ATTEMPS = 10
SLEEP_TIME = 5
RETRY_CODES = {429, 500}
logs = queue.Queue()


def handle_change(file_path):
    with open(file_path, 'r') as f_in:
        data = f_in.readlines()[-1]
    return data


def stream_worker():
    count = 0
    for _ in watch(DNS_LOG_CONFIG_FILE):
        new_data = handle_change(file_path=DNS_LOG_CONFIG_FILE)
        logs.put((count, new_data))
        count += 1


# Turn-on the worker thread.
threading.Thread(target=stream_worker, daemon=True).start()


class HostsManager:
    def __init__(self):
        self.__dns_handler = DnsHostHandler(filename=DNS_CONFIG_FILE, domain=DOMAIN)
        self.__hosts_mapper = {
            'host1.cognitive-equinox.com': {'ip': '172.20.0.4', 'show': False},
            'host2.cognitive-equinox.com': {'ip': '172.20.0.5', 'show': False},
            'host3.cognitive-equinox.com': {'ip': '172.20.0.6', 'show': False},
            'host4.cognitive-equinox.com': {'ip': '172.20.0.7', 'show': False},
            'host5.cognitive-equinox.com': {'ip': '172.20.0.8', 'show': False}
        }
        self.__session = requests.Session()

    def update_hosts(self):
        update_list = self.__dns_handler.list_host()
        for host, info_host in self.__hosts_mapper.items():
            if host not in update_list:
                self.__hosts_mapper[host]['show'] = False
                self.__hosts_mapper[host]['test'] = None
            else:
                self.__hosts_mapper[host]['show'] = True

    @property
    def host_mapper(self) -> dict:
        self.update_hosts()
        return copy.deepcopy(self.__hosts_mapper)

    def run_test(self, host):
        self.update_hosts()
        if host in self.__hosts_mapper:
            self.__hosts_mapper[host]['test'] = requests.get('http://%s/hello' % host).text
            response = None
            num_attempts = 0
            while response is None:
                try:
                    num_attempts += 1
                    response = self.__session.request(method='get', url='http://%s/hello' % host)
                except requests.RequestException as exc:
                    if num_attempts < MAX_ATTEMPS:
                        time.sleep(SLEEP_TIME)
                    else:
                        response = {'msg': 'Node not avaliable'}
                else:
                    if response.status_code in RETRY_CODES and num_attempts < MAX_ATTEMPS:
                        time.sleep(SLEEP_TIME)
                        response = None

            self.__hosts_mapper[host]['test'] = response.text

    def add_new_host(self):
        for host, info_host in self.__hosts_mapper.items():
            if not info_host['show']:
                self.__dns_handler.append_host(hostname=host, ip=info_host['ip'])
                break
        self.update_hosts()

    def remove_host(self, host):
        self.__dns_handler.delete_host(hostname=host)
        self.update_hosts()


class DnsHostHandler:

    def __init__(self, filename: str, domain: str):
        self.__filename = filename
        self.__domain = domain

    def check_exist_dns(self, hostname: str) -> bool:
        result = False
        with open(self.__filename, mode='r') as file:
            for line in file:
                if hostname in line:
                    result = True
                    break
        return result

    def append_host(self, hostname: str, ip: str):
        with open(self.__filename, mode='a') as file:
            file.write('%s.        IN      A      %s\n' % (hostname, ip))

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
                    elif hostname not in line:
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
                        host_name = host
                        if host[-1] == '.':
                            host_name = host_name[:-1]
                        ip = line.split('A')[1].rsplit()[0]
                        hosts[host_name] = {'ip': ip}
        return hosts


hosts_manager = HostsManager()


@app.route('/', methods=('GET', 'POST'))
def root_path():
    logs_json = {}

    if request.method == 'POST':
        if request.form.get('delete'):
            hosts_manager.remove_host(host=request.form['host'])
        elif request.form.get('add'):
            hosts_manager.add_new_host()
        elif request.form.get('test'):
            hosts_manager.run_test(host=request.form['host'])
        elif request.form.get('refresh'):
            while not logs.empty():
                i, last_logs = logs.get()
                logs_json[i] = last_logs

    return render_template('index.html', title='Index - Cognitive Equinox',
                           dict_hosts=hosts_manager.host_mapper, logs=logs_json)


@app.route('/hosts')
def list_hosts():
    return hosts_manager.host_mapper

"""
@app.route('/host', methods=['POST'])
def new_host():
    # data = {"hostname": ".....", "ip": "....."}
    data = request.json
    hostname = data.get('hostname', None)

    new_ip = data.get('ip', None)
    if hostname and new_ip:
        parsed_hostname = hostname.replace(DOMAIN, '')
        hosts_manager.add_new_host(hostname=parsed_hostname, ip=new_ip)
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


@app.route('/logs', methods=['GET'])
def get_logs():
    results = {}
    while not logs.empty():
        i, last_logs = logs.get()
        results[i] = last_logs
    return results
