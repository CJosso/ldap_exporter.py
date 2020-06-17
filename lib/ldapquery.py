from ldap3 import Server, Connection, ALL



class LdapQuery:
    """A simple Ldap wrapper class"""

    def __init__(self, config):
        self.config = config
        self.server = Server(**self.config['ldap3']['server'])
        self.connection = Connection(self.server, **self.config['ldap3']['connection'])
        self.connection.bind()

    def fetch(self):
        self.connection.search(**self.config['ldap3']['search'][0])
        test = (dict(self.connection.response[0]['attributes']))
        print(self.connection.response)
        return test

