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
        attributesText = (dict(self.connection.response[0]['attributes']))
        attributeDName = self.connection.response[0]['dn']
        formattedMetrics = self.formatAttributes(attributesText, attributeDName)
        return formattedMetrics

    def formatAttributes(self, attributesText, attributeDName):

        metrics = self.config['prometheus']['metrics']
        for configMetric in metrics:
            if configMetric['name'] == attributeDName:
                
               formattedValues = formatValues(configMetric, attributesText)

        return  formattedValues


def formatValues(configMetric, attributesText):
    
    beautifulMetric = ""
    if configMetric['mono_values']:

        mono_values = configMetric['mono_values']
        if 'counters' in mono_values:

            if 'counters_help_label' in mono_values:
                beautifulMetric += "# HELP {} {}\n".format(configMetric['name'], mono_values['counters_help_label'])

            beautifulMetric += "# TYPE {} counter\n".format(configMetric['name'])
            for counter in mono_values['counters']:

                beautifulMetric += "{}{{{}}} {}\n".format(configMetric['name'], counter, attributesText[counter][0])

        if 'gauges' in mono_values:

            if 'gauges_help_label' in mono_values:
                beautifulMetric += "# HELP {} {}\n".format(configMetric['name'], mono_values['gauges_help_label'])

            beautifulMetric += "# TYPE {} gauge\n".format(configMetric['name'])
            for gauge in mono_values['gauges']:

                beautifulMetric += "{}{{{}}} {}\n".format(configMetric['name'], gauge, attributesText[gauge][0])


            
    print(configMetric, attributesText)
    return beautifulMetric