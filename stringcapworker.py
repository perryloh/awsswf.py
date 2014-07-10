from baseworker import BaseWorker
from filelock import file_lock
import string
import sys
import time
import os

class StringCapWorker(BaseWorker):
    task_list = "sc{0}_tasks"

    def activity(self, activity_input):
        return self.complete(result=string.capitalize(activity_input))

if __name__ == "__main__":
    #os.remove('./stringcapworker.lock')

    while 1:	
        #with file_lock('stringcapworker.lock'):
        try: 
            StringCapWorker().run(sys.argv[1]) # grab task list from command line argument
        except Exception as inst:
            print inst	  
        
        time.sleep(30)