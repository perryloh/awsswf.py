# serial_worker.py
import time
import string
import boto.swf.layer2 as swf

class BaseWorker(swf.ActivityWorker):
    domain = 'perrypy'
    version = '1.0'
    task_list = None
   
    def run(self, id):          
		self.task_list = self.task_list.format(id)
		print 'base' + self.task_list
		activity_task = self.poll()
        
		if 'activityId' in activity_task:
            # Get input.
            # Get the method for the requested activity.
			try:
				print 'working on activity from tasklist %s at %i' % (self.task_list, time.time())
				self.activity(activity_task.get('input'))
			except Exception, error:
				self.fail(reason=str(error))
				raise error

			return True

    def activity(self, activity_input):
        raise NotImplementedError


