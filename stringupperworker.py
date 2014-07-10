from baseworker import BaseWorker
from filelock import file_lock
import string
import sys
import time
import os

class StringUpperWorker(BaseWorker):
    task_list = "su{0}_tasks"

    def activity(self, activity_input):
        self.complete(result=string.upper(activity_input))

if __name__ == "__main__":
    #os.remove('stringupperworker.lock')

    while 1:	
		#with file_lock('stringupperworker.lock'):
		try:
			StringUpperWorker().run(sys.argv[1])
		except Exception as inst:
			print inst	  
		
		time.sleep(30)