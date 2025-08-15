variable "apic_username" {
  type        = string
  description = "Username used to connect to the APIC"
}

variable "apic_password" {
  type        = string
  sensitive   = true
  description = "Password used to connect to the APIC"
}

variable "apic_url" {
  type        = string
  description = "URL of the APIC"
}