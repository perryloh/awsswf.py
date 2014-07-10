[supervisord]
nodaemon=true

[program:decider]
command=/usr/bin/python /vagrant/decider.py '{id}'
autorestart=true

[program:stringcapworker]
command=/usr/bin/python /vagrant/stringcapworker.py '{id}'
autorestart=true

[program:stringupperworker]
command=/usr/bin/python /vagrant/stringupperworker.py '{id}'
autorestart=true

[program:stringreverseworker]
command=/usr/bin/python /vagrant/stringreverseworker.py '{id}'
autorestart=true