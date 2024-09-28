# IPs in use in Iseage2

For the VMs running from [iseage2.iesage.org](iseage2.iesage.org), there need to be hard set ips.

Here are the ones currently in use.
`144.76.90.` is implied for single number ips.
Nothing in the ip means it uses DHCP.
A `!` shows that this isn't the real hostname.

| VM (hostname)       | IP                    | Owner    | Type          |
| ------------------- | --------------------- | -------- | ------------- |
| `dc1`               | `13`                  | Tristian | VM            |
| `dc2`               | `26`                  | Tristian | VM            |
| !unknown            | `39`                  | Tristian | Ubuntu VM     |
| splash              | `55`                  | Henry    | Ubuntu VM     |
| `iuab-cookie`       | `69`                  | Isaac    | Ubuntu VM     |
| `michaelubuntu`     | `113`                 | Michael  | Ubuntu VM     |
| `thisonebetterwork` | `123`                 | Aksel    | Ubuntu VM     |
| !Tristian's DHCP    | `200` through `240`   | Tristian | Dhcp Reserved |
| `bob-the-computer`  |                       | Dan      | Ubuntu VM     |
| !Router             | `254`                 | Iseage2  |               |
| !Network exit       | `199.100.16.100:3128` | Iseage2  |               |
