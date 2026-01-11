#!/usr/bin/env python3
"""
Dynamic Ansible inventory script that reads Terraform outputs.

This script reads Terraform outputs and generates an Ansible-compatible JSON inventory.
VMs are grouped under the 'vms' group.

Usage:
    ansible-inventory -i terraform.py --list
    ansible-playbook -i terraform.py playbooks/vm-base.yml --limit vms

Requirements:
    - Terraform must be initialized and outputs available
    - Run from repository root or set TERRAFORM_DIR environment variable
"""

import json
import os
import subprocess
import sys


def get_terraform_outputs(terraform_dir=None):
    """Get Terraform outputs as JSON."""
    if terraform_dir is None:
        terraform_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'terraform')
    
    if not os.path.exists(terraform_dir):
        return None
    
    try:
        # Get Terraform outputs as JSON
        result = subprocess.run(
            ['terraform', 'output', '-json'],
            cwd=terraform_dir,
            capture_output=True,
            text=True,
            check=False
        )
        
        if result.returncode != 0:
            # Terraform outputs not available (not initialized or no outputs)
            return None
        
        return json.loads(result.stdout)
    except (subprocess.SubprocessError, json.JSONDecodeError, FileNotFoundError):
        return None


def generate_inventory(terraform_outputs):
    """Generate Ansible inventory from Terraform outputs."""
    inventory = {
        '_meta': {
            'hostvars': {}
        },
        'vms': {
            'hosts': [],
            'vars': {
                'ansible_user': None,  # Will be set from first VM
                'ansible_port': 22,
                'ansible_ssh_common_args': '-o StrictHostKeyChecking=accept-new'
            }
        },
        'all': {
            'children': ['vms']
        }
    }
    
    if not terraform_outputs or 'vms' not in terraform_outputs:
        return inventory
    
    vms_output = terraform_outputs['vms'].get('value', {})
    
    for vm_name, vm_data in vms_output.items():
        # Add VM to vms group
        inventory['vms']['hosts'].append(vm_name)
        
        # Set host variables
        ansible_host = vm_data.get('ansible_host', '')
        ssh_user = vm_data.get('ssh_user', 'admin')
        
        # Skip if ansible_host is a placeholder
        if ansible_host.startswith('<') and ansible_host.endswith('>'):
            # Placeholder detected - skip this VM or use name as fallback
            inventory['_meta']['hostvars'][vm_name] = {
                'ansible_host': vm_name,
                'ansible_user': ssh_user,
                'ansible_port': 22,
                'ansible_ssh_common_args': '-o StrictHostKeyChecking=accept-new',
                '_note': 'IP address not set - update Terraform output or use static inventory'
            }
        else:
            inventory['_meta']['hostvars'][vm_name] = {
                'ansible_host': ansible_host,
                'ansible_user': ssh_user,
                'ansible_port': 22,
                'ansible_ssh_common_args': '-o StrictHostKeyChecking=accept-new'
            }
        
        # Set default ansible_user from first VM
        if inventory['vms']['vars']['ansible_user'] is None:
            inventory['vms']['vars']['ansible_user'] = ssh_user
    
    return inventory


def main():
    """Main entry point for Ansible dynamic inventory."""
    if len(sys.argv) == 2 and sys.argv[1] == '--list':
        # Get Terraform outputs
        terraform_outputs = get_terraform_outputs()
        
        if terraform_outputs is None:
            # No Terraform outputs available - return empty inventory
            print(json.dumps({
                '_meta': {'hostvars': {}},
                'vms': {'hosts': []},
                'all': {'children': ['vms']}
            }))
            sys.exit(0)
        
        # Generate inventory
        inventory = generate_inventory(terraform_outputs)
        print(json.dumps(inventory, indent=2))
    
    elif len(sys.argv) == 2 and sys.argv[1].startswith('--host='):
        # Single host lookup (not used in this implementation)
        host = sys.argv[1].split('=', 1)[1]
        print(json.dumps({}))
    
    else:
        print("Usage: terraform.py --list", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()

