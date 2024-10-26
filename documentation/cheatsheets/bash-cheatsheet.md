# Bash Cheat Sheet

## 1. Documentation

```bash
# Display manual for most commands
man <command>

    Detailed documentation for commands, programs, and functions. 
    Covers kernel builtins, most shell commands, and most external programs.

# Display help for shell builtins
help <command>

  # For example, to look up info on bash's extended test behavior:
  help [[

# Get quick help for many (not all) commands.
# If --help does not work, -h, -?, or something similar may.
<command> --help

```

## 2. Navigating the Filesystem

```bash
# Print current working directory
pwd

# Change directory
cd <directory>  # Specify the directory

cd ~

# Change to previous directory
cd -

# Change directory and remember current location
pushd <directory>

# Change back to location previously stored by using pushd
popd

```

## 3. Filesystem Basics

```bash
# List files in directory
ls
  -l long form
  -S sort by size
  -t sort by modification time
  -h human-readable sizes
  -a include hidden files
  -r reverse sort order

# Copy files
cp <source> <destination>
  -r recursive copy
  -a archive (copy recursively, saving all attributes)

# Move or rename files
mv <source> <destination>

# Delete files or directories recursively
rm <file/directory>
  -r recursive delete
  -f force (never prompt for confirmation)# Change to home directory

# Create a directory
mkdir <directory>
  -p create any missing parent directories

# Remove a directory
rmdir <directory>
  requires that the directory is empty

# Create an empty file
touch <file>

# Display file content
cat <file>

```

## 4. Redirection

### Standard Streams

**Standard Input (stdin)** : The default source of input for commands (usually the keyboard). Represented as file descriptor 0.

**Standard Output (stdout)** : The default destination for output (usually the terminal). Represented as file descriptor 1.

**Standard Error (stderr)** : The default destination for error messages (usually the terminal). Represented as file descriptor 2.

### File Redirection

* Redirecting stdout

```bash
command > file  # Overwrite file with stdout
command >> file  # Append stdout to file
```

* Redirecting stderr

```bash
command 2> file  # Overwrite file with stderr
command 2>> file  # Append stderr to file
```

* Using a file as stdin

```bash
command < file
```

* Ignore stderr

```bash
command 2> /dev/null
```

* Ignore both stderr and stdout

```bash
# In the following, the first '1' can be omitted
# but I've left it on for clarity.
command 1>/dev/null 2>&1
```

* Creating, overwriting, or appending to files using redirection

  ```bash
  # overwrite an existing file.
  # the file will be created if necessary.
  command > <filename>

  # append to an existing file.
  # the file will be created if necessary.
  command >> <filename>

  ```

## 5. Filesystem Utilities

```bash
# Display disk space usage
df
  -h human-readable sizes

# Display disk usage of files and directories
du
  -s summarize, showing only a total for each argument
  -h human-readable sizes
  -a show totals for all (including files as well as directories)

# Display file type
file <file>

# Find files
find <directory> -name <filename>
find <directory> -iname <filename-wildcard>
  much additional functionality is available.

# Create symbolic links
ln -s <target> <linkname>

# Display detailed file information
stat <file>

# Display the full path of commands
which <command>
  -a show all matches (not just the one that would be executed)

```

## 6. Working with Text

```bash
# Remove sections from each line of files
cut -d' ' -f1 <file>  # Example: cut by delimiter and field

# Search inside files
grep <pattern> <file>
  -P use Perl-Compatible Regular Expressions (PCREs)
  -r search recursively (omit <file> if you use this)
  -i case-insensitive search

# Display beginning or end of of a file
head -n <number_of_lines> <file>
tail -n <number_of_lines> <file>

# View a file with paging
more <file>
less <file>

# Sort lines of text files
sort <file>
  -k define a key to search on other than the whole line
  -t field terminator
     eg: 
       # sort myfile by the 4th comma-delimited field:
       sort -t ',' -k4 myfile 

       # same thing, but in reverse order:
       sort -t ',' -k4r myfile

       # same thing, but in human-sensible order
       # (meaning, for example, that '2' is smaller than '10')
       sort -t ',' -k4rh myfile  

# Remove duplicate lines from sorted file
uniq <file>

# Display line, word, and byte counts
wc <file>
  You can tweak the information displayed:
    --lines  display count of newlines
    --words  display count of words
    --bytes  display count of bytes
    --chars  display count of chars

```

## 7. Permissions

### Overview of Permissions

Permissions are displayed as a set of 10 characters called the file *mode*. As an example, suppose you see a output from `ls` indicating that a file has mode `-rwxr-xr-x`.

* The first character indicates the file type (- for regular file, d for directory, and so forth)
* The next three characters (rwx) are permissions for the file owner
* The next three (r-x) are permissions for the file group
* The last three (r-x) are permissions for others

### Numeric Representation of Permissions

Permissions can be set using numbers:

* Read (r) = 4
* Write (w) = 2
* Execute (x) = 1

For example, 755 means:

* Owner: Can Read, Write, and Execute (4+2+1=7)
* Group: Can Read and Execute (4+1=5)
* Others: Can Read and Execute (4+1=5)

> Note: for a directory, "Execute" means entering the directory with the `cd` command or any equivalent action.

There are other ways to manage permissions that are illustrated below. Please consult documentation for the relevant commands for more information.

```bash
# View file permissions by using ls -l
ls -l <file>

# Change file ownership
chown <owner> <file>

# Change file permissions
chmod <permissions> <file>

  # You can use numeric permissions, in which case 
  # you are replacing all existing permissions. for
  # example, to allow a file owner to read and 
  # execute it, but to allow its group and others
  # to only be able to read it, you could execute this:
  chmod 644 myfile 

  # alternatively, you can issue specific changes
  # symbolically. for example, to add the execute
  # permission to a files group, you can run this:
  chmod g+x myfile

# Display Access Control Lists (ACLs) of a file or directory
getfacl <file/directory>

# Set ACL for a user
setfacl -m u:<username>:rwx <file/directory>  # Grant read, write, execute to a user

# Remove ACL for a user
setfacl -x u:<username> <file/directory>

# Set default ACLs (for directories, new files will inherit these permissions)
setfacl -d -m u:<username>:rwx <directory>


```

## 7. System Monitoring and Management

```bash
# Print or control the kernel ring buffer
dmesg

# Query and display messages from the journal
journalctl

# Control the systemd system and service manager on systemd systems:
systemctl <command> <service>

# Manage system services on SysVinit systems:
service <service> <command>

# Set nameservers, resolve domain names, IP addresses, DNS resource records, and services
resolvectl

# Show/manipulate routing, devices, policy routing, and tunnels
ip <object-type> show
  address  shows information about IP addresses
  link     shows information about network adapters
  neigh    shows the ARP table - names/IPs/MACs of known hosts on the same network(s)
  route    shows routing table(s)

```

## 8. Scripting Basics

```bash
#!/bin/bash
# This is a comment

# Define a variable
variable="value"

# Print variable
echo $variable

# Sample function
greet() {
    local name=$1
    echo "Hello, $name!"
}

# Call the function
greet "Cyber Warriors"

# Conditional statement
if [ condition ]
then
    # commands
else
    # commands
fi

# Loop
for i in {1..5}
do
   echo "Welcome $i times"
done

```
