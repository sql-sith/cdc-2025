# Executive Summary: 
Exploring Memory Safety in Critical Open Source Projects

Publication:  June  26,  2024


Cybersecurity  and  Infrastructure  Security  Agency  (CISA)
Federal  Bureau  of  Investigation  (FBI)
Australian  Signals  Directorate’s  (ASD’s)  Australian  Cyber  Security  Centre  (ACSC)
Canadian  Centre  for  Cyber  Security  (CCCS)

Original document is marked TLP:CLEAR. Disclosure is not limited and distribution is without restriction.

## Source

[Exploring Memory Safety in Critical Open Source Projects](https://www.cisa.gov/sites/default/files/2024-06/joint-guidance-exploring-memory-safety-in-critical-open-source-projects-508c.pdf)

## Methodology

Project selection was based on the OpenSSF Securing Critical Project's Working Group's list of critical projects, the OpenSSF Criticality Score, and expert input. Most of the selected projects are hosted on GitHub.

The `cloc` tool was used to identify the language or file type of each file in each of the selected projects. Memory-unsafe and 

## Sampling of Critical Open Source Projects

| Project        | Total KLoc | Unsafe KLoc | Ratio |
| -------------- | ---------: | ----------: | ----: |
| chromium       |     34,677 |      17,718 |   51% |
| linux          |     26,023 |      24,721 |   95% |
| gcc            |     10,874 |       6,814 |   63% |
| jdk            |      8,172 |       2,101 |   26% |
| node           |      7,963 |       3,602 |   45% |
| kubernetes     |      5,039 |           9 |    0% |
| mysql-server   |      4,289 |       3,589 |   84% |
| TypeScript     |      2,316 |           0 |    0% |
| Rust           |      1,747 |           6 |    0% |
| cpython        |      1,566 |         629 |   40% |
| glibc          |      1,560 |       1,328 |   85% |
| vscode         |      1,545 |           0 |    0% |
| systemd        |        906 |         588 |   65% |
| angular        |        691 |           0 |    0% |
| PowerShell     |        628 |           0 |    0% |
| tor            |        343 |         320 |   93% |
| grub           |        322 |         281 |   87% |
| curl           |        226 |         173 |   77% |
| logging-log4j2 |        214 |           0 |    0% |
| nginx          |        166 |         163 |   99% |
| ruby           |        127 |           0 |    0% |
| openvpn        |        112 |          98 |   88% |
| memcached      |         48 |          32 |   68% |
| make           |         34 |          30 |   87% |

# methodology


| Language and File Type | Languages and File Types                                                                                                                                        |
| ---------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Memory-unsafe          | Assembly, C, C++, C/C++ Header, Cython, D                                                                                                                       |
| Non-executable         | CSV, diff, HTML, INI, JavaScript Object<br />Notation (JSON), Markdown,<br />reStructuredText, Text, Web Services<br />Description, XHTML, XML, XSD, XSLT, YAML |
