# serial_decider.py
import time
import boto.swf.layer2 as swf
from filelock import file_lock
import logging
import sys
import os


class SerialDecider(swf.Decider):

    domain = 'perrypy'
    task_list = 'default_tasks'
    version = '1.0'


    def run(self, id):    
        self.task_list = '{0}_tasks'.format(id)
        print 'polling ' + self.task_list
        history = self.poll()        
        if 'events' in history:            
            # Get a list of non-decision events to see what event came in last.
            workflow_events = [e for e in history['events']
                               if not e['eventType'].startswith('Decision')]
            decisions = swf.Layer1Decisions()
            # Record latest non-decision event.
            last_event = workflow_events[-1]
            last_event_type = last_event['eventType']
        
            if last_event_type == 'WorkflowExecutionStarted':
                # Schedule the first activity.
                start_event_attrs = last_event['workflowExecutionStartedEventAttributes']
                
                decisions.schedule_activity_task('%s-%i' % ('StringUpperActivity', time.time()),
                   'StringUpperActivity', self.version, task_list='su{0}_tasks'.format(id), input=start_event_attrs['input'])
            elif last_event_type == 'ActivityTaskCompleted':
                # Take decision based on the name of activity that has just completed.
                # 1) Get activity's event id.
                last_event_attrs = last_event['activityTaskCompletedEventAttributes']
                completed_activity_id = last_event_attrs['scheduledEventId'] - 1
                # 2) Extract its name.
                activity_data = history['events'][completed_activity_id]
                activity_attrs = activity_data['activityTaskScheduledEventAttributes']
                activity_name = activity_attrs['activityType']['name']
                # 3) Optionally, get the result from the activity.
                result = last_event['activityTaskCompletedEventAttributes'].get('result')

                # Take the decision.
                if activity_name == 'StringUpperActivity':
                    decisions.schedule_activity_task('%s-%i' % ('StringCapActivity', time.time()),
                        'StringCapActivity', self.version, task_list='sc{0}_tasks'.format(id), input=result)
                if activity_name == 'StringCapActivity':
                    decisions.schedule_activity_task('%s-%i' % ('StringReverseActivity', time.time()),
                        'StringReverseActivity', self.version, task_list='sr{0}_tasks'.format(id), input=result)
                elif activity_name == 'StringReverseActivity':
                    # Final activity completed. We're done.
                    decisions.complete_workflow_execution()

            self.complete(decisions=decisions)
            return True


if __name__ == "__main__":
	#logging.basicConfig(level=logging.DEBUG, filename='myapp.log')
	#os.remove('decider.lock')

    while 1:	
		#with file_lock('decider.lock'):
		try: 
			SerialDecider().run(sys.argv[1])
		except Exception as inst:
			print inst	  
	#			logging.exception(inst)
		
		time.sleep(30)