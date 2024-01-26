import requests
import browser_cookie3
import json

# the purpose of the script is to add 'GROUP NAME' group to BROWSE_PROJECTS and ADD_COMMENTS permissions to the particular projects
# PLEASE MAKE SURE that projects are not associated with default or any other shared permission scheme 

cookies = browser_cookie3.chrome(domain_name='domain_name.com') #change browser name if you do not use chrome and domain name for other environment
cookies_dict = requests.utils.dict_from_cookiejar(cookies) #convert cookies to dict

projectKeys = ['SDI', 'COGNOS', 'LPC', 'SLIDEDECK', 'ECM', 'OEBS', 'LMS', 'DYNT', 'BIZTALK', 'GDPR', 'LUXLOY', 'LUXSTAFF', 'CPORT', 
                'PRPASSPORT', 'CRMIAD', 'ENTDIR', 'INV', 'TRMSYS', 'TABLEAUBI', 'CONCUR', 'CONDECO', 'HOME', 'CSBU', 'CSBUUKR', 'CSFU3', 
                'CZUP', 'ALLRIGHTS', 'FLOW', 'HRSYS', 'LUXIM', 'LUXSKILL', 'LUXABSENCE', 'LUXSPACE', 'IADL3', 'NETXMS', 'KPI3']

# function to get permission shceme for the particular project
def getProjectPermissionScheme(projectKey: str):
    projectSchemeUrl = f'https://domain_name.com/jira/rest/api/2/project/{projectKey}/permissionscheme'
    r = requests.get(projectSchemeUrl, cookies=cookies_dict)

    scheme = {
        'link': json.loads(r.text)['self'],
        'id': json.loads(r.text)['id'],
        'name':json.loads(r.text)['name']
    }

    return scheme

# function to update BROWSE_PROJECTS promission
def updateBrowseScheme(link: str):
    link = f'{link}/permission'
    payload = {
        'holder': {
            'type': 'group',
            'parameter': 'GROUP NAME'
            },
        'permission': 'BROWSE_PROJECTS'
        }
    
    r = requests.post(link, json=payload, cookies=cookies_dict)

    return r.status_code

# function to update ADD_COMMENTS promission
def updateAddCommentPermission(link: str):
    link = f'{link}/permission'

    payload = {
        'holder': {
            'type': 'group',
            'parameter': 'GROUP NAME'
            },
        'permission': 'ADD_COMMENTS'
        }

    r = requests.post(link, json=payload, cookies=cookies_dict)

    return r.status_code

failed = []
succeed = []

# doing things
for i in projectKeys:
    scheme = getProjectPermissionScheme(i)
    if scheme['id'] in succeed:
        continue
    else:
        if updateBrowseScheme(scheme['link']) != 201:
            scheme['reason'] = 'BROWSE_PROJECTS'
            failed.append(scheme)
        else:
            print(f'Browse permission in scheme "{scheme["name"]}", id - {scheme["id"]}, was updated.')
            succeed.append(scheme['id'])
        
        if updateAddCommentPermission(scheme['link']) != 201:
            scheme['reason'] = 'ADD_COMMENTS'
            failed.append(scheme)
        else:
            print(f'Add Comments permission in scheme "{scheme["name"]}", id - {scheme["id"]}, was updated.\n')
            succeed.append(scheme['id'])

#verification
if len(failed) > 0:    
    print('The following permissions schemes were not updated:')
    for i in failed:
        print(f'{i["name"]}, reason - {i["reason"]}', '\n')