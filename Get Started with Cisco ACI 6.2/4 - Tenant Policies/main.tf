# Add the terraform provider
terraform {
  required_providers {
    aci = {
      source = "CiscoDevNet/aci"
      version = ">=2.17.0"
    }
  }
}

# Login information for the APIC
provider "aci" {
  username = var.apic_username
  password = var.apic_password
  url      = var.apic_url
}

module "aci" {
  # A link to the GitHub is here "github.com/netascode/terraform-aci-nac-aci"
  source  = "netascode/nac-aci/aci"
  version = ">=1.1.0"

  # This line points the module to the data/ directory, which is where we store our configuration
  yaml_directories = ["data"]

  # Each item here controls what the module expects to configure from the .yaml files in the data/ directory
  # The values are boolean and should be 'true' or 'false', depending on what is in the data/ directory 
  manage_access_policies    = false
  manage_fabric_policies    = false
  manage_pod_policies       = false
  manage_node_policies      = false
  manage_interface_policies = false
  manage_tenants            = true
}
