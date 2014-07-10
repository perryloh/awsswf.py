import os
import sys

class SupervisorConf:
    template_file = 'supervisorconf.tpl'
    conf_file = 'supervisor{0}.conf'

    def create(self,id):
        template = open(self.template_file, 'r').read()    
        template = template.replace('{id}', id)

        self.conf_file = self.conf_file.format(id)
        open(self.conf_file,'w').write(template)

if __name__ == '__main__':
    SupervisorConf().create(sys.argv[1])