
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


if __name__ == "__main__":
    file_handler = FileHandler('../dns/etc/db.cognitive-equinox')
    file_handler.write_host(hostname='host3', host='172.44.2.1')
    file_handler.delete_host(hostname="ns1")
    hosts = file_handler.list_host()
    print(hosts)


