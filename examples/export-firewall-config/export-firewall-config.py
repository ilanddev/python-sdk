import iland
import time
import json

CLIENT_ID = ''
CLIENT_SECRET = ''
USERNAME = ''
PASSWORD = ''
COMPANY_ID = ''

api = iland.Api(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, username=USERNAME, password=PASSWORD)

def main():
    export_edge_firewalls()

def export_edge_firewalls():

    # Get all the edges for a given user and company.
    edges = api.get('/users/%s/companies/%s/edges' % (USERNAME, COMPANY_ID))['data']

    # After getting all the edges, iterate through all of them and get the firewall for each.
    firewalls = []
    for edge in edges:
        # Get the uuid of the edge
        edge_uuid = edge['uuid']
        firewall = api.get('/edge-gateways/%s/firewall' % (edge_uuid))
        firewalls.append(firewall)

    # Write all the firewall configurations to a file.
    with open('firewall-configs.json', 'w') as outfile:
        json.dump(firewalls, outfile, indent=1)

if __name__ == '__main__':
    main()
