# git-annex special remote for Zenodo
This is a git-annex special remote for Zenodo. It allows the user to initialize a new special remote to use as a backend on Zenodo to store and/or publish. 

The backend could be defined on either the sandbox or the official Zenodo deposits. The used needs to create an access key according to the platforme before initializing the remote.


# Features
- The main program git-annex-remote-zenodo is used to create a special remote for git-annex where the used could upload files and move them around like they would do with any other git-annex remote. 
- The publishing of the Zenodo deposit is also possible with the use of the script git-annex-disableremote.py which takes care of disabling the remote locally as well as publishing the files on Zenodo and keeping copies of them on a web remote of git-annex.
- New versions of a published deposit could also be created using the program git-annex-remote-zenodo by simply choosing the option newversion=id and giving the id of the deposit we want to create a new version of.
- An archive containing the files of the deposit gets automatically stored in a Zenodo deposit once the user publishes them and this archive could be restored later using the script restore_archive.py.


# Usage
## Initializing a remote
1. Export the path to where git-annex-remote-zenodo is.
`export PATH=$PATH:path-program`
2. Make git-annex-remote-zenodo executable either by executing the following command or by simply
changing the permissions in the properties of the program (by checking the box).
`chmod +x git-annex-remote-zenodo`
3. Create a git-annex repository (https://git-annex.branchable.com/walkthrough/).
4. Initialize the remote by giving the needed information and choosing the other options.
Example: 
`git annex initremote Myproject type=external externaltype=zenodo key=ACCESS_TOKEN encryption=none`

## Disabling the remote and publishing the files on the deposit
Once the user has finished using the remote, they can disable it using the script **git-annex-disableremote.py**. This could be done by executing the program and giving it inofrmation about the deposit we want to publish. 
Example: 
`git-annex-disableremote.py -i deposit_id -k  ACCESS_TOKEN -p  path.restore_archive.py`

## Initializing a new version of a deposit
This could be done just like we would initialize a new remote but this time the user needs to specify that it's a new version of a deposit and not an empty deposit.
Example: 
`git annex initremote Myprojectv2 type=external newversion=id_olddeposit externaltype=zenodo key=ACCESS_TOKEN encryption=none` 

## Restoring an archive
When a deposit is published on Zenodo, we store an archive of the files on another Zenodo deposit and so the user could restore this archive by first retrieving the restoring file (**restore_archive.py**) from the Zenodo deposit and then executing it. The options are explained below. 
Example: 
`restore_archive.py -k ACCESS_TOKEN -o simpledownload -u sandbox` 

# Options
## When initializing the remote
Options specific to **git-annex-remote-zenodo**:
- _key_ : the access token created on the chosen platforme (either the sandbox or the official site). 
- _url_ : should be set to url=sandbox when the sandbox is used. If not, this option should not be used.
- _newversion_ : this should be set to newversion=id when the used wants to create a new version of a published deposit (id = the identifier of this deposit). This option should not be given if the user wants to create a new deposit.

General git-annex options:
- _encryption_ : 'none', 'hybrid', 'shared', 'pubkey', or 'sharedpubkey'. More information is here: https://git-annex.branchable.com/encryption/
- _keyid_ : when needed, this is used to give the gpg key for the encryption.
For other options, please visit https://git-annex.branchable.com/ 

## When publishing a deposit
These are the options given to the program **git-annex-disableremote.py** when archiving a deposit. 
- _-i_ (id=): the id of the deposit to be published.
- _-k_ (key=): the access token that's been used.
- _-f_ (file=): the path to the json file **zenodo.json** if the user wants to use it to publish. This file contains the metadata needed for publishing and an example for this file could be found in this repository. For more information on the metadata please visit: https://developers.zenodo.org/?python#representation 
- _-u_ (url=): this should be set to sandbox if the user wants to publish a depost that's stored on the sandbox. If not, this option could be omitted.
- _-p_ (path=): this should be set to the path of the script restore_archive.py so that it could be modified and uploaded to Zenodo to be used to restore the archive if needed.

## When restoring an archive
These options are given to the program **restore_archive.py** when restoring an archive.
- _-k_ (key=): the access token that's been used.
- _-u_ (url=): this should be set to sandbox if the user wants to publish a depost that's stored on the sandbox. If not, this option could be omitted.
- _-o_ (option=): The option for restoring files. It's either one of these:
	+ 'rebuildannex': Rebuild the annex so that the downloaded symbolic links point to the files.
	+ 'usegitannex': initialize a git-annex and add the restored files into it as well as store them as web remotes.
	+ 'simpledownload': download the files once we restore them by making them replace the broken symbolic links.

# Tutorial
A complete tutorial that showcases all the features of this program is available in the file **[walkthrough.org](walkthrough.org)**. It could be read through before using this remote and reexecuted to grasp the functionalities of the remote. 

You need to have the access token to Zenodo in order to execute it.

