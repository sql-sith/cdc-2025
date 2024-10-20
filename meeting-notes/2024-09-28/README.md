# Ethics, Batman, and Unobtainium

Cyber Defense Club, 2024-09-28

## Meeting Notes

### AI Ethics

Dan got us started with a great conversation topic about how and where to draw the line between ethical use of AI in our schoolwork and beyond, for example in the intellectual property concepts of fair use and prior art.

This led to further discussion about the wisdom of seeking clarity whenever you don't know what your professor, manager, or other authority requires.

### Network Config

We discussed who got how far in our bronze/silver/gold/platinum/unobtainium levels. Congratulations across the board! I think everybody got a lot done over the week.

On the other hand, I'd best point out that I broke my own unobtainium implementation earlier in the week, but the breakage didn't show up until the next reboot, which was during my demo with you folks. The proper level for my VM when I showed up Saturday was probably more like coal than unobtainium. :)

### A Little Dash of Scripting

We took a quick look at a service I created to stabilize my network config.

- As a reminder for anyone looking back at this later in the year, it was my dependencies that broke after I added Ubuntu's desktop environment.
- The demonstration of the service's script did work. No matter what we did to my network config, if we ran the script afterward, it put everything back, as intended.

## Follow-up Notes

### Discussion of `.profile` and `.bashrc`

These two files are automatically run for a user when `bash` sessions begin. However, I could not remember when each one runs. After doing a little digging, I'd like to clarify this for you.

- `.profile` runs whenever you start a login session. It will invoke `.bashrc` as well.
- `.bashrc` runs for interactive non-login shells.

> Login Shell: A login shell is the shell that initiates a user session on a computer, whether through a desktop environment or a tty/pty.
>
> Additional Note: Some utilities, like su and sudo, can be explicitly told to start a new login shell. For these utilities, consult their documentation for details.

### Pulling Commands From `history` Output

This was a spot that I got stuck on in class, so I thought I'd come back to this as well. I mentioned that I always have `set -o vi` in my `.bashrc` so that whenever I'm in `bash`, I can use vim-style searching. Someone in the class mentioned that you could also pipe the output of `history` through `grep` to pull out all the commands you might be interested in.

First of all, I need to mention that `history` has search mechanisms built into it. So what I'm going to show here is just for education - or you might prefer to do it this way. I kind of do.

The problem was how to pull commands that matched a pattern out of your command history. Unfortunately, if you just tell `grep` (which is a string searching utility) to find your command in the output of `history`, you will get your command prefixed by a the command number from the history file.

> `head` and `tail` are utilities that let you look at the first or last lines of a file or of a process's output. I'm using `head --lines=10` so that the process only shows me the first ten lines of output.

```bash
chris@caerdydd:~$ history | grep ssh | head --lines=10
   25  ssh bobby@palo.area51.network
   26  ssh-keygen
   27  ll ~/.ssh
   28  cat ~/.ssh/little_bobby_tables.pub |clip.exe
   29  cat ~/.ssh/little_bobby_tables.pub
   30  cat ~/.ssh/little_bobby_tables.pub |clip.exe
   32  ssh bobby@palo.area51.network
   33  ssh -v bobby@palo.area51.network
   34  ll .ssh
   35  ssh -v bobby@palo.area51.network
```

This is OK for copying and pasting, or for viewing, but it's not good if you want to use it for scripting. So how do you pop out just the name of the command?

#### Approach 1: You think your program name is at the start of every line (and you write a bad solution)

In this case you think you can ~~cheat~~ optimize your approach a little, and tell grep to find your command name and return it along with any characters that come after it. Since the only characters that come before your program will be the digits in the line number, this will return only the command.

> In regular expressions (regex), the wildcard for "any number of any characters" is `.*`. This is similar to the `*` in the Windows `*.*` filename pattern.
>
> The `.` is a wildcard character in regex and can match any single character. In regex, if you want to specify how many times a "quantifier" after it. The quantifier `*` means "0 to unlimited times" (that is, any number of times). So `.*` is a wildcard expression that can match any character (`.`) from any number of times (`*`).

```bash
chris@caerdydd:~$ history | grep --only-matching 'ssh.*' | head --lines=10
ssh bobby@palo.area51.network
ssh-keygen
ssh
ssh/little_bobby_tables.pub |clip.exe
ssh/little_bobby_tables.pub
ssh/little_bobby_tables.pub |clip.exe
ssh bobby@palo.area51.network
ssh -v bobby@palo.area51.network
ssh
ssh -v bobby@palo.area51.network
```

While this *looks like* it did what we wanted, if you compare it to the previous output, you'll see that the commands aren't all correct. For example, line 4 says its command was `ssh` when it was really `ls ~/.ssh`. This is because we told `grep` to find our search pattern - `ssh` - and all the characters after it. It turns out this isn't a very good solution.

### Approach 2: You write a better, general solution. I say you can do better

You see the problem with **Approach 1** right away and to your credit, you write something much better. You realize that the position of your command in the command string is not a reliable indicator of where to begin reading the command string. You find a Linux utility called `cut` that can take specific columns, fields, or characters out of a line of text. This sounds perfect. You realize that all of the commands start in column 9 of the `history` output, so you figure out how to use `cut` to get rid of the first 8 columns.

```bash
chris@caerdydd:~$ history | grep ssh | cut -c8- | head --lines=10
ssh bobby@palo.area51.network
ssh-keygen
ll ~/.ssh
cat ~/.ssh/little_bobby_tables.pub |clip.exe
cat ~/.ssh/little_bobby_tables.pub
cat ~/.ssh/little_bobby_tables.pub |clip.exe
ssh bobby@palo.area51.network
ssh -v bobby@palo.area51.network
ll .ssh
ssh -v bobby@palo.area51.network
```

You've definitely made things better. Well done!

But ... is this code bullet-proof? What if somebody had a really big history size defined such that they tracked their last billion commands. This would be impactically slow for using the history file, but just ... what if. Since the largest history line numbers are going to be at least 10 digits long, the command might not start in column 9.

Can you come up with a more robust solution? Feel free to use good online sources, but come to class ready to explain what your solution does or to ask why it works.

<!-- markdownlint-disable-next-line MD026 -->
## Free Club BONUS - DHCP is Functioning! More!

Just for being a member of our club, we have a free ICERINK DHCP server available for you. Tristan's DHCP server is up and running *and* (this is the big news) it can hand out Proxy addresses automatically. It's pretty easy to get Windows and Linux Network Manager to use these proxy settings. Netplan does not integrate with it as well.

Thanks, Tristan!
