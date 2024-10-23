# Installation

## Linux

Note that if you are working on a Windows machine you will need to either use **Windows Subsystem for Linux**, Virtualbox, or VMware to create an instance of Linux on your machine. I personally prefer to use WSL but any of the three will work just fine. If you are on Mac or Linux then you can skip down to setup.

### WSL

Here is a link for [WSL](https://learn.microsoft.com/en-us/windows/wsl/). I am using Ubuntu 24.04 which is currently the latest, but almost any flavor will be fine.
Here is a WSL [Cheat-sheet](../Course_Docs/wsl_cheat_sheet.md) that you may find useful.

### VMWare and Virtualbox

[Video](https://youtu.be/rJ9ysibH768?si=u_dEqPVRRtGGggNa) on installing Ubuntu into VirtualBox.
[Video](https://youtu.be/ZWSoASXGYNU?si=EDkSptm8TrdySboY) on installing Ubuntu into VMWare Player.

You can download [Virtual Box](https://www.virtualbox.org/wiki/Downloads).
You can download [VMware Workstation Player](https://www.vmware.com/products/workstation-player/workstation-player-evaluation.html.html).

Then you will need to download an [Ubuntu iso](https://ubuntu.com/download) file and load it into either VMware or VirtualBox.

## Setup

1. Log into your Linux or Mac OS
2. Launch a terminal window
3. Install the following packages (see images below)
   - Install:
     - g++ (compiler) `sudo apt install g++`
     - gdb (debugger) `sudo apt install gdb`
     - vs code
   - Install as needed:
     - cmake (compile and link tooling) `sudo apt install cmake`
     - git `sudo apt install git`
4. Verify everything installed (see image below)

   ![Verify Installs](./images/verifyinstalls.png "Verify Installs")

5. To check vs code, type "code ." while in wsl or other virtual machine, and that should start vs code.
6. In you home directory, create a working directory called "dev" that you will use during this course
7. Change directory into dev
8. Create a new directory called Module1
9. Change directory into Module1
10. Create a directories called bin and src
11. Add [cpp.vscode.snippet text](https://github.com/profdblair/CSCI-207/blob/main/JSON%20Docs/cpp.vscode.snippet)
    - Go to properties in vscode, User Snippets, cpp.json and copy-paste text from cpp.vscode.snippet, save and restart vscode

**Now we are ready to start Programming C++!**
