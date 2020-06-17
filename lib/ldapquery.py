from ldap3 import Server, Connection, ALL
import yaml



class LdapQuery:
    """A simple Ldap wrapper class"""

    def __init__(self, configFile):
        self.config = self.configInit(configFile)
        self.server = Server(**self.config['ldap3']['server'])
        self.connection = Connection(self.server, **self.config['ldap3']['connection'])
        self.connection.bind()

    def fetch(self):
        self.connection.search(**self.config['ldap3']['search'][0])
        test = (dict(self.connection.response[0]['attributes']))
        print(test)
        return test


    def configInit(self, configFile):
        stream = open(configFile, 'r')
        return yaml.safe_load(stream)