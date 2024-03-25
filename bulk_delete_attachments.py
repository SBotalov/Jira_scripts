from jira import JIRA
import sd_prod_creds as creds
import time
import os.path
import csv

# sd_prod_creds contains two lines:
#url = 'https://servicedesk.com/' - jira base URL
#token = '{token}'

jiraOptions = {'server' : creds.url
               }
jira = JIRA(server=jiraOptions, token_auth=creds.token)

jql = '''project = "Business Travel Department" AND issuetype = "Travel Support" 
        and attachmentAuthor ~ luxbpm_in  
        AND status = closed 
        and created < "2023/04/01" ORDER BY created DESC'''
fields = ['key', 'reporter', 'attachment']
issues = jira.search_issues(jql, maxResults=600, fields=fields, json_result=True) # maxResults can be changed depending on JQL, maxResults=0 will retrieve all issues

# create/open .csv file 
if os.path.isfile('Visa_Application_attachement_deletion_log.csv'): 
    f = open(f'Travel_Support_attachement_deletion_log.csv', 'a', encoding='utf-8', newline='')  
    writer = csv.writer(f, dialect='excel')
else:
    f = open(f'Travel_Support_attachement_deletion_log.csv', 'w', encoding='utf-8', newline='')  
    writer = csv.writer(f, dialect='excel')
    writer.writerow(["Issue Key", "Attachment Name", "Author"]) # write headers in csv file

start = time.perf_counter()
for issue in issues['issues']:
    print(f'Issue - {issue["key"]} ...')
    for attach in issue['fields']['attachment']:
        if 'author' in attach and attach['author']['name'] == 'luxbpm_in':
            print(f'Deleting attachment "{attach["filename"]}"...')
            jira.delete_attachment(attach['id'])
            writer.writerow([issue['key'], attach['filename'], attach['author']['name']])
        # elif issue['fields']['reporter'] and attach['author']['name'] == issue['fields']['reporter']['name']:
        #     print(f'Deleting attachment "{attach["filename"]}"...')
        #     jira.delete_attachment(attach['id'])
        #     writer.writerow([issue['key'], attach['filename'], attach['author']['name']])
        else:
            continue

end = time.perf_counter()

print(f'\nElapsed time - {end - start}')
f.close()