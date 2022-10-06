
class DnsHostHandler:

    def __init__(self, filename: str):
        self.__filename = filename

    def check_exist_dns(self, hostname: str, domain: str) -> bool:
        with open(self.__filename, mode='r') as file:
            for line in file:
                if hostname + domain in line:
                    return True
        return False

    def append_host(self, hostname: str, ip: str, domain: str):
        with open(self.__filename, mode='a') as file:
            file.write('\n%s.%s        IN      A      %s' % (hostname, domain, ip))

    def write_host(self, hostname: str, ip: str, domain: str) -> None:
        if not self.check_exist_dns(hostname=hostname, domain=domain):
            self.append_host(hostname=hostname, ip=ip, domain=domain)
        else:
            self.delete_host(hostname=hostname, domain=domain)
            self.append_host(hostname=hostname, ip=ip, domain=domain)

    def delete_host(self, hostname: str, domain: str) -> None:
        if self.check_exist_dns(hostname=hostname, domain=domain):
            definition_hosts = False
            with open(self.__filename, 'r') as f:
                lines = f.readlines()
            with open(self.__filename, 'w') as f:
                for line in lines:
                    if '; name servers - A records' in line:
                        definition_hosts = True
                    if not definition_hosts:
                        f.write(line)
                    elif hostname + domain not in line:
                        f.write(line)

    def list_host(self) -> None:
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


if __name__ == "__main__":
    file_handler = DnsHostHandler('dns/etc/db.cognitive-equinox')
    file_handler.write_host(hostname='host3', ip='172.44.2.1', domain='.cognitive-equinox.com.')
    file_handler.write_host(hostname='host4', ip='172.44.2.9', domain='.cognitive-equinox.com.')
    file_handler.delete_host(hostname="host1", domain='.cognitive-equinox.com.')
    file_handler.delete_host(hostname="ns1", domain='.cognitive-equinox.com.')
    file_handler.delete_host(hostname='host3', domain='.cognitive-equinox.com.')
    hosts = file_handler.list_host()
    print(hosts)


