# register.py
import boto.swf.layer2 as swf
import boto.swf as s
import boto
from boto.swf.exceptions import SWFTypeAlreadyExistsError, SWFDomainAlreadyExistsError
DOMAIN = 'perrypy'
VERSION = '1.0'


#print s.regions()
boto.set_stream_logger('boto')
registerables = []
registerables.append(boto.swf.layer2.Domain(name=DOMAIN))
for workflow_type in ('BasicWorkflow','AdvWorkflow'):
    registerables.append(boto.swf.layer2.WorkflowType(domain=DOMAIN, name=workflow_type, version=VERSION, task_list='default'))

for activity_type in ('StringReverseActivity','StringUpperActivity','StringCapActivity'):
    registerables.append(boto.swf.layer2.ActivityType(domain=DOMAIN, name=activity_type, version=VERSION, task_list='default'))

for swf_entity in registerables:
    try:
        swf_entity.register()
        print swf_entity.name, 'registered successfully'
    except (SWFDomainAlreadyExistsError, SWFTypeAlreadyExistsError):
        print swf_entity.__class__.__name__, swf_entity.name, 'already exists'