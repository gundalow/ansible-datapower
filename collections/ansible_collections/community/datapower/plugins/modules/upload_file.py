#!/usr/bin/env python

# Copyright: (c) 2020, Your Name <YourName@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: community.datapower.create

short_description: Use for modifying various objects on IBM DataPower


version_added: "1.0.0"

description: Use for modifying configuration.

options:
    domains:
        description: List of domains to execute on.
        required: true
        type: list
    defintions:
        description: DataPower object config defined in yaml.  Determine fromat using a GET and then convert to YAML.
        required: true
        type: list of YAML dictionaries.


author:
    - Your Name (anthonyschneider)
'''

EXAMPLES = r'''
# Modify a datapower object.  This example simply disables test_domain1.  
  
  - name: Create a datapower domain(s)
    community.datapower.upload_file:
      domains:
      - default
      definitions:
      - Domain:
          name: test_domain1
          mAdminState: disabled
      
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
original_message:
    description: The original name param that was passed in.
    type: str
    returned: always
    sample: 'hello world'
message:
    description: The output message that the test module generates.
    type: str
    returned: always
    sample: 'goodbye'
my_useful_info:
    description: The dictionary containing information about your system.
    type: dict
    returned: always
    sample: {
        'foo': 'bar',
        'answer': 42,
    }
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.community.datapower.plugins.module_utils.datapower import DPUploadFile

def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        domain = dict(type='str', required=True),
        top_dir = dict(type='str', choices=['local', 'cert', 'sharedcert'], required=True),
        src = dict(type='str', required=True),
        dst = dict(type='str', required=True),
        overwrite = dict(type='bool', required=True),
        
    )
    
    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
  

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )
    
    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)
    result = dict(
        changed=False
    )

    dp_up = DPUploadFile(module)
    #dp_up.send_request()
    result['upload_file_result'] = dp_up.send_request()

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()