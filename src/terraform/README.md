This terraform module will update the sshd_config based on template param on the array of hosts in the variables.tf file


# main.tf

Root terraform module

# outputs.tf

Output (Can be used to output variables)

# sshd_config.tftpl

Template file to pass configuration to remote hosts

# variables.tf

Update with remote server hosts name, user and password.  Accepts and array of hosts to run on multiple machines