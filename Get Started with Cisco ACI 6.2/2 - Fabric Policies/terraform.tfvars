#### APIC LOGIN INFORMATION
# It is not best practice to configure credentials in a plain text file. 
# We're going export our creds as an environmental variable via the terminal.
# Please ensure the username/password values match the credentials provided by the guide. 
####

### APIC CREDENTIALS
# export TF_VAR_apic_username='USERNAME_FROM_DEMO_GUIDE'
# export TF_VAR_apic_password='PASSWORD_FROM_DEMO_GUIDE'

### APIC URL
apic_url      = "https://198.18.133.200" # This statically defines the URL for the APIC in the demo

#### vCenter LOGIN INFORMATION
# Note that these are normal env. variables, and not Terraform specific
# More info can be found here: https://netascode.cisco.com/docs/guides/deployment/secrets_management/
####

### VCENTER CREDENTIALS
# export vcenter_username='USERNAME_FROM_DEMO_GUIDE'
# export vcenter_password='PASSWORD_FROM_DEMO_GUIDE'