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
  description = "Application URL (NodePort)."
  value       = "http://${azurerm_public_ip.this.ip_address}:${var.web_port}"
}

output "argocd_url" {
  description = "ArgoCD UI URL (NodePort, self-signed TLS)."
  value       = "https://${azurerm_public_ip.this.ip_address}:${var.argocd_port}"
}

output "argocd_password_cmd" {
  description = "Command to retrieve the initial ArgoCD admin password from the VM."
  value       = "ssh ${var.admin_username}@${azurerm_public_ip.this.ip_address} \"kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath='{.data.password}' | base64 -d\""
}

output "validation_steps" {
  description = "Post-deploy verification commands."
  value = [
    "ssh ${var.admin_username}@${azurerm_public_ip.this.ip_address} 'kubectl get nodes'",
    "ssh ${var.admin_username}@${azurerm_public_ip.this.ip_address} 'kubectl get pods -A'",
    "curl http://${azurerm_public_ip.this.ip_address}:${var.web_port}/health",
  ]
}
