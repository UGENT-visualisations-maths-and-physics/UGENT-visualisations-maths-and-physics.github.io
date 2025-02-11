# Setup LaTeX (locally) on macOS (for use in VS Code)

## 1: Ensure that a LaTeX contribution is installed on device
If not, download a LaTeX contribution: <br>
e.g. MacTex (https://www.tug.org/mactex/mactex-download.html)

## 2: Install "LaTeX workshop" extension in VSCODE

## 3: Compile a LaTeX file
If everything is properly installed a green run button "Build LaTeX project" should be visible, run it.

**Note**: 
The only relevant latex files, such as .tex files, are files present before compilation. 
Files generated after compilation, such as .aux, .log, etc., are specific to your computer and should not be tracked and added to GitHub.
To avoid this, it is good practice to add them to a .gitignore file. <br>
A **.gitignore** file, (as the name itself says) tells github which files to not add to github and thus, keep local.


