<!-- AUTH : Isaac Palmersheim -->
<!-- DATE : 28/09/2024 -->
<!-- Inspired by tutorial from StackExchange ( https://askubuntu.com/questions/1442352/migrate-ubuntu-server-from-netplan-to-networkmanager-without-disconnection-poss )-->

# Warnings
Don't use this with Netplan! Things *will* break.

# 1. Installing NetworkManager
`sudo apt install network-manager`

# 2. Configuring NetworkManger
1) run `ip a`
2) Write down/remember the device name on the second device (I.E. `ens192`)
3) run `sudo nmtui`
4) Using arrow keys, navigate to `Edit a Connection`
5) Navigate to `add`
6) Navigate to `Ethernet`
7) In `Device`, enter the device name you obtained with `ip a`
8) Navigate down and open `IPv4 CONFIGURATION` 
9) In `Addresses`, input `144.76.90.{Any number under 200 and above 1}/24`. (Refer to the table of taken IPs)
10) In `Gateway`, input `144.76.90.254`
11) Navigate to `DNS servers`
12) Enter `144.76.90.254` for the DNS server
13) Ensure `Automatically connect` is checked
14) Ensure `Available to all users` is checked
15) Navigate to `OK`
16) Navigate to `Back`
17) Navigate to `Quit`

# 3. Removing Netplan
1) Run `sudo systemctl disable systemd-networkd`
2) Run `sudo apt purge netplan.io`

# 4. Reboot system
1) Run `systemctl reboot`
OR
2) Reboot using vSphere (Just use `systemctl` man)