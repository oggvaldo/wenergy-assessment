# Terraform Azure Infrastructure Deployment

  

This project automates the deployment of a scalable web application infrastructure in Microsoft Azure using Terraform.

  

## Infrastructure Overview

  

The infrastructure includes the following components:

- A Virtual Network (VNet) with subnets for web, application, and database tiers.

- Two Virtual Machines (VMs) in the web tier with a Load Balancer.

- One VM in the application tier.

- An Azure SQL Database in the database tier.

- Network Security Groups (NSGs) with appropriate rules for each tier.

  

## Prerequisites

  

Before you begin, ensure you have the following:

- An Azure account.

- Azure CLI installed and authenticated.

- Terraform installed.

  

## Configuration

  

Update the `variables.tf` file with your desired configuration values. Here are some key variables you might want to set:

  

```hcl

variable "resource_group_name" {

description = "The name of the resource group"

default = "terraformtesting"

}

  

variable "location" {

description = "The Azure region to deploy the resources"

default = "East US"

}

  

variable "admin_username" {

description = "Admin username for the VMs"

default = "adminuser"

}

  

variable "admin_password" {

description = "Admin password for the VMs"

default = "P@ssw0rd1234!"

}
```
  
  

## Usage

Follow these steps to deploy the infrastructure:

  

1. Initialize Terraform:

```sh
terraform init
```

  
  

2. Plan the execution

```sh
terraform plan
```

  
  

3. Apply the configuration

```sh
terraform apply
```

  

Confirm the action when prompted by typing `yes`

  

- Destroy the Infrastructure (when no longer needed)

```sh
terraform apply
```

  

Confirm the action when prompted by typing `yes`

  

## Cost Estimate

  

The estimated monthly cost for running this infrastructure is as follows:

  

- **Virtual Machines (Standard_DS1_v2)**:

- Web VMs: 2 x $60 = $120

- App VM: 1 x $60 = $60

- **Load Balancer**: $20

- **Azure SQL Database (Basic tier)**: $5

- **Public IP Address**: $3

- **Storage (Standard_LRS)**: Approximately $5 for the three VMs

  

**Total Estimated Cost: $213 per month**

  

_Note: Costs may vary based on the Azure region and usage. This is an estimate for the East US region._

  

## File Descriptions

  

### `main.tf`

  

- This file includes the primary configuration for the provider.

  

### `resource_group.tf`

  

- This file includes the primary configuration for the resource group.

  

### `network.tf`

  

- This file includes the primary configuration for the resource group, virtual network, and subnets.

  

### `variables.tf`

  

- This file contains variable definitions to make the configuration reusable and flexible.

  

### `nsg.tf`

  

- Defines the NSGs and associated rules for each tier (web, application, database).

  

### `loadbalancers.tf`

  

- Configures the public IP, load balancer, frontend IP configurations, backend pools, and rules.

  

### `vms.tf`

  

- Defines the VM instances for the web and application tiers.

  

### `database.tf`

  

- Configures the Azure SQL Database and the necessary firewall rules.

  

### `availability_sets.tf`

  

- Defines the availability set for the web tier VMs to ensure high availability.

  

## Troubleshooting

  

If you encounter any errors, ensure:

  

- The Azure CLI is authenticated with `az login`.

- Terraform is initialized with `terraform init`.

- The Azure region and other variables are correctly set in `variables.tf`.

  

## Contributing

  

Feel free to open issues or submit pull requests if you find any bugs or have suggestions for improvements.

  

## License

  

This project is licensed under the MIT License.