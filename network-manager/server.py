from datetime import datetime
import pytz
from flask import Flask, request, render_template
import os

app = Flask(__name__)
SERVER_NAME = os.getenv("SERVER_NAME")
DNS_CONFIG_FILE = '../volume/db.cognitive-equinox.com'
DOMAIN = '.cognitive-equinox.com.'
FORMAT = "%d/%m/%Y %H:%M:%S"
TZ = pytz.timezone('Europe/Madrid')


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
                        hosts[host] = ip
        return hosts


dns_handler = DnsHostHandler(filename=DNS_CONFIG_FILE, domain=DOMAIN)


@app.route('/', methods=['GET', 'POST'])
def root_path():
    list_hosts = {}
    if request.method == 'POST':
        if request.form.get('delete'):
            dns_handler.delete_host(hostname=request.form.get('host').replace(DOMAIN, ''))
        if request.form.get('add'):
            dns_handler.append_host('pruebaaa', '172.20.0.21')
        list_hosts = dns_handler.list_host()
    return render_template('index.html', title='Index - Cognitive Equinox', list_hosts=list_hosts)


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


if __name__ == "__main__":
    app.run(debug=True)