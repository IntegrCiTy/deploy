import docker
import time

client = docker.from_env()

local_folder_path = '/home/pablo/Projects/DemoGA'
container_folder_path = '/home/ictuser/work'

def run_ict_node(node_name, local_path, conta_path, wrap_file):

	client.containers.run('integrcity/node',
		name=node_name,
		volumes={local_path: {'bind': conta_path, 'mode': 'rw'}},
		command='wrappers/{} 172.17.0.1'.format(wrap_file),
		detach=True, 
		auto_remove=True)


nodes = {
	'ict-node1': 'cool_consumer.py',
	'ict-node2': 'heat_consumer.py',
	'ict-node3': 'hp_central.py',
	'ict-node4': 'hp_heating.py',
	'ict-node5': 'hp_cooling.py',
	'ict-node6': 'power_network.py',
	'ict-node7': 'thermal_network.py'}

for name, file in nodes.items():
	print('Running', name, 'with', file)

	run_ict_node(
		name,
		local_folder_path, 
		container_folder_path, 
		file)

nodes_logs = {name: client.containers.get(name).logs(stream=True) for name in nodes}
