#!/usr/bin/env python

import argparse
import json
import subprocess

def read_json(f):
    f = open(f)
    j = json.loads(f.read())
    f.close()

    return j

def update_task_definitions(container_name, task_definition, family, image_name, tag, env):
    for d in task_definition['containerDefinitions']:
        d['name'] = container_name
        d['image'] = image_name + ':' + tag
        d['environment'].append({"name": "ENV", "value": env})

    task_definition['family'] = family

    return task_definition

def register_task_definition(task_definition):
    definition_str = ''
    proc = subprocess.Popen(["aws", "ecs", "register-task-definition", "--cli-input-json", json.dumps(task_definition)], stdout=subprocess.PIPE)
    while True:
        line = proc.stdout.readline()
        if line != '':
            definition_str += line.rstrip()
        else:
            break

    return json.loads(definition_str)

def task_arn(task_definition):
    return task_definition['taskDefinition']['taskDefinitionArn'].split('/')[-1].split(':')[0]

def update_service(service, cluster, task_arn):
    subprocess.call(['aws', 'ecs', 'update-service', '--cluster', cluster, '--service', service, '--task-definition', task_arn])

def run_task(cluster, task_arn):
    subprocess.call(['aws', 'ecs', 'run-task', '--cluster', cluster, '--task-definition', task_arn])
    
parser = argparse.ArgumentParser()

parser.add_argument('definitions', metavar='d', type=str)
parser.add_argument('env', metavar='e', type=str)
parser.add_argument('tag', metavar='t', type=str)

args = vars(parser.parse_args())

app = read_json(args['definitions'])
env = args['env']
env_config = app['envs'][env]

for service, service_def in env_config['services'].iteritems():
    task_def = read_json(service_def['template'])
    update_task_definitions(service_def['containerName'], task_def, service_def['family'], app['image'], args['tag'], env)

    # register task
    arn = task_arn(register_task_definition(task_def))

    # update service
    update_service(service_def['id'], env_config['cluster'], arn)

if 'tasks' in env_config:
    for task, task_item in env_config['tasks'].iteritems():
        task_def = read_json(task_item['template'])
        update_task_definitions(task_item['containerName'], task_def, task_item['family'], app['image'], args['tag'], env)

        # register task
        arn = task_arn(register_task_definition(task_def))

        # run task
        run_task(env_config['cluster'], arn)
