#### 📄 README на других языках:
- [Русский](README.md)


## Script for Automated Installation of an AF Cluster

The script allows you to deploy a PTAF PRO cluster automatically from a large number of nodes without manually configuring everything in wsc.

**How it works:**
An Ansible playbook is created, which can be run on the first base node of PTAF PRO. It executes wsc configuration commands on all nodes and prepares the cluster for AF PRO installation.

Archives with configuration and executable files are located in [RELEASES](https://github.com/kib888/ptaf-pro-conf_ansible/releases) 

## How to:

1. Fill out `AF4_conf.xlsx` without changing the filename (English and Russian versions available)

2. Run the script in the same directory where .xlsx is located (you can run it from the executable file .exe or ELF or .py).

3. The output will be 4 files:
   - `readme.txt` file with instructions on what to do
   - `AF4_conf.txt` text file for manual cluster installation as usual 
   - `playbook.yaml` file with scripts for configuring wsc and other parameters
   - `inventory.yaml` file containing cluster host information

4. For automatic installation:
   1. Assign addresses on the cluster interfaces of the nodes like this:  
      `ifconfig <interface_name> up; ip a add <IP>/<netmask> dev <interface_name>`
   2. Place the `inventory.yaml` and `playbook.yaml` files on the first base node
   3. Activate the virtual environment:  
      ```source /opt/ptaf/pywsc/bin/activate```
   4. Verify that all nodes are reachable via the cluster interfaces:  
      ```ansible all -i ./inventory.yaml -m ping```
   5. Run Ansible:  
      ```ansible-playbook -i inventory.yaml playbook.yaml```
   6. If Ansible fails at the config commit stage, you can try again:  
      ```ansible-playbook -i inventory.yaml playbook.yaml --start-at-task "Commit configuration changes"```
   7. Deactivate the virtual environment:  
      ```deactivate```
   8. Profit!

5. Then run the infrastructure, monitoring, and deployment:
   ```bash
   /var/pt/infra/current/install.sh
   /var/pt/infra/current/install.sh --action=add_monitoring
   /var/pt/ptaf-deploy/current/install.sh
   ```

If the installation completes without errors, `failed = 0`.