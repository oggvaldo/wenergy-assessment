resource "azurerm_mssql_server" "sql_server" {
  name                         = "sqlservertestanayran"
  resource_group_name          = azurerm_resource_group.rg.name
  location                     = azurerm_resource_group.rg.location
  version                      = "12.0"
  administrator_login          = "azuretest"
  administrator_login_password = "@nyth1nGhere!"
  
}

resource "azurerm_sql_database" "sql_database" {
  name                = "sqldatabasetestanayran"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  server_name         = azurerm_mssql_server.sql_server.name
  edition             = "Basic"
  requested_service_objective_name = "Basic"
}

resource "azurerm_sql_firewall_rule" "allow_access_from_azure" {
  name                = "AllowAzureServices"
  resource_group_name = azurerm_resource_group.rg.name
  server_name         = azurerm_mssql_server.sql_server.name
  start_ip_address    = "0.0.0.0"
  end_ip_address      = "0.0.0.0"
}
