# Setup LaTeX (locally) on Windows (for use in VS Code)

## 1: Ensure that a LaTeX contribution is installed on device
If not, download a LaTeX contribution: <br>
e.g. MiKTeX (https://miktex.org/)

## 2: Install "LaTeX workshop" extension in VSCODE

## 3 Check latexmk installation:
- Execute in terminal:
```
latexmk --version
```

### 3.1 In case of error: "'latexmk', is not recognized as command"
-> install latexmk via MiKTeX: <br>
- Open Miktex Console <br>
- Type 'latexmk' in search bar and click install
- Again verify installation via:
```
latexmk --version
```
## 4 Check if perl is installed:
In terminal:
```
perl -v
```

### 4.1 In case of error: " 'perl' is not recognized as an internal or external command, operable program or batch file."
-> install perl:
-Download the MSI file from strawberry perl (most popular perl version) (https://strawberryperl.com/)
-Run the installation

- Verify installation via:
perl -v

- If there's still an error (after restarting terminal), check if perl is added to SYSTEM's PATH, otherwise add it (https://www.architectryan.com/2018/03/17/add-to-the-path-on-windows-10/)

## 5: Compile a LaTeX file
If everything is properly installed a green run button "Build LaTeX project" should be visible, run it.

**Note**: 
The only relevant latex files, such as .tex files, are files present before compilation. 
Files generated after compilation, such as .aux, .log, etc., are specific to your computer and should not be tracked and added to GitHub.
To avoid this, it is good practice to add them to a .gitignore file. <br>
A **.gitignore** file, (as the name itself says) tells github which files to not add to github and thus, keep local.