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