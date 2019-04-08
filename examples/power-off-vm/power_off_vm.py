import iland
import time

CLIENT_ID = ''
CLIENT_SECRET = ''
USERNAME = ''
PASSWORD = ''

api = iland.Api(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, username=USERNAME, password=PASSWORD)

def main():
    vapp_uuid = print_and_get_vapp()
    vm_uuid = perform_vm_operations(vapp_uuid)
    delete_vm(vm_uuid)

'''
This function prints all the vApps a user has in their inventory.
It uses the GET endpoint /users/{username}/inventory and filters to get only vApps.
It then gets the vApp uuid of the vApp of the name provided and returns the uuid.
'''
def print_and_get_vapp():
    vapp_name = 'Example vApp Name'
    vapp_uuid = ''
    inventory = api.get('/users/%s/inventory' % USERNAME)['inventory']
    for i in inventory:
        vapps = i['entities']['IAAS_VAPP']
        for vapp in vapps:
            if vapp['name'] == vapp_name:
                vapp_uuid = vapp['uuid']
            print(vapp['name'] + ' ' + vapp['uuid'])
    return vapp_uuid

'''
This function performs power operations on a VM of the vApp we got in the previous function.
Using the POST endpoints /vms/{vmUuid}/actions/poweron and /vms/{vmUuid}/actions/poweroff we 
are able to power on and off the VM. These endpoints produce a task response that we need to 
check until they are synced.  
'''
def perform_vm_operations(vapp_uuid):
    vapp_vms = api.get('/vapps/%s/vms' % vapp_uuid)
    vm_uuid = vapp_vms['data'][0]['uuid']
    power_on_task = api.post('/vms/%s/actions/poweron' % vm_uuid)
    wait_for_synced_task(power_on_task['uuid'])
    power_off_task = api.post('/vms/%s/actions/poweroff' % vm_uuid)
    wait_for_synced_task(power_off_task['uuid'])
    return vm_uuid

'''
This function deletes a VM with the DELETE endpoint /vms/{vmUuid}
'''
def delete_vm(vm_uuid):
    api.delete('/vms/%s' % vm_uuid)

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
