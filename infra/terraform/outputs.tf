output "resource_group_name" {
  description = "Created resource group name."
  value       = azurerm_resource_group.this.name
}

output "public_ip_address" {
  description = "Public IP address of the VM."
  value       = azurerm_public_ip.this.ip_address
}

output "vm_name" {
  description = "Linux VM name."
  value       = azurerm_linux_virtual_machine.this.name
}

output "ssh_command" {
  description = "Convenience SSH command."
  value       = "ssh ${var.admin_username}@${azurerm_public_ip.this.ip_address}"
}

output "app_url" {
  description = "Application URL based on selected web port."
  value       = "http://${azurerm_public_ip.this.ip_address}:${var.web_port}"
}

output "validation_steps" {
  description = "Post-deploy checks for SSH, web, and containers."
  value = [
    "ssh ${var.admin_username}@${azurerm_public_ip.this.ip_address}",
    "ssh ${var.admin_username}@${azurerm_public_ip.this.ip_address} \"docker ps\"",
    "curl http://${azurerm_public_ip.this.ip_address}:${var.web_port}",
  ]
}
