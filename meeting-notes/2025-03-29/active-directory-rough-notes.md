# build a vsphere domain

## domain controller

1. build vm
2. install windows server 2022 with gui
3. rename server
4. assign static ip and related settings
5. assign proxy connections (note: internet options dialog only applies to current user)
   * a great task for someone? find a way to set proxy settings for a whole windows computer that actually works. i have some info to get you started if you're willing to look into it.
6. reboot
7. shut off ie enhanced security configuration
8. open powershell
9. test curl: `curl google.com`
10. add the active directory domain services role
11. promote server to be a dc (new forest)
12. reboot

> at this point, the domain controller no longer has a local security database. put another way, the local security database on the domain controller has been modified and is now the domain security database. you should try to get very used to this idea.

1. install dhcp
2. configure dhcp
3. add a scope
   * give it a one-second delay so it won't run over tristan's dhcp scope
   * give it options for dns and default gateway
4. in ad users and computers, create a user for yourself.
   * chris: your password is variant .*N*\w*[d]?!.*.

## workstation

1. build vm
2. use windows 10 20H2
   * i can't find a windows-11-compatible vm template on this vsphere
   * i tried the windows 10 profiles and the windows server 2022 profiles
3. "i don't have internet"
   * this will prompt you to create an account that is not tied to a microsoft.com login
   * everybody says microsoft is so evil for doing this, but ... do these people have macs? iphones? androids? thought so. ;)
   * say no to everything you can say no to.
4. set proxy settings
5. rename the workstation
6. reboot
7. join the domain
   * access work or school
   * connect
   * please wait patiently
   * alternate actions: join this device to a local active directory domain
   * give your domain user access to your workstation
     * you might want to make them an admin. just sayin.
8. reboot

> at this point, the workstation still has a local security database but it is also enlisted in the active directory security directory. this means that while you can still create and use local accounts and other resources, the use of local resources can be constrainted by active directory group policy and other elements of active directory.
>
> it's a pretty fair trade. active directory enables policy-driven network, user, and resource management for windows, linux, and linux through a single management platform. as a user, it gives you access to goodies in a way that feels familiar over time, and as an admin, it gives you a consistent model for controlling all sorts of things in a controlled, repeatable manner.
>
> <ad_trivia>
> AD is also extensible: many applications add schema extensions so that they can leverage AD for special purposes. For example, Microsoft offers special versions of AD called ADAM (AD Application Management, I believe) that authenticates users to specific applications and to authenticate users to an Azure AD domain in a way that lets you trust their identity in your linked domain (we use this at GoDaddy). I think that apps like Exchange that rely heavily on LDAP and AD sometimes add to the AD schema as well.
> </ad_triva>

## interesting things to do on your workstation

```powershell
Add-WindowsCapability -Online -Name Rsat.ActiveDirectory.DS-LDS.Tools~~~~0.0.1.0
Get-ADUser chrisleonard # use your own username

DistinguishedName : CN=chris leonard,CN=usersDC=tgwin,DC=iseage,DC=org
Enabled           : True
GivenName         : chris
Name              : chris leonard
ObjectClass       : user
ObjectGUID        : 3746a35a-923c-406d-8dac-49232629fedb
SamAccountName    : cleonard
SID               : S-1-5-21-deadedbeef-00deadco3-l0000ll0000l-13337
Surname           : leonard
UserPrincipalName : chrisleonard@tgwin.iseage.org
```

## not everything has a policy

In the AD utilities, notice that the icons for **Users** and **Computers** are different from the one used for **Domain Controllers**. Why? Glad you asked:

* Users is a **Container**. So is Computers. Containers hold objects but cannot have Group Policy applied to them.
* Domain Controllers is an **Organizational Unit** (OU). When you want to assign a policy to a group of users or computers, the best practice is to put them into a new OU and apply one or more group policies to that OU.

So what can a Group Policy Object apply to?

* **Active Directory Domains**. An entire domain can have a GPO applied to it.
* **Organizational Units**. These are the basic "folders" into which you place users and computers. They typically have a structure that means something in your organization. For example, my Distinguished Name (DN) at GoDaddy is `CN=Chris Leonard,OU=Iowa Developers,OU=Users and Groups,OU=GoDaddy,DC=jomax,DC=paholdings,DC=com`. You can see the string of OU names identifying me essentially as a developer in Iowa in the main "Users and Groups" OU within the main "GoDaddy" part of our business.
* **Active Directory Sites**. These are typically used for just what they sound like - physical locations. Consider that when you log onto a Windows AD Domain, information about you has to be exchanged between your workstation and one or more Domain Controllers (DCs), If you are in Iowa, it's relatively cheap for you to talk to a Domain Controller (DC) that's in Chicago, as opposed to one that's in Belgrade. You can use AD Sites to tell AD that these two DCs are in different physical locations, and that Belgrade is farther away from Chicago (has a higher communication cost with Chicago) compared to New York or Dallas.

And that's it! nothing else can have a Group Policy Object bound to it. However, admins can get sneaky...

* **Individual AD Users and Computers**. You can apply a GPO at a high level and then use **Security Filtering** to control who it actually applies to. For example, you might have a GPO that says that people have access to a certain part of your building. If you don't have a specific OU for these people, you can modify the security for the policy. Just make sure that these people are the only ones with the **Read** and **Apply Group Policy** permissions for that Group Policy Object.
* **WMI Filtering**. If you want to control where a GPO is used but the information to filter with is not stored in AD, it might be stored in WMI. If it is, you can build a WMI query to identify the computers to apply the policy to. Copilot gave me this as an example of how to identify Windows 10 computers if they needed a specific policy applied:

```wmi
SELECT * FROM Win32_OperatingSystem WHERE Version LIKE "10.%"
```
