# ldap_exporter.py (WIP)

Simple Prometheus exporter for LDAP written in Python3
License : Apache 2.0 http://www.apache.org/licenses/

# Prerequisite

- python3 (v3.6 tested)
- pip

# Limitations

Only counter and gauge are supported

# Dependencies

- Flask (https://flask.palletsprojects.com)
- ldap3 (https://pypi.org/project/ldap3/)

# Install

```
git clone https://github.com/CJosso/ldap_exporter.py.git
cd ldap_exporter.py
pip install -r requirements.txt
```

# Launch

` # python app.py `

# Usage

Create a config.yml file from example-config.yml
Setup your search in ldap section :
```
  search:
    - search_base: 'cn=monitor'
      search_scope: 'BASE'
      search_filter: '(objectclass=*)'
      attributes: '*'
```

Then setup the exposed metrics in prometheus section :
```
prometheus:
  metrics:
    - name: 'ldap_monitor'
      search_base: 'cn=monitor'
      mono_values:
        counter_help_label: "Compteur depuis le monitoring général"
        counter:
        - 'bytessent'
        - 'entriessent'
        - 'opscompleted'
        - 'opsinitiated'
        - 'totalconnections'
        gauge_help_label: "Jauges depuis le monitoring général"
        gauge:
        - 'cache-avail-bytes'
        - 'connectionpeak'
        - 'currentconnections'
        - 'currentpsearches'
        - 'dtablesize'
        - 'heapmaxhighhits'
        - 'heapmaxlowhits'
        - 'nbackends'
        - 'readwaiters'
        - 'request-que-backlog'
        - 'threads'
```

