import lp_uat_jira_creds
from jira import JIRA
import requests
import browser_cookie3

#lp_uat_jira_creds.py contains Jira instance url and api token:
#url = 'http://damain_name.com/jira'
#api_token = '<token>'
# 
#PAY ATTENTION
#Before deletion make sure that all schemes are not assosiated with any projects.


#get current cookies from the browser
cookies = browser_cookie3.chrome(domain_name='damain_name.com') #change browser name if you do not use chrome and domain name for other environment
cookies_dict = requests.utils.dict_from_cookiejar(cookies) #convert cookies to dict

#connect to jira instance
jiraOptions = {'server' : lp_uat_jira_creds.url
               }
jira = JIRA(server=jiraOptions, token_auth=lp_uat_jira_creds.api_token)

schemesToDelete = {
    'permission': ['10400'],
    'notification': ['10400'],
    'security': ['10400']  
}

notDeleted = {
    'Permission': [],
    'Notification': [],
    'Security': []
}

#deleting permission schemes
k = 0
for i in schemesToDelete['permission']:
    try:
         jira.delete_permissionscheme(i)
         print(i + ' permission scheme is deleted')
         k += 1
    except Exception:
         notDeleted['perm'].append(i) 
         print(i + ' permission scheme is not deleted')
         continue
print(str(k) + ' permission schemes were deleted')
print('----------------------------')

#deleting notification shcemes
k = 0
notifSchemeUrl = 'https://damain_name.com/jira/secure/admin/DeleteNotificationScheme.jspa'
for i in schemesToDelete['notification']:
    payload = {
        'schemeId': i,
        'confirmed': 'true',
        'Delete': 'Delete',
        'atl_token': '<atl_token>'
    }

    response = requests.post(
        notifSchemeUrl,
        params=payload,
        cookies=cookies_dict
    )

    if response.status_code == 200:
        print(i + ' notification shceme is deleted')
        k += 1
    else:
        print(i + ' notification shceme is not deleted')
        notDeleted['notif'].append(i)
        continue
print(str(k) + ' notification schemes were deleted')
print('----------------------------')

#deleting issue security schemes
k = 0
securitySchemeUrl = 'https://damain_name.com/jira/secure/admin/DeleteIssueSecurityScheme.jspa'
for i in schemesToDelete['security']:
    payload = {
        'schemeId': i,
        'confirmed': 'true',
        'Delete': 'Delete',
        'atl_token': '<atl_token>'
    }

    response = requests.post(
        securitySchemeUrl,
        params=payload,
        cookies=cookies_dict
    )

    if response.status_code == 200:
        print(i + ' security shceme is deleted')
        k += 1
    else:
        print(i + ' security shceme is not deleted')
        notDeleted['sec'].append(i)
        continue
print(str(k) + ' security schemes were deleted')
print('----------------------------')

#verification
for i in notDeleted:
    if len(notDeleted[i]) > 0:
        print('The following ' + i + ' schemes were not deleted:')
        print(notDeleted[i], '\n')