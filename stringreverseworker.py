from baseworker import BaseWorker
from filelock import file_lock
import string
import sys
import time
import os

class StringReverseWorker(BaseWorker):
    task_list = "sr{0}_tasks"

    def activity(self, activity_input):
        self.complete(result=activity_input[::-1])

if __name__ == "__main__":
    #os.remove('stringreverseworker.lock')

    while 1:	
        #with file_lock('stringreverseworker.lock'):
		try:
			StringReverseWorker().run(sys.argv[1])
		except Exception as inst:
			print inst	  
		time.sleep(30)