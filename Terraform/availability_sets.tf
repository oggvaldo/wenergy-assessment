resource "azurerm_availability_set" "web_availability_set" {
  name                = "webAvailabilitySet"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name

  platform_fault_domain_count  = 2
  platform_update_domain_count = 2
  managed                      = true
}
