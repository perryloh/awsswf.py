import pika
import json
import createsupervisorconf
import subprocess

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')

print ' [*] Waiting for messages. To exit press CTRL+C'

def docker(args, stdin=None):
	print "# docker " + " ".join(args)
	p = subprocess.Popen(["docker"] + list(args), stdin=stdin, stdout=subprocess.PIPE)
	return p.stdout

def callback(ch, method, properties, body):
    print " [x] Received %r" % (body,)
    msg = json.loads(body)

    if msg['cmd'] == 'prv':
        createsupervisorconf.SupervisorConf().create(msg['id'])
        print docker(["run", "-d", "-v", "/vagrant:/vagrant", "-i","-t", "ubuntu-ncp-2", "/usr/bin/supervisord", "-c","/vagrant/supervisor{0}.conf".format(msg['id'])])
        #subprocess.call(['ls', '*.conf'])
        #subprocess.call('docker run -d -v /vagrant:/vagrant -i -t ubuntu-ncp-2 /usr/bin/supervisord -c /vagrant/supervisor{0}.conf'.format(msg['id']))

channel.basic_consume(callback,
                      queue='hello',
                      no_ack=True)

channel.start_consuming()