import iland
import time

CLIENT_ID = ''
CLIENT_SECRET = ''
USERNAME = ''
PASSWORD = ''

api = iland.Api(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, username=USERNAME, password=PASSWORD)

def main():
    vdc_uuid = print_entity_inventory('IAAS_VDC')
    vapp_uuid = create_scratch_vapp(vdc_uuid)
    delete_vapp(vapp_uuid)

'''
This function gets a user's inventory with the GET endpoint /users/{username}/inventory and filters to get the specified
entity type. In this case I am getting all the vDCs the user has access to so I pass IAAS_VDC.
Besides printing all the vDCS, this function lazily grabs the first vDC uuid for the scratch vApp that we create below.
'''
def print_entity_inventory(entity_type):
    inventory = api.get('/users/%s/inventory' % USERNAME)['inventory']
    vdc_uuid = ''
    for i in inventory:
        vdcs = i['entities'][entity_type]
        for vdc in vdcs:
            if vdc_uuid == '':
                vdc_uuid = vdc['uuid']
            print(vdc['name'] + ' ' + vdc['uuid'])
    return vdc_uuid

'''
This function creates a vApp from scratch using the endpoint POST /vdcs/{vdcUuid}/actions/build-vapp. 
All of the parameters passed below are required for creating a vApp from scratch. 
After creating the vApp I get all the vApps back from the vDC to get the vApp uuid by it's unique name. 
'''
def create_scratch_vapp(vdc_uuid):
    scratch_vapp = {'name':'Example vApp Name', 'description':'example description',
                    'vms': [{'name': 'Example VM name','computer_name':'Computer-Name','ram': 2000, 'number_of_cpus': 4,
                            'cpu_cores_per_socket': 2, 'hardware_version': 11, 'operating_system_version': 'ubuntu64Guest'}]}
    build_vapp_task = api.post('/vdcs/%s/actions/build-vapp' % vdc_uuid, scratch_vapp)
    wait_for_synced_task(build_vapp_task['uuid'])
    vapps = api.get('/vdcs/%s/vapps' % vdc_uuid)
    vapp_uuid = ''
    for vapp in vapps['data']:
        if vapp['name'] == 'Example vApp Name':
            vapp_uuid = vapp['uuid']
            break
    return vapp_uuid

'''
This function deletes a vApp with the DELETE endpoint /vapps/{vappUuid}
'''
def delete_vapp(vapp_uuid):
    api.delete('/vapps/%s' % vapp_uuid)

'''
This function gets a task with the GET endpoint /tasks/{taskUuid}
'''
def get_task(task_uuid):
    return api.get('/tasks/%s' % task_uuid)

'''
This function waits for a task to sync. It waits 2 seconds between getting the task
and checking if it is synced. We need to wait for tasks to sync when doing multiple actions
on a resource so we don't try doing something that isn't possible, ie. reconfiguring properties of a VM
when it is still on. 
'''
def wait_for_synced_task(task_uuid):
    synced = False
    while not synced:
        # Wait two seconds before checking if task is synced
        time.sleep(2)
        # Get task
        task = get_task(task_uuid)
        synced = task['synced']

if __name__ == '__main__':
    main()
