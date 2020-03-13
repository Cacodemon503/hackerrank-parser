# #---------HACKERRANK LEADERBOARDS PARSER--------#

This parser may help recruiters to get users from hackerrank.com
It's mostly focused on getting users from Russia & CIS countries, but may be easily reconfigured for getting users from other regions.
It has also a GitHub checker feature, which checks if users with the sames usernames exist on GitHub.com.
Program will prepare a csv file for you with a list of users with their names and links, which may be easily convert to excel with MS Office package.

Users in the list are ranged by a position in the leaderboard (from the top to the down grade of the list).
Program has it's own menu and built in -help module.

## Usefull Tips for SOURCE CODE

1. Script requires [python3](https://www.python.org/downloads) and [requests](https://requests.readthedocs.io/en/master).

2. Open `cmd/powershell/terminal`.

3.1. `cd ~/path to script directory` for Linux.
3.2. `cd C:\Users\path to script directory` for Windows.

4.1. `python3 ./SCRIPT-NAME.py` for Linux.
4.2. `python3 ./SCRIPT-NAME.py` for Windows.

5. Use [pyinstaller](https://www.pyinstaller.org/) to compilate it under your OS: `pyinstaller -F -i "ICON-NAME.ico" SCRIPT-NAME.py`.

## Some more tips for Windows:

[Setting the path and variables in Windows 10](https://www.computerhope.com/issues/ch000549.htm)

[Powershell Core](https://github.com/PowerShell/PowerShell)

For pwsh -- edit the PATHEXT environment variable and add the .py extension:
1. `notepad $profile`
2. `$env:PATHEXT += ";.py"`
3. Now you may execute scripts just printing it's name e.g.: `hackerrank`.

[Install Chocolately -- the package manager for Windows](https://chocolatey.org/install)

Check for the next stuff in choco, install it & turn your pwsh cli pretty much the same as linux terminal:
`wget zip unzip curl whois git grep less nano unxutils`

## Some more tips for Linux:

If you want to make your scripts be easily executable on linux:
1. Make a new empty `your-script.py` file in the directory where you want to store it with `touch your-script.py` command

2. Add `#!/usr/bin/python3` at the top of the script

3. Copy all of the code to the new file & save it

4. Run: `chmod +x your-script.py` 

5. Add a Directory with your script to `$PATH:` permanently by running the following in Terminal:`nano ~/.bashrc`

6. Add in the end of the file `PATH=$PATH:~/YOUR NEW PATH TO SCRIPT`, mark it with `##PATH##` for further needs

7. Save & exit wtih: `ctrl+O` `ctrl+X`

8. Run: `source ~/.bashrc`

9. Confirm changes: `echo $PATH`. You'll see the path to your new directory in the end of the line.

10. Now you can launch it in Terminal from every directory by running: `your-script.py` 

# #----------------------OTHER OPTIONS-----------------------#

### [LINUX APP](https://github.com/Cacodemon503/hackerrank-parser/tree/master)  

### [WIN APP](https://github.com/Cacodemon503/hackerrank-parser/tree/windows)
