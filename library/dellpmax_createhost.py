#!/usr/bin/python


from __future__ import absolute_import, division, print_function

__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['preview'],
                    'supported_by': 'VMAX REST API Community '
                                    'https://community.emc.com/docs/DOC-56447'
                    }
DOCUMENTATION = r'''
---
module: dellpmax_createsg

contributors: Paul Martin, Rob Mortell

software versions=ansible 2.6.2
                  python version = 2.7.15rc1 (default, Apr 15 2018,

short_description: 
    module to add new volumes to existing storage group. This module can be 
    repeated multiple times in a playbook.

notes:
    - This module has been tested against UNI 9.0.  Every effort has been 
    made to verify the scripts run with valid input.  These modules 
    are a tech preview.  Additional error handling will be added at a later 
    date, base functionality only right now.



Requirements:
    - Ansible, Python 2.7, Unisphere for PowerMax version 9.0 or higher. 
    VMAX All Flash, VMAX3, or PowerMAX storage Array



playbook options:
    unispherehost:
        description:
            - Full Qualified Domain Name or IP address of Unisphere for 
            PowerMax host.
        required:True

    universion:
        -description:
            - Integer, version of unipshere software 
            https://{HostName|IP}:8443/univmax/restapi/{version}/{resource}
            90 is the release at time of writing module.
        -required:True
    verifycert:
        description: 
            -Boolean, securitly check on ssl certificates
        required:True             

        required: True
    array_id:
        description:
            - Integer 12 Digit Serial Number of PowerMAX or VMAX array.
        required:True
    host_id:
         description:
            -  String value to denote hostname, No  Special Character 
            support except for _.  Case sensistive for REST Calls.
        required:True
    initiator_list:
        description:
            - List of Initiator WWN or IQN 
        required:True
    consistent_lun:
        description:
            - Boolean Value, specifying consistent_lun ensures LUN address 
            consistency across ports, this is not required on most modern 
            operating systems as WWN or UUID is used to Uniqely identify luns
        required:True    
    async:
        Optional Parameter to set REST call to run Asyncronously, job will 
        be submitted to job queue and executed.  Task Id will be returned in 
        JSON for lookup purposed to check job completion status. 

'''

EXAMPLES = r'''
- name: Create Host
  hosts: localhost
  connection: local
    vars:
        unispherehost: '192.168.165.63'
        universion: "90"
        verifycert: False
        user: 'smc'
        password: 'smc'
  tasks:
  - name: Add Volume to Storage Group
    dellpmax_createhost:
        unispherehost: "{{unispherehost}}"
        universion: "{{universion}}"
        verifycert: "{{verifycert}}"
        user: "{{user}}"
        password: "{{password}}"
        initiator_list:
            -10000090fa812345
            -10000090fa812346
        consistent_lun: 'True'
        hostId: "MyHostName"
'''
RETURN = r'''
'''


def main():
    changed = False
    # print (changed)
    module = AnsibleModule(
        argument_spec=dict(
            sgname=dict(type='str', required=True),
            unispherehost=dict(required=True),
            universion=dict(type='int', required=False),
            verifycert=dict(type='bool', required=True),
            user=dict(type='str', required=True),
            password=dict(type='str', required=True),
            array_id=dict(type='str', required=True),
            host_id=dict(type='str', required=True),
            initiator_list=dict(type='list', required=True),
            consistent_lun=dict(type='bool', required=True)
        )
    )
    # Make REST call to Unisphere Server and execute create Host

    payload = (
        {
            {
                "hostFlags": {
                    "disable_q_reset_on_ua": {
                        "override": False,
                        "enabled": False
                    },
                    "environ_set": {
                        "override": False,
                        "enabled": False
                    },
                    "volume_set_addressing": {
                        "override": False,
                        "enabled": False
                    },
                    "spc2_protocol_version": {
                        "override": False,
                        "enabled": True
                    },
                    "scsi_support1": {
                        "override": False,
                        "enabled": True
                    },
                    "openvms": {
                        "override": False,
                        "enabled": False
                    },
                    "avoid_reset_broadcast": {
                        "override": False,
                        "enabled": False
                    },
                    "scsi_3": {
                        "override": False,
                        "enabled": True
                    },
                    "consistent_lun": module.params['consistent_lun']
                },
                "hostId": module.params['hostId'],
                "initiatorId": [
                     module.params['initiator_list']
                ]
            }
    )

    headers = ({

        'Content-Type': 'application/json'

    })

    resource_url = "https://{}:8443/univmax/restapi/{" \
                   "}/sloprovisioning/symmetrix" \
                   "/{}/host/".format \
        (module.params['unispherehost'], module.params['universion'],
         module.params['array_id'])

    verify = module.params['verifycert']
    username = module.params['user']
    password = module.params['password']
    print(resource_url)
    open_url(url=resource_url, data=json.dumps(payload), timeout=600,
             headers=headers, method="POST",
             validate_certs=verify, url_username=username,
             url_password=password, force_basic_auth=True)

    module.exit_json(changed=True)


from ansible.module_utils.basic import *
from ansible.module_utils.urls import *

if __name__ == '__main__':
    main()


