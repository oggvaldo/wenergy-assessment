import os
import argparse
import logging
from azure.core.exceptions import ResourceNotFoundError
from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient, models as compute_models
from azure.mgmt.network import NetworkManagementClient, models as network_models
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.sql import SqlManagementClient, models as sql_models
from azure.mgmt.storage import StorageManagementClient

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Constants for resource names
RESOURCE_GROUP_NAME = 'py-testing'
LOCATION = 'eastus'
VNET_NAME = 'pytesting-vnet'
SUBNET_NAME = 'pytesting-subnet-1'
NIC_NAME = 'pytesting-vm-nic'
VM_NAME = 'pytesting-vm'
SQL_SERVER_NAME = 'pytestingbr1-sql-server'
DATABASE_NAME = 'pytestingbr1-database'
STORAGE_ACCOUNT_NAME = 'pytestingstorageaccount'

SUBSCRIPTION_ID = os.getenv('ARM_SUBSCRIPTION_ID')
PY_VM_USERNAME = 'pyvmtest'
PY_VM_PASSWORD = os.getenv('VM_PASSWORD')
PY_SQL_SERVER_PASSWORD = os.getenv('SQL_PASSWORD')

def _create_or_update_resource_group(resource_client):
    """Creates or updates the resource group."""
    logging.info("Ensuring resource group '%s'...", RESOURCE_GROUP_NAME)
    resource_client.resource_groups.create_or_update(
        RESOURCE_GROUP_NAME, {'location': LOCATION}
    )
    logging.info("Resource group '%s' ensured.", RESOURCE_GROUP_NAME)

def _create_or_update_vnet(network_client):
    """Creates or updates the virtual network."""
    logging.info("Ensuring virtual network '%s'...", VNET_NAME)
    try:
        network_client.virtual_networks.get(RESOURCE_GROUP_NAME, VNET_NAME)
        logging.info("Virtual network '%s' found.", VNET_NAME)
    except ResourceNotFoundError:
        vnet_params = network_models.VirtualNetwork(
            location=LOCATION,
            address_space=network_models.AddressSpace(address_prefixes=['10.0.0.0/16'])
        )
        network_client.virtual_networks.begin_create_or_update(
            RESOURCE_GROUP_NAME, VNET_NAME, vnet_params
        ).result()
        logging.info("Virtual network '%s' created.", VNET_NAME)

def _create_or_update_subnet(network_client):
    """Creates or updates the subnet."""
    logging.info("Ensuring subnet '%s'...", SUBNET_NAME)
    try:
        network_client.subnets.get(RESOURCE_GROUP_NAME, VNET_NAME, SUBNET_NAME)
        logging.info("Subnet '%s' found.", SUBNET_NAME)
    except ResourceNotFoundError:
        subnet_params = network_models.Subnet(address_prefix='10.0.0.0/24')
        network_client.subnets.begin_create_or_update(
            RESOURCE_GROUP_NAME, VNET_NAME, SUBNET_NAME, subnet_params
        ).result()
        logging.info("Subnet '%s' created.", SUBNET_NAME)

def _create_or_update_network_interface(network_client):
    """Creates or updates the network interface."""
    logging.info("Ensuring network interface '%s'...", NIC_NAME)
    try:
        network_client.network_interfaces.get(RESOURCE_GROUP_NAME, NIC_NAME)
        logging.info("Network interface '%s' found.", NIC_NAME)
    except ResourceNotFoundError:
        subnet = network_client.subnets.get(RESOURCE_GROUP_NAME, VNET_NAME, SUBNET_NAME)
        nic_params = network_models.NetworkInterface(
            location=LOCATION,
            ip_configurations=[
                network_models.NetworkInterfaceIPConfiguration(
                    name='ipconfig1', subnet={'id': subnet.id}
                )
            ],
        )
        network_client.network_interfaces.begin_create_or_update(
            RESOURCE_GROUP_NAME, NIC_NAME, nic_params
        ).result()
        logging.info("Network interface '%s' created.", NIC_NAME)

def _create_or_update_vm(compute_client, network_client):
    """Creates or updates the virtual machine."""
    logging.info("Ensuring virtual machine '%s'...", VM_NAME)
    try:
        compute_client.virtual_machines.get(RESOURCE_GROUP_NAME, VM_NAME)
        logging.info("Virtual machine '%s' found.", VM_NAME)
    except ResourceNotFoundError:
        nic = network_client.network_interfaces.get(RESOURCE_GROUP_NAME, NIC_NAME)
        vm_params = compute_models.VirtualMachine(
            location=LOCATION,
            hardware_profile=compute_models.HardwareProfile(vm_size='Standard_DS1_v2'),
            storage_profile=compute_models.StorageProfile(
                image_reference=compute_models.ImageReference(
                    publisher='MicrosoftWindowsServer',
                    offer='WindowsServer',
                    sku='2016-Datacenter',
                    version='latest',
                )
            ),
            os_profile=compute_models.OSProfile(
                computer_name=VM_NAME,
                admin_username=PY_VM_USERNAME,
                admin_password=PY_VM_PASSWORD,
            ),
            network_profile=compute_models.NetworkProfile(
                network_interfaces=[compute_models.NetworkInterfaceReference(id=nic.id)]
            ),
        )
        compute_client.virtual_machines.begin_create_or_update(
            RESOURCE_GROUP_NAME, VM_NAME, vm_params
        ).result()
        logging.info("Virtual machine '%s' created.", VM_NAME)

def _create_or_update_sql_server(sql_client):
    """Creates or updates the SQL server."""
    logging.info("Ensuring SQL Server '%s'...", SQL_SERVER_NAME)
    try:
        sql_client.servers.get(RESOURCE_GROUP_NAME, SQL_SERVER_NAME)
        logging.info("SQL Server '%s' found.", SQL_SERVER_NAME)
    except ResourceNotFoundError:
        server_params = sql_models.Server(
            location=LOCATION,
            administrator_login='adminuser',
            administrator_login_password=PY_SQL_SERVER_PASSWORD,
            version='12.0',  # Default SQL Server version
        )
        sql_client.servers.begin_create_or_update(
            RESOURCE_GROUP_NAME, SQL_SERVER_NAME, server_params
        ).result()
        logging.info("SQL Server '%s' created.", SQL_SERVER_NAME)

def _create_or_update_sql_database(sql_client):
    """Creates or updates the SQL database."""
    logging.info("Ensuring SQL database '%s'...", DATABASE_NAME)
    sql_client.databases.begin_create_or_update(
        RESOURCE_GROUP_NAME,
        SQL_SERVER_NAME,
        DATABASE_NAME,
        {'location': LOCATION, 'sku': {'name': 'S0'}},
    ).result()
    logging.info("SQL Database '%s' ensured.", DATABASE_NAME)

def _create_or_update_storage_account(storage_client):
    """Creates or updates the storage account."""
    logging.info("Ensuring storage account '%s'...", STORAGE_ACCOUNT_NAME)
    try:
        storage_client.storage_accounts.get_properties(
            RESOURCE_GROUP_NAME, STORAGE_ACCOUNT_NAME
        )
        logging.info("Storage account '%s' found.", STORAGE_ACCOUNT_NAME)
    except ResourceNotFoundError:
        storage_account_params = {
            'location': LOCATION,
            'sku': {'name': 'Standard_RAGRS'},
            'kind': 'StorageV2',
        }
        storage_client.storage_accounts.begin_create(
            RESOURCE_GROUP_NAME, STORAGE_ACCOUNT_NAME, storage_account_params
        ).result()
        logging.info("Storage account '%s' created.", STORAGE_ACCOUNT_NAME)

def create_update_resources(resource_client, network_client, compute_client, sql_client, storage_client):
    """Creates or updates all Azure resources."""
    logging.info("Starting resource creation or update process...")
    _create_or_update_resource_group(resource_client)
    _create_or_update_vnet(network_client)
    _create_or_update_subnet(network_client)
    _create_or_update_network_interface(network_client)
    _create_or_update_vm(compute_client, network_client)
    _create_or_update_sql_server(sql_client)
    _create_or_update_sql_database(sql_client)
    _create_or_update_storage_account(storage_client)
    logging.info("Resource creation or update process completed.")

def start_vm(compute_client):
    """Starts the virtual machine."""
    logging.info("Starting VM: %s", VM_NAME)
    compute_client.virtual_machines.begin_start(RESOURCE_GROUP_NAME, VM_NAME).wait()
    logging.info("VM %s started successfully.", VM_NAME)

def stop_vm(compute_client):
    """Stops the virtual machine."""
    logging.info("Stopping VM: %s", VM_NAME)
    compute_client.virtual_machines.begin_deallocate(
        RESOURCE_GROUP_NAME, VM_NAME
    ).wait()
    logging.info("VM %s stopped successfully.", VM_NAME)

def delete_vm(compute_client):
    """Deletes the virtual machine."""
    logging.info("Deleting VM: %s", VM_NAME)
    compute_client.virtual_machines.begin_delete(RESOURCE_GROUP_NAME, VM_NAME).wait()
    logging.info("VM %s deleted successfully.", VM_NAME)

def main(action=None):
    """Main function for Azure resource management."""
    if not SUBSCRIPTION_ID:
        logging.error("ARM_SUBSCRIPTION_ID environment variable not set.")
        raise EnvironmentError("ARM_SUBSCRIPTION_ID environment variable not set.")

    logging.info("Authenticating with Azure...")
    credential = DefaultAzureCredential()

    resource_client = ResourceManagementClient(credential, SUBSCRIPTION_ID)
    compute_client = ComputeManagementClient(credential, SUBSCRIPTION_ID)
    network_client = NetworkManagementClient(credential, SUBSCRIPTION_ID)
    sql_client = SqlManagementClient(credential, SUBSCRIPTION_ID)
    storage_client = StorageManagementClient(credential, SUBSCRIPTION_ID)

    if not action:
        create_update_resources(
            resource_client, network_client, compute_client, sql_client, storage_client
        )
    elif action == 'startvm':
        start_vm(compute_client)
    elif action == 'stopvm':
        stop_vm(compute_client)
    elif action == 'deletevm':
        delete_vm(compute_client)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Azure Resource Management")
    parser.add_argument(
        'action',
        nargs='?',
        help="Action to perform on the VM (startvm, stopvm, deletevm)",
        default=None,
    )
    args = parser.parse_args()
    main(args.action)