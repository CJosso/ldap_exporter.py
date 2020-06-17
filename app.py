from flask import Flask
from lib.ldapquery import LdapQuery
from os import path

app = Flask(__name__)
configFile = path.join(app.root_path, 'config.yml')

@app.route('/')
def root():
    return '<html><head></head><body><H1>Welcome !</H1> \
        Go to <a href=/metrics>/metrics</a>'

@app.route('/metrics')
def metrics():
    ldapQuery = LdapQuery(configFile)
    metrics = ldapQuery.fetch()
    page = metrics
    return page

