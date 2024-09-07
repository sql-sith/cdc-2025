# Contributing to this repo

The general workflow for contributing to this repo is straightforward:

1. Clone this repository to your workstation.
2. Create a new branch of the repository and check out your new branch.
3. Edit your branch as desired.
4. Stage your changes.
   - This is how you tell `git` which of your pending changes you want to actually commit.
   - In VS Code, this is when you click the `+` sign and the file(s) move from **Changes** to **Staged Changes**.
   - In `git`, you stage files with the `git add` command.
5. Commit your changes.
Take time to write a good description for your commit. This is what others will see when they look at a list of commits.
   - Be polite by keeping it brief.
     - PRETTY GOOD: Added instructions on using the VPN.
     - NOT SO GOOD: Included specific methods for connecting to and using the ISEAGE VPN and what the benefits are.
   - Make it meaningful by being specific.
     - PRETTY GOOD: Improved quality checks for Diffie-Hellman parameters
     - NOT SO GOOD: Improved parameter checking
   - For code, say what it's for. Go beyond what the code itself says.
     - PRETTY GOOD: replaced `requests` with native Python `urllib` library to minimize dependencies
   - NOT SO GOOD: switched from `requests` to `urllib`
6. Push your branch to the GitHub server.
7. Create a PR to merge your branch to the `main` branch.
8. At least one reviewer will take a look at your PR.
   - If a reviewer thinks changes should be made, they will leave a note suggesting changes.
   - You are not obliged to comply with the request, but the reviewer is not obliged to approve the PR until the conversation about the request is resolved to their satisfaction.
9. Once your PR is resolved, you can merge your PR to the main branch.
   - Please use the squash and merge strategy.
   - Do not delete the branch.
