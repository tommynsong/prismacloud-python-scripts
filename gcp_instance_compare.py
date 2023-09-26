import json

from pcpi import session_loader
session_managers = session_loader.load_config('creds.json')

cspm_session = session_managers[0].create_cspm_session()
cwp_session = session_managers[0].create_cwp_session()


rql = "config from cloud.resource where api.name = 'gcloud-compute-instances-list' and resource.status = Active"

payload = {
    "query": rql,
    "timeRange": {
        "relativeTimeType": "BACKWARD",
        "type": "relative",
        "value": {
            "amount": 36,
            "unit": "hour"
        }
    },
    "withResourceJson": False,
    "heuristicSearch": True
}

search_data = cspm_session.config_search_request(payload)

vms_searched = search_data['data']['items']
print()
print('Number of all VMs found:', len(vms_searched))

with open('vms_searched_dump.json', 'w') as outfile:
    json.dump(vms_searched, outfile)


#Paginate
vms_defended = []
count = 0
limit = 50
while True:
    offset = limit * count
    res = cwp_session.request('GET', '/api/v1/cloud/discovery/vms', params={'limit':limit, 'offset':offset, 'provider':'gcp', 'hasDefender':'true'})

    if not res.json():
        break

    vms_defended.extend(res.json())

    count += 1
print()
print('Number of Dedended VMs:', len(vms_defended))

with open('vms_defended_dump.json', 'w') as outfile:
    json.dump(vms_defended, outfile)

with open('vms_not_defended_dump.json', 'w') as outfile:
	vms_not_defended = vms_searched

	for d in vms_defended:
		for u in vms_not_defended:
			if d.get('_id') == u.get('id'):
				vms_not_defended.remove(u)
	print()
	print('Number of VMs not Defended:', len(vms_not_defended))
	json.dump(vms_not_defended, outfile)