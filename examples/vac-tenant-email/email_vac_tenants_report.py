import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

import iland

# iland python SDK settings
CLIENT_ID = ''
CLIENT_SECRET = ''
USERNAME = ''
PASSWORD = ''
COMPANY_ID = ''
LOCATION_ID = ''

# Email settings
HOST = ''
PORT = ''
EMAIL_ADDRESS = ''
EMAIL_PASSWORD = ''
EMAIL_TO_SEND_TO = ''

api = iland.Api(client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
                username=USERNAME, password=PASSWORD)


def main():
    COMPANY_ID, LOCATION_ID = get_vac_company_id_and_location()
    vac_tenant_names_for_report = ['example-tenant-name']
    get_vac_tenant_report(COMPANY_ID, LOCATION_ID, vac_tenant_names_for_report)
    email_report()


'''
Get the a user's inventory and the first VAC backup location we see.
'''


def get_vac_company_id_and_location():
    inventory = api.get('/users/%s/inventory' % USERNAME)['inventory']
    for item in inventory:
        vac_locations = item['entities']['VCC_BACKUP_LOCATION']
    if len(vac_locations) > 0:
        location_split = vac_locations[0]['uuid'].split(':')
        company_id = location_split[3]
        location_id = location_split[5]
        return company_id, location_id


'''
Create a VAC tenant report by getting the specified VAC tenants for a given 
location and company
'''


def get_vac_tenant_report(company_id, location_id, tenants):
    vac_tenants = api.get(
        '/companies/%s/location/%s/vac-companies' % (company_id, location_id))[
        'data']
    tenant_report = open('vac_tenants.csv', 'w+')
    tenant_report.write(
        'name, allocated storage (GB), storage used (GB), used storage %, '
        'last active, last result, VMs protected, agents protected, insider '
        'protection')
    for tenant in vac_tenants:
        if tenant['name'] in tenants:
            # Prevent a divide by 0
            if tenant['total_storage_quota'] == 0:
                used_percentage = 0
            else:
                used_percentage = tenant['used_storage_quota'] / tenant[
                    'total_storage_quota']
            tenant_report.write('\n%s, %s, %s, %s, %s, %s,%s, %s, %s' % (
                tenant['name'], tenant['total_storage_quota'],
                tenant['used_storage_quota'], used_percentage,
                tenant['last_active'],
                tenant['last_result'], tenant['vms_backed_up'],
                tenant['agent_and_sub_tenant_count'],
                tenant['backup_protection_enabled']))


'''
Attach and email VAC tenant report
'''


def email_report():
    server = smtplib.SMTP(host=HOST, port=PORT)
    server.starttls()
    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

    msg = MIMEMultipart()
    # setup the parameters of the message
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_TO_SEND_TO
    msg['Subject'] = "VAC Tenant Report"

    # Setup the attachment
    attachment = open('vac_tenants.csv', "rb")
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition',
                    "attachment; filename= %s" % 'vac_tenants.csv')

    # Attach the attachment to the MIMEMultipart object
    msg.attach(part)

    text = msg.as_string()
    server.sendmail(EMAIL_ADDRESS, EMAIL_TO_SEND_TO, text)
    server.quit()


if __name__ == '__main__':
    main()
