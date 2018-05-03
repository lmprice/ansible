#!/usr/bin/python

# (c) 2018, NetApp, Inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = """
---
module: netapp_e_mgmt_interface
short_description: Configure E-Series management interfaces
description:
    - Configure the settings of an E-Series management interface
version_added: '2.6'
author: Michael Price (@lmprice)
extends_documentation_fragment:
    - netapp.eseries
options:
    controller:
        description:
            - The controller that owns the port you want to configure.
            - Controller names are represented alphabetically, with the first controller as A,
             the second as B, and so on.
            - Current hardware models have either 1 or 2 available controllers, but that is not a guaranteed hard
             limitation and could change in the future.
        required: yes
        choices:
            - A
            - B
    name:
        description:
            - The name of the port to modify the configuration of.
            - The list of choices is not necessarily comprehensive. It depends on the number of ports 
            that are present in the system.
            - The numerical value represents the interface number. Typically the base ports on the controller
             are the lowest numbered ports.
            - Required when I(ipv4) is provided.
        choices:
            - 0
            - 1
            - 2
            - 3
    ssh_enable:
        type: boolean
        description:
            - Enable ssh access to the controller for debug purposes.
            - This is a controller-level setting.
        required: no
    ipv4:
        type: 'complex'
        description:
            - Specify the ipv4 configuration.
        suboptions:
            state:
                description:
                    - When present, the provided configuration will be utilized.
                    - When absent, the IPv4 configuration will be cleared and IPv4 connectivity disabled.
                choices:
                    - present
                    - absent
                default: present
            address:
                description:
                    - The IPv4 address to assign to the interface.
                    - Should be specified in xx.xx.xx.xx form.
                    - Mutually exclusive with I(config_method=dhcp)
            subnet_mask:
                description:
                    - The subnet mask to utilize for the interface.
                    - Should be specified in xx.xx.xx.xx form.
                    - Mutually exclusive with I(config_method=dhcp)
            gateway:
                description:
                    - The IPv4 gateway address to utilize for the interface.
                    - The gateway is common for all management ports on the controller.
                    - Should be specified in xx.xx.xx.xx form.
                    - Mutually exclusive with I(config_method=dhcp)
            config_method:
                description:
                    - The configuration method type to use for this interface.
                    - dhcp is mutually exclusive with I(address), I(subnet_mask), and I(gateway).
                choices:
                    - dhcp
                    - static
                required: True
notes:
    - Check mode is supported.
"""

EXAMPLES = """
    - name: Configure the first port on the A controller
      netapp_e_mgmt_interface:
        controller: "A"
        name: "0"
        ipv4:
            config_method: static
            address: "192.168.1.100"
            subnet_mask: "255.255.255.0"
            gateway: "192.168.1.1"
        ssid: "{{ ssid }}"
        api_url: "{{ netapp_api_url }}"
        api_username: "{{ netapp_api_username }}"
        api_password: "{{ netapp_api_password }}"

    - name: Disable ipv4 connectivity for the second port on the B controller
      netapp_e_mgmt_interface:
        controller: "B"
        name: "1"
        ipv4:
            state: absent
        ssid: "{{ ssid }}"
        api_url: "{{ netapp_api_url }}"
        api_username: "{{ netapp_api_username }}"
        api_password: "{{ netapp_api_password }}"
"""

RETURN = """
msg:
    description: Success message
    returned: success
    type: string
    sample: The interface settings have been updated.
ipv4_address:
    description: The currently configured IPv4 address for the interface
    returned: on success when ipv4_config.state=present
    sample: 192.168.1.100
    type: string
"""
import json

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.netapp import request, eseries_host_argument_spec
from ansible.module_utils._text import to_native

HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json",
}


class MgmtInterface(object):
    def __init__(self):
        argument_spec = eseries_host_argument_spec()
        argument_spec.update(dict(
            controller=dict(type='str', required=True, choices=['A', 'B', 'a', 'b']),
            name=dict(type='str', required=False),
            ssh_enable=dict(type='bool', required=False),
            ipv4=dict(type='dict', required=False),
        ))

        required_together = [
            ['name', 'ipv4']
        ]

        self.module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True,
                                    required_together=required_together)
        args = self.module.params
        self.controller = args['controller'].upper()
        self.name = args['name']
        self.ipv4_config = args['ipv4']
        self.ssh_enable = args['ssh_enable']

        self.ssid = args['ssid']
        self.url = args['api_url']
        self.user = args['api_username']
        self.pwd = args['api_password']
        self.certs = args['validate_certs']

        self.check_mode = self.module.check_mode
        self.post_body = dict()

        if not self.url.endswith('/'):
            self.url += '/'

    def __call__(self, *args, **kwargs):
        pass

    def _validate_complex_params(self):
        # Validate the ipv4_config
        pass


def main():
    mgmt = MgmtInterface()
    mgmt()


if __name__ == '__main__':
    main()
