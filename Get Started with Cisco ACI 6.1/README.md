[![Terraform Version](https://img.shields.io/badge/terraform-%5E1.3-blue)](https://www.terraform.io)

# ACI Network-as-Code (NaC) Demo

## Overview
The code is was created for the CISCOU-2065 presentation at Cisco Live 2025 in San Diego by Steve Sharman. 

This code has been slightly modified for use in the Cisco dCloud 'Getting Started with Cisco ACI 6.1' demo, which allows users to complete an initial configuration of an ACI deployment.

These script use Network-as-Code to configure the ACI deployment. Read more about Network-as-Code (NaC) here: https://netascode.cisco.com/

## Getting started
- Schedule the "Getting Started with Cisco ACI 6.1" demo in Cisco dCloud
- Use the NAC demo guide attached to the demo

## File Structure
The file structure of this folder is as follows:
```
├── 1 - Node Policies
│   ├── data
│   │   └── static-node-mgmt-addresses.nac.yaml
│   ├── main.tf
│   ├── terraform.tfvars
│   └── variables.tf
├── 2 - Fabric Policies
│   ├── data
│   │   └── configuration.nac.yaml
│   ├── main.tf
│   ├── terraform.tfvars
│   └── variables.tf
├── 3 - Access Policies
│   ├── data
│   │   ├── 1_pools.nac.yaml
│   │   ├── 2_domains.nac.yaml
│   │   ├── 3_policies.nac.yaml
│   │   ├── 4_policy-groups.nac.yaml
│   │   ├── 5_interface-policies.nac.yaml
│   ├── main.tf
│   ├── terraform.tfvars
│   └── variables.tf
├── 4 - Tenant Policies
│   ├── data
│   │   └── pseudoco-tenant.nac.yaml
│   ├── main.tf
│   ├── terraform.tfvars
│   └── variables.tf
```

## File Overview
- 1 - Node Policies
  - Registers 2x leaf and 2x spine switches to the APIC 
  - Configures the management IP addresses on each switch
- 2 - Fabric Policies
  - Configures global settings
  - Adds route reflectors
  - Adds banners
  - Adds NTP policiy
  - Adds DNS policy
  - Adds a VMM domain - i.e. create a new VDS on vCenter
- 3 - Access Policies
  - Adds a VLAN pool
  - Adds domain
  - Adds AAEP
  - Adds interface policies
  - Adds policy groups
  - Adds interfaces 
- 4 - Tenant Policies
  - Creates a new tenant
  - Adds a VRF
  - Adds Bridge Domains
  - Adds EPGs, ESGs
  - Configures contracts and filters
  - Configures application profiles
