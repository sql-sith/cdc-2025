# A Look Ahead / Bash Script Debugging

Cyber Defense Club, 2024-10-05

## Looking Ahead

Those of you who've been in the club before and are paying close attention might notice that I've juggled the order of the itinerary this year.

##### Schedule

#### Linux

* Bash Scripting (done today)
* Service installation

  * SSH
  * DNS
  * Firewall

#### Windows

* Service Management
* PowerShell Scripting
* Firewall

#### International CDC

Other "extra" CDCs we've done have been outside our regular season prep. In 2022, the prep for the International CDC took from May 9 to May 22 (24 days). We should discuss whether we think we want to use this much of our schedule for the International CDC in February, but we should wait until Dan is here to make a decision.

## Today

### Isaac

Last week, we said Isaac was going to have time at the beginning of class to do ... something. Isaac, what was it, and are you ready to go?

At this point, Isaac showed us some code he had written for a database CRUD module, which means a program that can perform Create, Read, Update, and Delete operations. There was a lot of discussion, but I believe that an instructor let Isaac get credit for a full class by writing this code. It was fun to try to get him to do SQL injection on his code, but it survived our valiant attempts to take it down, so far.

Isaac may put his code up on our GitHub project for all to enjoy. :)

### Bash Script Debugging (Homework Review)

We walked through the shell script problems that are defined by the homework guide in the [2024-10-26](../2024-10-26) folder. Here are some of the things we discussed along the way:

#### ShellCheck

If you have the ShellCheck linter installed in VSCode, or if you just go out to [their website](https://shellcheck.net) and dump the code into their online form, it would have basically done the homework for you. More importantly, if you read its explanations, this site can help you understand shell programming better.

#### $Variables: To Quote or Not?

Deciding when to use quotation marks and when not to can be tricky to learn. Here are some rules of thumb:

1. Variables inside double quotes will be replaced by their values. This does not happen inside single quotes.

   ```bash
   $ myvar=hello
   $ echo "$myvar"
   hello
   $ echo '$myvar'
   $myvar
   ```
2. If you want a variable or glob to be expanded, leave it unquoted. To protect it from expansion, put double-quotes around it.

   ```bash
   # directory contents:
   $ ls
   file-01.txt  file-02.txt  file-03.txt

   # observe that the glob *.txt is
   # _not_ expanded when it is quoted:

   $ echo "*.txt"
   *.txt

   $ ls "*.txt"
   ls: cannot access '*.txt': No such file or directory

   # observe that the same glob _is_
   # expanded when it is unquoted:

   $ echo *.txt
   file-01.txt  file-02.txt  file-03.txt

   $ ls *.txt
   file-01.txt  file-02.txt  file-03.txt

   # the same logic works for variables.   
   $ myglob=*.txt

   # observe that the contents of $myglob 
   # is _not_ expanded when the variable is quoted:

   $ echo "$myglob"
   *.txt

   $ ls "$myglob"
   ls: cannot access '*.txt': No such file or directory

   # observe that the contents of the $myglob
   # _is_ expanded when it the variable is unquoted:

   $ echo $myglob
   file-01.txt file-02.txt file-03.txt file-04.txt file-05.txt

   $ ls $myglob
   file-01.txt  file-02.txt  file-03.txt  file-04.txt  file-05.txt


   ```

#### Trade-offs in coding

We talked about how sometimes, as a programmer, you need to decide where the right place is to balance desirable characteristics like robustness, correctness, and performance against other desirable characteristics like speed of development, legibility, and maintainability. Sometimes bullet-proof code can be hard to read and maintain, and might take longer to produce. But sometimes the code _has_ to be bullet-proof. On the other hand, sometimes it's OK for code to be "good enough," and in those cases issues like readability may be more important.

I gave an example of this for the `search-history.sh` script [in Zulip](https://cyberdefense.zulipchat.com/#narrow/channel/406656-random/topic/random.20tech/near/480349628). For private and ad-hoc use, our simplest solution might be the best one, but if that code were being rolled out to customers, if you click on the link, I demonstrate that it's possible that the code will break. If you expect to have many customers, your original code may quickly become "tech debt" - code you have to rewrite soon.
