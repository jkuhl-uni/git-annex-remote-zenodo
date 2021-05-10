# git-annex.

## intro git-annex.
git-annex allows managing files with git, without checking the file contents into git. While that may seem paradoxical, it is useful when dealing with files larger than git can currently easily handle, whether due to limitations in memory, time, or disk space.

## useful commands.
- creating a repository:
$ git init 
$ git annex init 

- adding files:
$ git annex add .
$ git commit -a -m added

- adding a remote (usb drive):
$ sudo mount /media/usb
$ cd /media/usb
$ git clone ~/annex
$ cd annex
$ git annex init "portable USB drive"
$ git remote add laptop ~/annex
$ cd ~/annex
$ git remote add usbdrive /media/usb/annex

- getting file content:
$ cd /media/usb/annex
$ git annex sync laptop
$ git annex get .

- syncing:
$ cd /media/usb/annex
$ git annex sync

- removing files:
$ git annex drop iso/debian.iso

## useful links.
https://git-annex.branchable.com/walkthrough/
https://git-annex.branchable.com/special_remotes/external/



# Zenodo API.
## intro Zenodo.
Zenodo is a general-purpose open-access repository developed under the European OpenAIRE program and operated by CERN. It allows researchers to deposit research papers, data sets, research software, reports, and any other research related digital artifacts.

## useful link.
https://developers.zenodo.org/#quickstart-upload


# Datalad.
## intro Datalad.
DataLad builds on top of git-annex and extends it with an intuitive command-line interface. It enables users to operate on data using familiar concepts, such as files and directories, while transparently managing data access and authorization with underlying hosting providers.

A powerful and complete Python API is also provided to enable authors of data-centric applications to bring versioning and the fearless acquisition of data into continuous integration workflows.

## additional functionalities to Git / git-annex:
- minimize the use of unique/idiosyncratic functionality.
- simplify working with repositories.
- add a range of useful concepts and functions.
- make the boundaries between repositories vanish from a user’s point of view.
- provide users with the ability to act on “virtual” file paths.

## key points:
- DataLad manages your data, but it does not host it.
- You can make DataLad publish file content to one location and afterwards automatically push an update to GitHub.
- DataLad scales to large dataset sizes.
- dataset = superdataset = subdataset unless it's registered in another dataset: sub / super.
- Converting an existing Git or git-annex repository into a DataLad dataset: 	$ datalad create -f

## exporting the content of a dataset as a ZIP archive to figshare:
Ideally figshare should be supported as a proper git annex special remote. Unfortunately, figshare does not support having directories, and can store only a flat list of files. That makes it impossible for any sensible publishing of complete datasets.
	$ datalad export-to-figshare [-h] [-d DATASET] [--missing-content {error|continue|ignore}] [--no-annex] [--article-id ID] [PATH]	(*)

## useful links.
https://handbook.datalad.org/en/latest/basics/101-180-FAQ.html
http://docs.datalad.org/en/stable/generated/man/datalad-export-to-figshare.html	 (*)
http://handbook.datalad.org/en/latest/usecases/ml-analysis.html
https://handbook.datalad.org/en/latest/beyond_basics/101-168-dvc.html


# Snakemake.
## intro Snakemake.
Snakemake is a workflow engine that provides a readable Python-based workflow definition language and a powerful execution environment that scales from single-core workstations to compute clusters without modifying the workflow.

## useful links.
https://snakemake.readthedocs.io/en/stable/
https://snakemake.readthedocs.io/en/stable/tutorial/tutorial.html#tutorial
https://www.youtube.com/watch?v=NNPBDOBHlxo&ab_channel=EdinburghGenomicsTraining

