resource "azurerm_public_ip" "lb_public_ip" {
  name                = "PublicIP"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  allocation_method   = "Static"
}

resource "azurerm_lb" "the_loadbalancer" {
  name                = "myLoadBalancer"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  frontend_ip_configuration {
    name                 = "PublicIPAddress"
    public_ip_address_id = azurerm_public_ip.lb_public_ip.id
  }
}

resource "azurerm_lb_backend_address_pool" "bckendaddpool" {
  loadbalancer_id     = azurerm_lb.the_loadbalancer.id
  name                = "BackEndAddressPool"
}

resource "azurerm_lb_probe" "lb_probe" {
  loadbalancer_id     = azurerm_lb.the_loadbalancer.id
  name                = "httpProbe"
  protocol            = "Http"
  port                = 80
  request_path        = "/"
  interval_in_seconds = 5
  number_of_probes    = 2
}

resource "azurerm_lb_rule" "http_lb_rule" {
  loadbalancer_id                = azurerm_lb.the_loadbalancer.id
  name                           = "httpRule"
  protocol                       = "Tcp"
  frontend_port                  = 80
  backend_port                   = 80
  frontend_ip_configuration_name = "PublicIPAddress"
  backend_address_pool_ids        = [azurerm_lb_backend_address_pool.bckendaddpool.id]
  probe_id                       = azurerm_lb_probe.lb_probe.id
}

resource "azurerm_network_interface_backend_address_pool_association" "web_lb_association" {
  count               = 2
  network_interface_id = azurerm_network_interface.web_nic[count.index].id
  ip_configuration_name = "ConfigIPWeb"
  backend_address_pool_id   = azurerm_lb_backend_address_pool.bckendaddpool.id
}
