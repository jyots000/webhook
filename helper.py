import requests
import os
import re
import json


def create_data(category,impact,desc,urgency,vmanage_alert_id):
    # create incident in ServiceNow
    headers = {"Content-Type":"application/json", "Accept":"application/json"}
    auth = (os.environ['SERVICENOW_USERNAME'], os.environ['SERVICENOW_PASSWORD'])
    try:
        servicenow_caller = requests.get(os.environ['SERVICENOW_INSTANCE'] + "/api/now/table/sys_user?sysparm_query=user_name%3D" + os.environ['SERVICENOW_USERNAME'], auth=auth, headers=headers).json()['result'][0]['name']
    except Exception:
        return "Cannot Get ServiceNow CallerID! Check Variables"
    ticket = {
        "caller_id": servicenow_caller,
        "impact": impact,
        "urgency": urgency,
        "category": category,
        "short_description": vmanage_alert_id,
        "description": "The full log for this alert is:  \n" + desc
    }
    try:
        create_ticket = requests.post(os.environ['SERVICENOW_INSTANCE'] + "/api/now/table/u_evtmgmt_staging_table", auth=auth, headers=headers, json=ticket)
    except Exception as e:
        return "Error on Creating ServiceNow Ticket! Check your ServiceNow settings or connectivity!"
    servicenow_raw_json = create_ticket.json()

