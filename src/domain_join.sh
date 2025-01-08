#!/bin/bash

if [ "${EUID}" -ne "0" ]; then
    echo "Must be run as root"
    exit
fi

# Installing packages
echo "Performing updates..."

apt-get install > /dev/null ; apt-get update > /dev/null ; apt-get install > /dev/null ; apt-get upgrade -y > /dev/null ; apt-get autoremove -y > /dev/null

echo "Installing packages..."

apt-get install realmd libnss-sss libpam-sss sssd sssd-tools adcli samba-common-bin oddjob oddjob-mkhomedir packagekit 1> /dev/null

echo ""

read -p "Domain Name (example.com): " domain_name
read -p "Uppercase Domain Name (EXAMPLE.COM): " upper_domain_name
read -p "BIOS Domain Name (EXAMPLE): " bios_domain_name
read -p "Ip Address of Domain Controller (x.x.x.x): " domain_controller
read -p "Domain Administrator Account Name (administrator): " account
read -s -p "Password for Account: " password

if [ -n $account ]; then
    account="administrator"
fi

# Join the domain

echo "" ; echo "Joining domain..."

realm discover $domain_name 1> /dev/null

echo -e "[libdefaults]\n\trdns = false" > /etc/krb5.conf

echo $password | realm join -U ${account} $domain_controller 1> /dev/null

# nsswitch.conf
echo "" ; echo "Editing nsswitch.conf..."

new_nsswitch=""
for i in $(seq 1 $(wc -l < /etc/nsswitch.conf)); do
    line=$(sed "${i}q;d" /etc/nsswitch.conf)
    
    if [ -n "${line}" ]; then
        line+=" sss"
    fi

    line+="\n"
    
    new_nsswitch+=$line
done

echo -e "${new_nsswitch}" > /etc/nsswitch.conf

echo "Making backups of existing configuration (x.conf.old)..." ; echo ""

cp /etc/krb5.conf /etc/krb5.conf.old
cp /etc/sssd/sssd.conf /etc/sssd/sssd.conf.old

# krb5.conf and sssd.conf
read -p "Enter number of domain controllers [1]: " num_controller

read -p "Enter fqdn of domain controller 1 [dc1.example.com]: " domain_controller_1

hostname=$(hostname)
if [ $num_controller == "2" ]; then
    read -p "Enter fqdn of domain controller 2 [dc2.example.com]: " domain_controller_2

    krb5_conf="[libdefaults]\n\tdefault_realm = ${upper_domain_name}\n\trdns = false\n\tudp_preference_limit = 0\n\n[realms]\n\t${upper_domain_name} = {\n\t\tkdc = ${domain_controller_1}\n\t\tkdc = ${domain_controller_2}\n\t\tmaster_kdc = ${domain_controller_1}\n\t\tadmin_server = ${domain_controller_2}\n\t\tdefault_domain = ${domain_name}\n\t}"
    sssd_conf="[sssd]\ndomains = ${domain_name}\nconfig_file_version = 2\nservices = nss, pam\ndebug_level = 6\n\n[domain/${domain_name}]\ndefault_shell = /bin/bash\ncache_credentials = False\nfallback_homedir = /home/%d/%u\nuse_fully_qualified_domain_names = True\nrealmd_tags = manages-system joined-with-adcli\n\nad_server = ${domain_controller_1},${domain_controller_2}\nad_hostname=${hostname}.${domain_name}\nad_domain=${domain_name}\n\nldap_uri=ldap://${domain_controller_1}:389,ldap://${domain_controller_2}:389\nldap_backup_uri=ldap://${domain_controller_1}:389,ldap://${domain_controller_2}:389\nldap_id_mapping = True\n\nkrb5_server = ${domain_controller_1},${domain_controller_2}\nkrb5_realm = ${upper_domain_name}\nkrb5_store_password_if_offline = False\n\nid_provider = ad\naccess_provider = ad\nauth_provider = krb5\nchpass_provider = krb5\nsudo_provider = ad\n"
elif [ -n $num_controller ] || [ "1" -eq $num_controller ]; then
    krb5_conf="[libdefaults]\n\tdefault_realm = ${upper_domain_name}\n\trdns = false\n\tudp_preference_limit = 0\n\n[realms]\n\t${upper_domain_name} = {\n\t\tkdc = ${domain_controller_1}\n\t\tmaster_kdc = ${domain_controller_1}\n\t\tadmin_server = ${domain_controller_1}\n\t\tdefault_domain = ${domain_name}\n\t}"
    sssd_conf="[sssd]\ndomains = ${domain_name}\nconfig_file_version = 2\nservices = nss, pam\ndebug_level = 6\n\n[domain/${domain_name}]\ndefault_shell = /bin/bash\ncache_credentials = False\nfallback_homedir = /home/%d/%u\nuse_fully_qualified_domain_names = True\nrealmd_tags = manages-system joined-with-adcli\n\nad_server = ${domain_controller_1}\nad_hostname=${hostname}.${domain_name}\nad_domain=${domain_name}\n\nldap_uri=ldap://${domain_controller_1}:389\nldap_backup_uri=ldap://${domain_controller_1}:389\nldap_id_mapping = True\n\nkrb5_server = ${domain_controller_1}\nkrb5_realm = ${upper_domain_name}\nkrb5_store_password_if_offline = False\n\nid_provider = ad\naccess_provider = ad\nauth_provider = krb5\nchpass_provider = krb5\nsudo_provider = ad\n"
fi

echo "" ; echo "Configuring krb5.conf and sssd.conf..."

echo -e $krb5_conf > /etc/krb5.conf
echo -e $sssd_conf > /etc/sssd.conf

# Pam/make home directory
echo "Editing pam configuration..." ; echo ""

(cat /etc/pam.d/common-session ; echo -e "session required\tpam_mkhomedir.so skel=/etc/skel umask=0022") > /etc/pam.d/common-session

# Sudo
read -p "Enable sudo control via SSSD/Active Directory [y/n]: " yes_or_no

if [ $yes_or_no == "y" ] || [ $yes_or_no == "Y" ]; then
    read -p "Enter name of group to control sudo access [domain admins]:" sudoers_group_name

    if [ -n $sudoers_group_name ]; then
        sudoers_group_name="domain admins"
    fi

    sudoers_group_name="${sudoers_group_name// /\\ }"
    echo "Installing..."

    echo "" | apt-get install libsss-sudo -y 1> /dev/null

    echo "Editing sudoers..."

    chmod u+w,g+w /etc/sudoers
    (cat /etc/sudoers ; echo -e "%${sudoers_group_name}@${domain_name} ALL=(ALL) ALL") > /etc/sudoers
    chmod u-w,g-w /etc/sudoers

    echo "Editing sssd.conf..."

    sed "s/services = nss, pam/services = nss, pam, sudo/" /etc/sssd/sssd.conf > /etc/sssd/sssd.conf
fi

# SSH
echo "" ; read -p "Enable active directory access over ssh [y/n]: " yes_or_no

if [ $yes_or_no == "y" ] || [ $yes_or_no == "Y" ]; then
    sed "s/UsePAM no/UsePAM yes/" /etc/ssh/sshd_config > /etc/ssh/sshd_config
    sed "s/KdbInteractiveAuthentication no/KdbInteractiveAuthentication yes/" /etc/ssh/sshd_config > /etc/ssh/sshd_config
    sed "s/ChallengeResponseAuthentication no/ChallengeResponseAuthentication yes/" /etc/ssh/sshd_config > /etc/ssh/sshd_config
fi

# Restarting configured services
echo "Restarting Services..."

systemctl restart sssd
systemctl restart sshd
systemctl restart sssd

echo "Install and setup completed. Good luck."
