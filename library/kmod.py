#!/usr/bin/python

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import subprocess

DOCUMENTATION = r'''
---
module: kmod

short_description: Module for managing loaded kernel modules.

version_added: "1.0"

description: This module allows for the loading and unloaded of kernel modules in Linux.

options:
    name:
        description: The name of the module whose state should be managed.
        required: true
        type: str
    state:
        description: Whether the module's final state should be 'loaded' or 'unloaded'.
        required: true
        type: str

author:
    - Zachary Green (@itbadcat)
'''

EXAMPLES = r'''
# Load a kernel module
- name: Load a Linux kernel module
    name: nameOfALKM
    state: loaded

# Unload a kernel module
- name: Unload a Linux kernel module
    name: nameOfALKM
    state: unloaded
'''

RETURN = r'''
message:
    description: The output message that modprobe generates.
    type: str
    returned: always
    sample: 'modprobe: FATAL: Module nameOfALKM not found in directory /lib/modules/5.14.0-427.22.1.el9_4.x86_64'
'''

from ansible.module_utils.basic import AnsibleModule


def run_module():
    # Valid module parameters
    module_args = dict(
        name=dict(type='str', required=True),
        state=dict(type='str', required=True)
    )

    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        message='No modules changed.'
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # CHECK TO SEE IF MODULE WOULD DO ANYTHING
    if module.check_mode:
        module.exit_json(**result)

    # do stuff here
    mods_changed = False
    valid_states = ['loaded', 'unloaded']
    if module.params['state'] not in valid_states:
        module.fail_json(msg=f'{module.params["state"]} is not a valid state for this module.', **result)

    loaded_mods = [ line.split()[0] for line in subprocess.run('lsmod', shell=True, capture_output=True).stdout.decode().splitlines()[1:] ]
    result['message'] = str(loaded_mods)

    if module.params['state'] == 'loaded' and module.params['name'] not in loaded_mods:
        process = subprocess.run(['modprobe', '--dry-run', module.params['name']], capture_output=True, text=True)
        # ONLY FAIL THE MODULE IF THE MODULE FAILS TO LOAD
        if process.returncode != 0:
            module.fail_json(msg=f'{process.stderr}')
        else:
            result['message'] = f"{process}"
            mods_changed = True

    if module.params['state'] == 'unloaded' and module.params['name'] in loaded_mods:
        process = subprocess.run(['modprobe', '--dry-run', '--remove', module.params['name']], capture_output=True, text=True)
        # ONLY FAIL THE MODULE IF THE MODULE FAILS TO UNLOAD
        if process.returncode != 0:
            module.fail_json(msg=f'{process.stderr}')
        else:
            result['message'] = f"{process}"
            mods_changed = True

    # CHECK IF MODULE LOADED OR UNLOADED. TRUE = CHANGED STATE
    if mods_changed:
        result['changed'] = True

    # successful module execution
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
