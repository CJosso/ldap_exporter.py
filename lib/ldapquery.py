from ldap3 import Server, Connection, ALL



class LdapQuery:
    """A simple Ldap wrapper class"""

    def __init__(self, config):
        
        self.config = config
        self.server = Server(**self.config['ldap3']['server'])
        self.connection = Connection(self.server, **self.config['ldap3']['connection'])
        self.connection.bind()

    def fetch(self):
        formattedMetrics = ""
        for search in self.config['ldap3']['search']:
            self.connection.search(**search)
            attributesText = (dict(self.connection.response[0]['attributes']))
            print(self.connection.response[0]['dn'])
            searchBase = search['search_base']
            formattedMetrics += self.formatAttributes(attributesText, searchBase)
        
        return formattedMetrics

    def formatAttributes(self, attributesText, searchBase):

        metrics = self.config['prometheus']['metrics']
        for configMetric in metrics:
            if configMetric['search_base'] == searchBase:
                
               formattedValues = formatValues(configMetric, attributesText)

        return  formattedValues


def formatValues(configMetric, attributesText):
    
    beautifulMetric = ""
    if configMetric['mono_values']:

        monoValues = configMetric['mono_values']
        if 'counter' in monoValues:
            beautifulMetric += formatMonoValues(monoValues, attributesText, configMetric['name'], 'counter')

        if 'gauge' in monoValues:
            beautifulMetric += formatMonoValues(monoValues, attributesText, configMetric['name'], 'gauge')

#    print(configMetric, attributesText)
    return beautifulMetric

def formatMonoValues(monoValues, attributesText, name, valueType):

    metricsOut = ""
    if valueType + '_help_label' in monoValues:
        metricsOut += "# HELP {} {}\n".format(name, monoValues[valueType + '_help_label'])

    metricsOut += "# TYPE {} {}\n".format(name, valueType)

    for counter in monoValues[valueType]:
        if isinstance(attributesText[counter], list):
            metricsOut += "{}{{label={}}} {}\n".format(name, counter, attributesText[counter][0])
        else:
            metricsOut += "{}{{label={}}} {}\n".format(name, counter, attributesText[counter])

    return metricsOut

    


