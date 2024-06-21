variable "resource_group_name" {
  description = "The name of the resource group"
  default     = "terraformtesting"
}

variable "location" {
  description = "The Azure region to deploy the resources"
  default     = "East US"
}

variable "admin_username" {
  description = "Admin username for the VMs"
  default     = "adminuser"
}

variable "admin_password" {
  description = "Admin password for the VMs"
  default     = "P@ssw0rd1234!"
}