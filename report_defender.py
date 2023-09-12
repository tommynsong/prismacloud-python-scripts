import logging
import os
import json
import sys
import types

from prismacloud.cli import cli_output, pass_environment
from prismacloud.cli.api import pc_api

@pass_environment

def get_inventory_vms():
    """ 
    [{
    "rrn": "",
    "stateId": "",
    "assetId": "",
    "id": "i-00000",
    "name": "",
    "accountId": "",
    "accountName": "",
    "cloudType": "aws",
    "regionId": "us-east-1",
    "regionName": "AWS Virginia",
    "service": "Amazon EC2",
    "resourceType": "Instance",
    "insertTs": "",
    "createdTs": "",
    "deleted": "False",
    "hasNetwork": "False",
    "hasExternalFinding": "False",
    "hasExternalIntegration": "False",
    "allowDrillDown": "True",
    "hasExtFindingRiskFactors": "False",
    "resourceConfigJsonAvailable": "True"
    }] 
    """
    query = "config from cloud.resource where api.name = 'gcloud-compute-instances-list' AND resource.status = Active AND json.rule = labels.dataflow_job_id does not exist and labels.goog-gke-node does not exist and labels.goog-dataproc-cluster-uuid does not exist"
    search_params = {}
    search_params["limit"] = 1000
    search_params["timeRange"]["type"] = "relative"
    search_params["timeRange"]["value"] = {}
    
    search_params["withResourceJson"] = False
    search_params["query"] = query

    result = pc_api.search_config_read(search_params=search_params)

    return result

def get_defended_vms():
    """
    [{
    "_id": "i-00000",
    "hostname": "",
    "fqdn": "",
    "imageID": "ami-0149b2da6ceec4bb0",
    "imageName": "ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-20220914",
    "arn": "arn:aws:ec2:us-east-1:",
    "architecture": "x86_64",
    "createdAt": "2022-11-10T02:06:36Z",
    "accountID": "",
    "hasDefender": "True",
    "timestamp": "2023-09-12T01:50:08.388Z",
    "collections": "['All', 'All from Prisma Cloud Resource List - Access Group (RBAC)']",
    "provider": "aws",
    "region": "us-east-1",
    "awsVPCID": "",
    "awsSubnetID": "",
    "cluster": "",
    "tags": "",
    "name": ""
    }]
    """
    query_param = "&provider=gcp&hasDefender=true"
    result = pc_api.cloud_discovery_vms(query_param)

    return result

def main():
    """
    Iterate through all dictionaries in vm_from_inventory list and compare
    value of id element  
    with value of _id elemenment in each dictionaries in the list vms_defend
    if match, pop the dictionary from the vm_from_inventory list, then
    print out the remain 
    """
    vms_from_inventory = get_inventory_vms()
    vms_defended = get_defended_vms()

    for vm in vms_from_inventory:
        for d in vms_defended:
            if vm.id == d._id:
                vms_from_inventory[].pop()
