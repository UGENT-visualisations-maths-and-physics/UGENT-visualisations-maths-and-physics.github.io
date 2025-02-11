# Setup Github on macOS

**Note:** statements that need to be executed in terminal are always displayed in code blocks:
```
execute statement
```
**Note:** substitute the placeholder variables in <> with your personal details.

## 1: Create github account
https://github.com/ (link account to email that you will not lose, e.g. NOT UGent email)

Video for both steps 2. and 3. : https://www.youtube.com/watch?v=cGcpVQlhbuI
## 2: Generating a new SSH key and adding it to the ssh-agent
 https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent?platform=mac
### 2.1: Generating a new SSH key
Follow the step "Generating a new SSH key" in the link.

### 2.2: Adding to the ssh-agent
Follow the step "Adding your SSH key to the ssh-agent" in the link. <br>
The config file is located in the .ssh folder, which has the path `C:\Users\<YourUsername>\.ssh`, by default. This is a hidden folder and can be made visible by pressing `Command + Shift + .`  

**Copy** this in the config file's content (with `<IdentityFileRelativePath>` by default: `~/.ssh/id_ed22519`):
```
Host github.com
    AddKeysToAgent yes
    UseKeychain yes
    IdentityFile <IdentityFileRelativePath>
```

## 3: Add (copy paste) SSH key to github account
https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account?platform=mac

## 4: Check if git is installed
Execute in terminal:
```
git --version
```

- if no error (for example a good response is "git version 2.41.0") -> everything is fine.
- otherwise -> install git: https://git-scm.com/downloads/mac (via homebrew is easy)

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