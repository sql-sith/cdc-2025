<!-- Created by SQL Sith in 2024 --

# Links and Other Resources for Installing Elasticsearch

## Using Proxies with `git` and `gh`

`git` has its own proxy settings.

*Adapted from [stackoverflow](https://stackoverflow.com/a/19213999/1236579):*

```bash
git config --global http.proxy http://199.100.16.100:3128
git config --global https.proxy http://199.100.16.100:3128
```

`gh` can use the `HTTPS_PROXY` environment variable. See GitHub [here](https://github.com/cli/cli/discussions/7602) and [here](https://github.com/cli/cli/issues/2037).

*Specific code adapted from [this answer]()https://github.com/cli/cli/issues/2037#issuecomment-2564202627). I have not tested these solutions, but they look right.*

```bash
# bash
alias gh="HTTPS_PROXY='http://localhost:7890' gh"
```

```powershell
# pwsh
function gh_proxy {
    $originalProxy = $env:HTTPS_PROXY
    $env:HTTPS_PROXY = 'http://localhost:7890'
  
    try {
        gh.exe @Args
    } finally {
        $env:HTTPS_PROXY = $originalProxy
    }
}

Set-Alias gh gh_proxy
```
