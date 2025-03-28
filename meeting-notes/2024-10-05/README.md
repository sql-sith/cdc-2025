# Bash Scripting and Control of Flow

Cyber Defense Club, 2024-10-05

## Housekeeping

### Iowa State Thing Next Saturday (12-Oct)

Meet at NewBoCo before 8:00 AM.

### My GoDaddy Security Hackathon Team Didn't Win Nuttin'

... but we had fun. Also, after being asked by our security org to drum up more interest, we as a team were able to see registered participants go from almost nobody to over 100 in about one week.

Another hackathon team found a vulnerability and informed me because I was part of an Active Directory group that owned the [Vulnerable Thing]. I got to make the decision to shut it down after a quick risk assessment. It felt good to make a decision and to know that it was OK for me to do so. My boss is always encouraging me to be more directive and less suggestive.

## Scripting with Bash is the Greatest Thing

### A sample script

For reference:

```bash
#!/bin/bash
# The 
# exit if there's an error:
set -e 

# even if that error occurred in the middle of a pipeline:
set -o pipefail

# Define a function
square_number() {
    local number=$1
    local result=$((number * number))
    echo $result
    return 0
}

# Call the function and capture the returned value
number_to_square=5
squared_value=$(square_number $number_to_square)

# Use the returned value
echo "The square of $number_to_square is $squared_value."


```

### Control-of-flow examples

```bash
############################
### if/then/fi:
############################

if [[ 1 -eq 1 ]]; then
  echo "true"
  echo "so celebrate"
else
  echo "false; me so sad"
fi

############################
### for/do/done:
############################

for f in *.txt; do
  echo "I found a text file named $f."
done

############################
### while/do/done:
############################

# Initialize the counter
counter=5

# While loop to count down from 5 to 1
while [ $counter -gt 0 ]; do
    echo "Countdown: $counter"
    ((counter--))
    sleep 1
done

echo "Time's up!"

############################
### case/esac:
############################

# Get the current day of the week
day=$(date +%A)

# Case statement to print a message based on the day
case $day in
    Monday)
        echo "Start of the work week!"
        ;;
    Tuesday)
        echo "It's Tuesday. Keep going!"
        ;;
    Wednesday)
        echo "Midweek already!"
        ;;
    Thursday)
        echo "Almost there!"
        ;;
    Friday)
        echo "It's Friday! Weekend is near."
        ;;
    Saturday|Sunday)
        echo "Enjoy your weekend!"
        ;;
    *)
        echo "Unknown day: $day"
        ;;
esac

############################
### select loop:
############################

# Define the options
PS3="Please select your favorite fruit: "
options=("Apple" "Banana" "Cherry" "Quit")

# Select loop to display the menu
select fruit in "${options[@]}"; do
    case $fruit in
        "Apple")
            echo "You selected Apple."
            ;;
        "Banana")
            echo "You selected Banana."
            ;;
        "Cherry")
            echo "You selected Cherry."
            ;;
        "Quit")
            echo "Goodbye!"
            break
            ;;
        *)
            echo "Invalid option. Please try again."
            ;;
    esac
done

```

### Variables types in bash

#### Common types of variables: shell variables and environment variables

I will almost always use these terms interchangeably (sue me), but it's important to keep the difference in mind at all times.

##### TL;DR

**Shell variables** belong to the currently-executing shell only. Subshells (child processes) do not inherit these variables. You can think of them as temporary variables, or as variables with a local scope (local meaning the current shell).

```bash
$ color=red
$ echo $color
red
$ # start a subshell:
$ bash
$ echo $color
$
```

Note that in bash, you use $ when you reference a variable's value, but not when you reference its name.

**Global variables** are variables that are passed to subshells as shell parameters. For example, if process 1234 has an **environment variable** `x` equal to `123`, then any shell it spawns will inherit a **shell variable** named `x` with the value `123`.

### Working with Shell and Environment Variables

This section will show you how to create, reference, and undefine `bash` variables.

#### Creating and Using Shell Variables

##### Creating Shell Variables

Creating **shell variables** in bash is easy. Just name the variable and give it a value.

```bash
year_of_arrival=2030
```

##### Using Shell Variables

Whenever you want to reference the value held by a variable, add a `$` to the front of the variable name.

```bash
$ echo "NASA's Europa Clipper is expected to reach the Jupiter system in $year_of_arrival."
NASA's Europa Clipper is expected to reach the Jupiter system in 2030.
```

#### Creating and Using Environment Variables

##### Creating Environment Variables

To create an **environment variable**, you first create a **shell variable** and then `export` it to the list of **environment variables** for the current shell. It is possible to create and export a variable in one step.

```bash
# export an existing variable sometime after it's created:
$ first_name=Chris
$ export first_name

# create and export a variable with one command:
$ export last_name=Leonard
```

##### Using Environment Variables

You use an **environment variable** just like you would use a **shell variable**. In fact, technically, you *are* using a **shell variable** (see discussion below about **Environment Variables and Subshells**).

```bash
$ echo "Hello, $first_name, $last_name!"
Hello, Chris Leonard!
```

###### Environment Variables and Subshells

The main use of **environment variables** is to pass information to subshells. Every time a process starts another shell, that shell gets its own **environment variables**. This means that *it does not inherit the environment of its parent process*, a fact that surprises many people new to Linux process management. While this may be surprising, it is also the reason that Linux processes can run with a high degree of autonomy: they do not share any variable references with each other.

Starting a new `bash` shell loads **shell variables** from sources like `.bashrc` and `.profile`, along with copies of **environment variables**. You can tell these variables are copies, not references to the actual **environment variables**, by noticing that changes in a subshell don't affect the caller's variables. If shells accessed the actual **environment variables**, changes in one shell would propogate across all shells. Because of this behavior, you can think of a set of **environment variables** as a template used to create **shell variables** in a new shell.

```bash
# create an environment variable:
$ my_envvar=10
$ export my_envvar
$ echo "$my_envvar"
10

# start subshell
$ bash

# show that $my_envvar was inherited properly:
echo "$my_envvar"
10

# modify the value of my_envvar in the subshell:
$ my_envvar=25
$ echo "$my_envvar"
25

# exit the subshell:
$ exit

# notice that the parent shell's copy of $my_envvar did not change:
$ echo "$my_envvar"
10
```

##### Undefining variables

###### The Wrong Way

There are two common ways to undefine a variable. The first way is wrong:

```bash
$ color=red
$ echo $color
red
$ red=
$ echo $color

$ # yay, we think it worked. however, $color is still definied:
$ set|grep red
red=
```

The syntax `red=` does not undefine a variable. It merely replaces its value with the empty string ("").

###### The Right Way

The right way to undefine a variable is to use `unset`:

```bash
$ color=red
$ export red
# it's an shell variable:
$ set|grep red
color=red
# it's also an environment variable:
$ env|grep red
color=red

$ unset color

# now it's completely gone:
$ echo $color

$ set|grep red
$ env|grep red
```
