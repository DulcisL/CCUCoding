# Windows Subsystem for Linux Cheat-Sheet

## list available distros
`wsl --list --online`

## list installed distros
`wsl --list --verbose`

## install a specific disto
`wsl --install --distribution <distro-name>`

## set default version
`wsl --set-default-version <distro-name>`

## start wsl in home directory
`wsl ~`

## update default version to latest version
`wsl --update`

## see general information about install
`wsl --status`

## check version
`wsl --version`

## run as a specific user
`wsl --user <username>`

## terminate (stop) all running distros
`wsl --shutdown`

## terminate a specific distro
`wsl --terminate <distro-name>`

## export a snapshot of a distro to a file, defaults to tar format
`wsl --export <distro> <filename>`

## import a snapshot tar file
`wsl --import <distro> <installation> <filename>`

## unregister and uninstall a wsl distro
`wsl --unregister <distro>`

## mount a disk or device
`wsl --mount <disk-path>`

## unmount a disk or device
`wsl --unmount <disk-path>`
