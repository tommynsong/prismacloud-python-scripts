import json

from pcpi import session_loader
session_managers = session_loader.load_config('creds.json')

cspm_session = session_managers[0].create_cspm_session()
cwp_session = session_managers[0].create_cwp_session()


rql = "config from cloud.resource where api.name = 'gcloud-container-describe-clusters' AND resource.status = Active "

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
    "withResourceJson": True,
    "heuristicSearch": True
}

search_data = cspm_session.config_search_request(payload)

cluster_searched = search_data['data']['items']
print()
print('Number of GKE clusters found:', len(cluster_searched))

with open('cluster_searched_dump.json', 'w') as outfile:
    json.dump(cluster_searched, outfile)

cluster_defended = []
res = cwp_session.request('GET', '/api/v1/radar/container/clusters')
cluster_defended.extend(res.json())

print()
print('Number of Dedended GKE clusters:', len(cluster_defended))

with open('cluster_defended_dump.json', 'w') as outfile:
    json.dump(cluster_defended, outfile)

with open('cluster_not_defended_dump.json', 'w') as outfile:
	cluster_not_defended = cluster_searched

	for d in cluster_defended:
		for u in cluster_not_defended:
			if d.get('name') == u.get('name'):
				cluster_not_defended.remove(u)
	print()
	print('Number of GKE clusters not Defended:', len(cluster_not_defended))
	json.dump(cluster_not_defended, outfile)