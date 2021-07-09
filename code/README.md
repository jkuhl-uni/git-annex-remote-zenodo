# What's in this directory.

- git-annex-remote-zenodo: this is the main program that takes care of all the needed information to create and manipulate a Zenodo git-annex remote. It can be recorded in the path and then used as a regular git-annex command to use a remote.

- tests_remote: this folder contains a few python files with tests to check the implementation of the remote. It tests basic functions of git-annex-remote-zenodo.
These tests have been made available on github by the user who created the AnnexRemote library used to implement the remote.
	+ link: https://github.com/Lykos153/AnnexRemote

- git-annex-disableremote.py: this is a function that takes care of disabling a Zenodo remote. Firstly, it publishes the content of the remote (all the files available in the deposit). Then, it turns these files into web remotes. Lastly, it disables the remote by removing it locally.

- walkthrough.org: this file is essencially a tutorial with explanations that walks you through the use of all the things that have been implemented thus far. It utilizes the git-annex-remote-zenodo program to initialize a remote and the git-annex-disableremote.py to disable it after having shown all the basic functionalities that they allow.
