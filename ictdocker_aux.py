import docker
import time

client = docker.from_env()

for container in client.containers.list():
	if 'ict' in container.name:
		print('Cleaning', container.name, '...')
		container.kill()

print('Removing stoped containers ...')
client.containers.prune()

client.containers.run('integrcity/rabbitmq', 
	name='ict-rab',
	ports={'5672/tcp': 5672},
	detach=True, 
	auto_remove=True)

client.containers.run('redis:alpine', 
	name='ict-red',
	ports={'6379/tcp': 6379},
	detach=True, 
	auto_remove=True)

time.sleep(5)

rab = client.containers.get('ict-rab')
red = client.containers.get('ict-red')

print('RabbitMQ:', rab.status)
print('Redis DB:', red.status)

local_folder_path = '/home/pablo/Projects/DemoGA'
container_folder_path = '/home/ictuser/work'
sce_file = 'data/sce.json'
run_file = 'data/run.json'

print('Running orchestrator ...')
client.containers.run('integrcity/orchestrator',
	name='ict-orch',
	volumes={local_folder_path: {'bind': container_folder_path, 'mode': 'rw'}},
	command='172.17.0.1 {} {}'.format(sce_file, run_file),
	detach=True, 
	auto_remove=True)

logs_generator = client.containers.get('ict-orch').logs(stream=True)

while True:
	try:
		output = logs_generator.__next__()
		print(output)

	except StopIteration:
		break
