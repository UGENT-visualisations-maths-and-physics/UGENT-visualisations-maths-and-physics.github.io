# Setup Github on Windows

**Note:** statements that need to be executed in terminal are always displayed in code blocks:
```
execute statement
```
**Note:** substitute the placeholder variables in <> with your personal details.

## 1: Create github account
https://github.com/ (link account to email that you will not lose, e.g. NOT UGent email)

## 2: Generating a new SSH key and adding it to the ssh-agent
 https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent?platform=windows
### 2.1: Generating a new SSH key
Follow the step "Generating a new SSH key" in the link.

### 2.2: Adding to the ssh-agent
Follow the step "Adding your SSH key to the ssh-agent" in the link, but also perform these steps (better if you have multiple SSH keys, later). <br>
- Check the path to the .ssh folder (where it is located), by default this is `C:\Users\<YourUsername>\.ssh` we will call this path `<YourSSHPath>`.
- Open powershell as administrator (https://www.ninjaone.com/blog/open-an-elevated-powershell-prompt/#:~:text=Right%2Dclick%20on%20%E2%80%9CWindows%20PowerShell,Administrator%E2%80%9D%20in%20the%20title%20bar.)
- Execute in powershell (this creates config file):
```
New-Item -Path <YourSSHPath>\config -ItemType File -Force
```
The config file is located in the .ssh folder, which has the path `C:\Users\<YourUsername>\.ssh`, by default. 

**Copy** this in the config file's content (with `<IdentityFileRelativePath>` by default: `~/.ssh/id_ed22519`):
```
Host github.com
    Hostname github.com
    User <GithubUsername>
    IdentityFile <IdentityFileRelativePath>
```
## 3: Add (copy paste) SSH key to github account
https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account?platform=windows

## 4: Check if git is installed
Execute in terminal:
```
git --version
```

- if no error (for example a good response is "git version 2.41.0") -> everything is fine.
- otherwise -> install git: https://git-scm.com/downloads/win (git standalone installor is best option)

## 5: Setup username and email in git config file (https://docs.github.com/en/get-started/getting-started-with-git/setting-your-username-in-git):
In terminal:
```
git config --global user.name "<GithubUsername>"
```

```
git config --global user.email "<GithubEmail>"
```

These can be checked via:
```
git config --global user.name 
```

```
git config --global user.email
```

## 6. Check SSH connection: 

```
ssh -T git@github.com
```    

- If prompted:
    "Are you sure you want to continue connecting (yes/no/[fingerprint])?"
    
Enter:
```
yes
```

- Upon succes the response is:
Warning: "Permanently added 'github.com' to the list of known hosts.
Hi <GithubUsername>! You've sucessfully authenticated, but Github does not provide shell access."















