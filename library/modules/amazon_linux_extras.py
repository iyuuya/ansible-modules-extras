#!/usr/bin/env python

import re
from ansible.module_utils.basic import AnsibleModule

# ==============================================================================
# Util
# ==============================================================================


def success(module, changed, msg=None):
    result = {}
    result['name'] = module.params.get('name')
    result['state'] = module.params.get('state')
    result['version'] = module.params.get('version')
    result['changed'] = changed
    if msg:
        result['msg'] = msg
    module.exit_json(**result)


def fail(module, changed, msg):
    result = {}
    result['name'] = module.params.get('name')
    result['state'] = module.params.get('state')
    result['version'] = module.params.get('version')
    result['changed'] = changed
    result['msg'] = msg
    module.fail_json(**result)


# ==============================================================================
# Command
# ==============================================================================


def enable(module):
    name = module.params.get('name')
    version = module.params.get('version')
    name_with_version = name + '=' + version
    rc, _, err = module.run_command("amazon-linux-extras enable " + name_with_version)

    if rc == 0:
        return True
    else:
        fail(module, False, err)

    return False


def disable(module):
    name = module.params.get('name')
    rc, _, err = module.run_command("amazon-linux-extras disable " + name)

    if rc == 0:
        return True
    else:
        fail(module, False, err)

    return False


# ==============================================================================
# Check
# ==============================================================================


def enabled(module):
    info = get_topic_info(module)

    if info[2] == 'enabled':
        name_and_version = info[1].split('=')
        if len(name_and_version) == 2:
            return module.params.get('version') == name_and_version[1]
        else:
            return False
        return True
    else:
        return False
    return True


def disabled(module):
    info = get_topic_info(module)
    if info[2] == 'available':
        return True
    else:
        return False


def get_topic_info(module):
    name = module.params.get('name')
    _, out, _ = module.run_command("amazon-linux-extras list")
    for line in out.splitlines():
        cols = line.strip().split()
        if re.match('^' + name + '=?', cols[1]):
            return cols
    fail(module, False, "Topic not found.")
    

# ==============================================================================
# Main
# ==============================================================================


def main():
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(required=True, type='str'),
            state=dict(required=False,
                       default='enabled',
                       choices=['enabled', 'disabled'],
                       type='str'),
            version=dict(required=False, default='latest', type='str'),
        ),
        supports_check_mode=True,
    )

    state = module.params.get('state')

    changed = False
    if state == 'enabled':
        if enabled(module):
            changed = False
        elif module.check_mode:
            changed = True
        else:
            changed = enable(module)
    elif state == 'disabled':
        if disabled(module):
            changed = False
        elif module.check_mode:
            changed = True
        else:
            changed = disable(module)
    else:
        fail(module, False, "unknown value of state")
    success(module, changed)


if __name__ == '__main__':
    main()
