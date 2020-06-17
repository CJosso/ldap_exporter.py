from flask import Flask
from lib.ldapquery import LdapQuery
from os import path
import yaml

app = Flask(__name__)
configFile = path.join(app.root_path, 'config.yml')
stream = open(configFile, 'r')
config = yaml.safe_load(stream)

@app.route('/')
def root():
    return '<html><head></head><body><H1>Welcome !</H1> \
        Go to <a href=/metrics>/metrics</a>'

@app.route('/metrics')
def metrics():
    ldapQuery = LdapQuery(config)
    metrics = ldapQuery.fetch()
    page = metrics
    return page

if __name__ == '__main__':
    app.run(**config['flask']['app'])