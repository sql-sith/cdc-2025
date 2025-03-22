# A First Look at Unit Tests

## SSH and Linux Services

We are deferring this topic until next week.

## Software Testing Overview

To be clear, I've never worked anyplace that does all of these things, but Co-Pilot thinks this is a good list. In the GoDaddy registrar group, we do the following testing explicitly:

* unit testing
* integration testing
* system testing
* smoke testing

Other concepts from the list below are included in our methodologies (for example, we have security reviews and code reviews that fill in for some of the other items).

* **Unit Testing** : Testing individual units or components of code to ensure they function correctly. This is the first line of defense for catching bugs.
* **Integration Testing** : Testing combined parts of an application to ensure they work together as expected. This helps catch issues that may arise when different modules interact.
* **System Testing** : Testing the entire system as a whole to verify it meets the specified requirements. This is usually done in an environment that closely mimics production.
* **Acceptance Testing** : Verifying the system against user requirements. This can include:

  * **User Acceptance Testing (UAT)** : Conducted by end-users to ensure the system meets their needs.
  * **Operational Acceptance Testing (OAT)** : Ensuring the system is ready for operational use, including backup/recovery, maintenance tasks, etc.
* **Regression Testing** : Testing existing functionality after changes to ensure that new code hasn't adversely affected the existing system.
* **Performance Testing** : Checking if the system performs well under expected or peak load conditions. This includes:
* **Load Testing** : How the system behaves under a heavy load.
* **Stress Testing** : Evaluating system performance under extreme conditions.
* **Scalability Testing** : How well the system scales with increased user load.
* **Security Testing** : Identifying vulnerabilities and ensuring that the system is secure from threats.
* **Usability Testing** : Assessing how easy and user-friendly the system is for end-users.
* **Smoke Testing** : A quick set of tests to check the basic functionality of an application. It's like a sanity check to see if the major functions work.
* **Exploratory Testing** : Simultaneous learning, test design, and test execution. Testers explore the application, often finding issues that automated tests may miss.

## Unit Testing Overview

* What is unit testing?
* What benefit justifies the effort of unit testing?
* What is test-driven development?

## Unit Testing Shell Scripts

Developers usually unit test applications but not shell scripts. However, shell scripts are easy to unit test, and any piece of code that that may undergo maintenance in the future can benefit from unit tests.

Here are some rules of thumb I have to decide whether to write unit tests for shell scripts:

* If I do something more than twice, it becomes a candidate for automation (scripting).
* If, while building a script, I find myself repeatedly testing the same things, that thing should be a unit test.
* If I know something will be tricky, I should consider test-driven development.

  * This creates a simple "definition of done" simply: it's done when it passes these tests.
  * As I discover more requirements and edge cases, I write more tests to check that those requirements and edge cases are met, and they automatically become part of my definition of done.

If I am writing anything in one of our approved application languages (Golang, Java, Python, and others), GoDaddy policy requires that I unit test it.

## Unit Testing in Bash

There are several libraries for unit testing bash scripts. Here are the first four I ran into that seemed reasonable. They all have different strengths.

* **bashunit** : A comprehensive and lightweight testing framework for Bash, focused on the development experience.
* **bunit** : A very lightweight unit testing framework for Shell scripts, similar to Java's JUnit.
* **Bach Unit Testing Framework** : Bach provides APIs to mock commands and ensures that unit tests verify the behavior of bash scripts without actually running commands.
* **ShellSpec** : A full-featured BDD unit testing framework for dash, bash, ksh, zsh, and all POSIX shells.

## Unit Testing With bashunit (ShellSpec)

First, install `bashunit` if it is not installed:

```bash
curl -s https://bashunit.typeddevs.com/install.sh | sudo bash -s /usr/sbin/
sudo chmod 755 /usr/sbin/bashunit
```

Here is a simple `bash` script we will use to build our first unit test. Save it as `math.sh`.

```bash
#!/bin/bash

add() {
  echo $(($1 + $2))
}

subtract() {
  echo $(($1 - $2))
}

```

The following script builds test cases using `bashunit`. Save it in the same folder as `math.sh` and name it `math_test.sh`.

```bash
#!/bin/bash

# Import the script to be tested
source ./math.sh

# Test the add function
test_add() {
  local result=$(add 2 3)
  assertEquals "Addition test" "5" "$result"
}

# Test the subtract function
test_subtract() {
  local result=$(subtract 5 3)
  assertEquals "Subtraction test" "2" "$result"
}

# Load bashunit
source bashunit

```

Next, make sure both scripts are executable by granting execute to the files' user (owner):

```bash
chmod u+x test.sh test_math.sh
```
