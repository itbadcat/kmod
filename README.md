# kmod - An Ansible module for EL9

### Description
This module, based on the provided module template, enables Ansible to manage the loaded state of kernel modules in RHEL-like distros.

### Requirements
- Ensure that lsmod, modprobe, and ansible are available locally.

### Installation
- Clone the repo.

### Usage
1. Quick and dirty version (executing on local machine without permanently installing module):
- ```cd <PROECT ROOT>; ANSIBLE_LIBRARY=./library ansible -m kmod -a 'name=<MODULE NAME> state=loaded' localhost```
