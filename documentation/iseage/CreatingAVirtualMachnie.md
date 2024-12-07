# Creating a new VM

Guide Created by Aksel Rasmussen on 2024-12-17.
Taken from Tristian Ribble's explanation of the process.

> ## Before we begin
> 1. this guide assumes that you have a *Hacker Name*, i.e., a name you will choose and use while hacking. Please choose one if you haven't, and post it in the contact information Zulip Channel.
> 2. In this guide:
>   - Buttons will be shown in [Brackets]
>   - Text items will be shown in "Quotes"
>   - Text input will be shown in `monospace`.
> 3. If you don't know how to do somthing, ask! We can help.
> 4. This guide assumes we are creating
>   - A NEW virtual machine.
>   - On the playground iseage instance.
>   - For yourself.
>   - On Team 5 (School 14)
>   - With purpose, dedication, and promise that you will show it the love it deserves.
> 5. If you dislike any part of 1 or 4, turn back now.

## In the begining

...the man followed these steps to create a new virtual machine:

1. Right Click our location. In this case, "School 14"
2. Left Click "New Virtual Machine..."
3. Assuming we're actually creating a virtual machine, choose "Create a new virtual machine" and press [Next].
4. Choose a name. For our purposes in the playground, this should identify your *Hacker Name* and tell YOU which machine it is.
    - > Isaac P. suggests that you use the format `<hacker-name>-<serverOS>:<Reason for existance>`
5. Select your location again . In this case, "School 14". You may need to expand some of the folders in the center pane to find it. Once you select this, press [Next].
6. Choose your compute resource. This will be "School 14" again in this case. Once this is selected, press [Next].
7. Select a storage policy. In this case, "Highschool Storage". Press [Next] after you select it.
8. The default option is usually fine for this step. You should push [Next].
9. Choose the operating system you PLAN TO install. This will not install the system, but will tell Vsphere information that will help you. Press [Next] once you choose. This does set some defaults for step 10.
10. For these options, if you don't understand what you're doing, choose the default. Some specifics here:
    - Between 2 and 4 CPUs (inclusive) for your machine.
    - Choose a maximum of 16GB of RAM.
        - 8GB or 4GB should be good for linux machines.
        - 8GB SHOULD be enough for Windows.
    - ALWAYS choose thin disk provisioning. This is under "New Hard disk > Disk Provisioning".
        - Using thin provisioning, you should be fine making it as big as you like, but try to make it into a REASONABLE size for your purposes.
    - Remember that these are limits on your machine so that you do not consume too much resources. Restrain yourself.
11. Continuing down the options, select the "New CD/DVD drive", and set the option to "Datastore ISO File".
    1. Under the "Playground ISO Datastore", you will find your install media.
        - If you are installing windows server, choose "SERVER\_EVAL....iso" instead of "Windows\_Server....iso".
    2. Double Click your iso file, then select [OK].
    3. Under the drive, choose "Connect At Power On"
12. Now that you've configured your hardware, select [Next].
13. Double check what you have set, and choose [Finish].
14. Your machine is set up. You can now boot it to install your OS.


