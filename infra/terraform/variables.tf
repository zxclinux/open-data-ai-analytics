variable "location" {
  description = "Azure region for all resources."
  type        = string
  default     = "spaincentral"
}

variable "resource_group_name" {
  description = "Resource group name."
  type        = string
  default     = "rg-open-data-ai-student"
}

variable "vm_name" {
  description = "Linux VM name."
  type        = string
  default     = "open-data-ai-vm"
}

variable "vm_size" {
  description = "VM size. k3s + ArgoCD requires at least 4 GiB RAM."
  type        = string
  default     = "Standard_B4s_v2"
}

variable "admin_username" {
  description = "Admin username for the Linux VM."
  type        = string
  default     = "azureuser"
}

variable "ssh_public_key" {
  description = "SSH public key content used for VM login."
  type        = string
}

variable "address_space" {
  description = "VNet CIDR."
  type        = string
  default     = "10.20.0.0/16"
}

variable "subnet_prefix" {
  description = "Subnet CIDR."
  type        = string
  default     = "10.20.1.0/24"
}

variable "web_port" {
  description = "NodePort exposed by the web Service and opened in NSG."
  type        = number
  default     = 30080
}

variable "argocd_port" {
  description = "ArgoCD server NodePort for UI access."
  type        = number
  default     = 30443
}

variable "repo_url" {
  description = "Git repository URL cloned by cloud-init."
  type        = string
  default     = "https://github.com/zxclinux/open-data-ai-analytics.git"
}

variable "repo_branch" {
  description = "Git branch checked out by cloud-init."
  type        = string
  default     = "monitoring"
}
