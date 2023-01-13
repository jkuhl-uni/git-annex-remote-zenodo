#!/usr/bin/env python

# This program will be used when finalizing the publishing in a remote.
# by executing this command 'git-annex-disableremote', the deposit will
# be publsihed using informaion given by the user or submitted in a json
# file. The remote will also be removed locally.
# Possible options:
# - deposit_id: the id of the deposit we want to publish.
# - from-file: the zenodo.json file containing the information needed for publishing.


import sys, getopt

LICENCE = ''
EMBARGO_DATE = ''
ACCESS_CONDITIONS= ''

# method to look for the name of the remote. This is to be used when we want to remove it in disableremotelocally
# and when we want to create the archive in archiving
def get_remotename(deposit_id):
    import subprocess, shlex

    # reading the file from the other branch without checking into it
    output = subprocess.getoutput("git show git-annex:./remote.log")

    # we can have multiple remotes in one log and they are separated by lines.
    lines = output.splitlines()
    remote_name = ''
    # going through the remotes
    for line in lines:
        # parsing the output and separating the lines in a list where each element is a file
        s = shlex.split(line, comments=True, posix=False)
        # now, let's go through the list
        for elm in s:
            # looking through the elemnts for the index of the id
            if elm.startswith("deposit_id"):
                id = elm.split("=")[-1]
            # we have found the name of the remote that we are looking for
            if (elm.startswith("name")) and (id == deposit_id):
                remote_name = elm.split("=")[-1]
    return remote_name


# this function creates an archive of the files and uploads it to Zenodo so as to allow the user
# to recover the files later on if they wish to
def archiving(deposit_id, key, url, path_restorearchive):
    import tempfile, json, os, requests, subprocess, shlex 

    headers = {"Content-Type": "application/json"}
    params = {'access_token': key}

    ########### creating the info file #############################
    # getting the output from trom the command
    output = subprocess.getoutput("git-annex find")
    # parsing the output and separating the lines in a list where each element is a file
    s = shlex.split(output, comments=True, posix=False)
    # init the dico
    dico_files = {}

    # getting the name of the project: to get the name of project we can either ask the user about it // or use the name of the remote
    # getting the name of the remote from the remote.log file
    remote_name = get_remotename(deposit_id)
    
    # getting the list of the unused files
    # fetching the keys of the files that are not unused
    for file in s:
        info_file = {}
        info_file["filename"] = file
        # getting the key
        filekey = subprocess.getoutput("git-annex lookupkey %s" % file)
        info_file["key"] = filekey
        # getting the path it's pointing to
        path = subprocess.getoutput("git-annex contentlocation %s" % filekey)
        contentlocation = path
        info_file["contentlocation"]= contentlocation
        dico_files[filekey] = info_file

    # getting the download link of the file
    nurl = url + '/%s/files' % deposit_id
    
    # since this will be reused, we need to remember it
    r = requests.get(nurl, params=params)
    # for each of the files
    for i in range(len(r.json())):
    # fetching the necessary information
        file_id = r.json()[i]['filename']
        download_link = r.json()[i]['links']['download']
        if file_id in dico_files:
            dico_files[file_id]['downloadlink'] = download_link

    # creating a temporary directory to store the files in
    dir = tempfile.TemporaryDirectory()
            
    # write the file in the temporary directory     
    f = open(dir.name + "/git-annex-info.json", "w+")
    json.dump(dico_files, f)
    f.close()


    ########### creating the archive ###############################
    # creating the archive
    archivepath =  dir.name + "/" + remote_name + ".tar.gz"
    os.system("git archive --output="+ archivepath + " --format=tar.gz HEAD --prefix=%s/" % remote_name)         

    ########### creating a new deposit on Zenodo ###################
    r = requests.post(url, params=params, json={}, headers=headers)

    # setting the id & the bucket url
    archivedeposit_id = r.json()['id']
    archivedeposit_bucket = r.json()['links']['bucket']

    # setting the id of the new deposit in the restoring script
    # we also need to set the name of the archive
    with open(path_restorearchive, 'r+') as f:
        f.seek(0, 0)
        f.write("archivedeposit_id=%s" % archivedeposit_id)
        f.write("\n \n")
        f.write("remote_name='%s'" % remote_name)
        f.write("\n\n")
        f.close()
    
    # uploading the two files into the deposit
    with open(path_restorearchive, "rb") as fp:
        r = requests.put("%s/%s" % (archivedeposit_bucket, 'restore_archive.py'), params=params, json={}, data=fp)
                        
    with open(archivepath, "rb") as fp:
        archivename = remote_name + '.tar.gz'
        r = requests.put("%s/%s" % (archivedeposit_bucket, archivename), params=params, json={}, data=fp)

    with open(dir.name + "/git-annex-info.json", "rb") as fp:
        r = requests.put("%s/%s" % (archivedeposit_bucket, 'git-annex-info.json'), params=params, json={}, data=fp)

    # we need to remove the directory when we finish working with it
    dir.cleanup()


# function to call whenever we can to choose an upload type:
def setting_uploadtype():
    # the possible types of the uploads
    uploadtypes = ['publication', 'poster', 'presentation', 'dataset', 'image',
                    'video', 'software', 'lesson', 'physicalobject', 'other']

    # in the case: upload_type == 'publication'
    publicationtypes = ['annotationcollection', 'book', 'section', 'conferencepaper', 'datamanagementplan',
                        'article', 'patent', 'prepint', 'deliverable', 'milestone', 'proposal', 'report',
                        'softwaredocumentation', 'taxonomictreatment', 'technicalnote', 'thesis', 'workingpaper', 'other']
    # in the case: upload_type == 'image'
    imagetypes = ['figure', 'plot', 'drawing', 'diagram', 'photo', 'other']

    # asking for the initial type of the upload:
    print("What is the type of the upload? Please choose one of these options (ex: 5) \n")
    print("0 - publication \n")
    print("1 - poster \n")
    print("2 - presentation \n")
    print("3 - dataset \n")
    print("4 - image \n")
    print("5 - video \n")
    print("6 - software \n")
    print("7 - lesson \n")
    print("8 - physical object \n")
    print("9 - other \n")
    n = int(input('Enter the correspoding number: '))
    upload_type = uploadtypes[n]


    # taking care of the information concerning the publication type:
    if upload_type == 'publication':
        print('Here are the possible types of publication. Please choose one of them (ex: 5) \n')
        print("0 - annotation collection \n")
        print("1 - book \n")
        print("2 - section \n")
        print("3 - data management plan \n")
        print("4 - article \n")
        print("5 - patent \n")
        print("6 - preprint \n")
        print("7 - deliverable \n")
        print("8 - milestone \n")
        print("9 - proposal \n")
        print("10 - software documentation \n")
        print("11 - taxonomic treatment \n")
        print("12 - technical note \n")
        print("13 - thesis \n")
        print("14 - working paper \n")
        print("15 - other \n")
        n = int(input('Enter the correspoding number: '))
        upload_type = publicationtypes[n]

    elif upload_type == 'image':
        print('Here are the possible types of images. Please choose one of them (ex: 5) \n')
        print("0 - figure \n")
        print("1 - plot \n")
        print("2 - drawing \n")
        print("3 - diagram \n")
        print("4 - photo \n")
        print("5 - other \n")
        n = int(input('Enter the correspoding number: '))
        upload_type = imagetypes[n]

    return upload_type

# function to call to set the creators of the upload.
# This function is called whenever the user wants to publish an upload.
def setting_creators():
    creators = []
    c = {}
    nbcreators = int(input("Enter the number of the creators of this upload. \n"))
    for i in range(nbcreators):
        print("For the " + str(i) + " creator: \n")
        family_name = input('Enter the Family name (Required): \n')
        given_name = input('Enter the Given name (Required): \n')
        affiliation = input('Enter the affiliation of the creator or press enter to pass (Optional): \n')
        orcid = input('Enter the orcid of the creator or press enter to pass (Optional): \n')
        gnd = input('Enter the gnd of the creator or press enter to pass (Optional): \n')
        c['name'] = "%s, %s" % (family_name, given_name)
        if affiliation != '':
            c['affiliation'] = affiliation
        if orcid != '':
            c['orcid'] = orcid
        if gnd != '':
            c['gnd'] = gnd
        creators.append(c)

    return creators

# function to call to set the access right to the publication. The user
# chooses which type of access to give and takes care of any additional
# information that depends on the chosen access.
# This function is called whenever the user wants to publish an upload.
def setting_accessright ():
    # initializing the list of options
    accessrights = ['open', 'embargoed', 'restricted', 'closed']
    licenses = ['Creative Commons Attribution 4.0 International', 'Creative Commons Attribution 1.0 Generic',
                'Creative Commons Attribution 2.0 Generic', 'Creative Commons Attribution 3.0 Unported']

    # choosing the access right
    print("What is the access right of the upload? Please choose one of these options (ex: 2) \n")
    print("0 - open \n")
    print("1 - embargoed \n")
    print("2 - restricted \n")
    print("3 - closed \n")
    n = int(input('Enter the correspoding number: '))
    access_right = accessrights[n]

    # taking care of the extra information concerning all the possible access rights
    if access_right == 'embargoed':
        # need to specify embargo_date
        print('Specify the Embargo date. The format is: YYYY-MM-DD. \n')
        embargo_date = input()
        EMBARGO_DATE = embargo_date

    if access_right == 'embargoed' or access_right == 'open':
        # need to specify the license
        print('Specify the license. Choose one of these options: \n')
        print("0 - Creative Commons Attribution 4.0 International \n")
        print("1 - Creative Commons Attribution 1.0 Generic \n")
        print("2 - Creative Commons Attribution 2.0 Generic \n")
        print("3 - Creative Commons Attribution 3.0 Unported \n")
        n = int(input('Enter the correspoding number: '))
        license = licenses[n]
        LICENCE = license

    if access_right == 'restricted':
        # need to specify access_conditions
        print('Specify the conditions under which you grant users access to the files in your upload. \n')
        access_conditions = input()
        ACCESS_CONDITIONS = access_conditions

    return access_right

# method to look up the metadata on the remote before publishing.
# returns true if all the needed metadata is given or false if it's not
# returns the dictionary containing the metadata as well to show the user
# so that they decide whether to change or not.
def lookup_metadata(url, key):
    import requests
    r = requests.get(url, params = {'access_token': key})
    metadata = r.json()['metadata']
    # In Zenodo, we can't change only one of these and save the file since we have to
    # give all of them (they are required) to be able to save it
    # so, by knowing that one of them is absent, we can know that they all are.
    if ('title' not in metadata.keys() ) or ('upload_type' not in metadata.keys()) or ('description' not in metadata.keys()) or ('creators' not in metadata.keys()) or ('access_right' not in metadata.keys()):
        return False, {}
    return True, metadata


# this is the function that will be used to publish the deposit
def publish(deposit_id, key, url, pub_file = None):
    import json
    import requests

    # setting the url of the deposit
    nurl = url + '/%s' % deposit_id

    # initializing the required metadata if the file is not given
    if not pub_file:
        # look to see if the user has already set the metadata in the remote manually.
        # if it's the case, either ask the user if the info is ok and publish directly
        # or make them fill in the information manually on the command line.
        bool, dict = lookup_metadata(nurl, key)
        # showing the user the metadata they have submitted so as to see if they want
        # to keep them or update them
        if bool:
            print("Here is the metadata of the deposit. Do you want to change it (y/n)? \n")
            print(json.dumps(dict, indent=4))
            response = input()

        # if they don't want to change it, we can use the metadata as the data given when publishing
        if response == False:
            data = dict
        # or else, they want to update the existing metadata or want to submit it from the start
        elif response == True or bool == False:
            # setting the type of the upload using the choosetype function
            upload_type = setting_uploadtype()
            # setting the title of the upload
            title = input('Enter the title of the upload: ')
            # setting the description of the upload
            description = input('Enter a basic description of the upload')
            # setting the access right of the upload
            access_right = setting_accessright()
            # getting information about the creators of the publication
            creators = setting_creators()
            # setting up the data
            data = {
                'metadata': {
                    'title': title,
                    'upload_type': upload_type,
                    'description': description,
                    'creators': creators,
                    'access_right': access_right
                }
            }
            data = json.dumps(data)

    # if the file is already written by the user, we can simply use it
    else:
        with open(pub_file, "rb") as fp:
            #data = fp
            data = json.load(fp)

    # finishing the publication
    headers = {"Content-Type": "application/json"}
    params = {'access_token': key}

    # updating the deposit with the needed metadata
    requests.put(nurl, params=params, data=json.dumps(data), headers=headers)

    # publishing
    nurl = nurl + "/actions/publish"
    requests.post(nurl,params=params, json={}, headers=headers)


# method that transforms the files into web remotes
def transformtoweb(deposit_id, key, url):
    # we can simply use the git annex addurl --file and do this for each file as has been previously tested
    # the option --file will attach the url to the existing file instead of creating a new one.
    # this way, a trace has been kept of where this file exists (the remotes in this case being Zenodo and the web remote)
    # to do this, we can use a shell command with a library to facilitate the interaction between the two interfaces.

    import subprocess, shlex, os, requests

    # getting the output from trom the command
    output = subprocess.getoutput("git-annex find")
    # parsing the output and separating the lines in a list where each element is a file
    s = shlex.split(output, comments=True, posix=False)
    # init the dico
    dico = {}
    # fetching the keys of these files
    for file in s:
        output = subprocess.getoutput("git-annex info %s" % file)
        l = shlex.split(output)
        # we won't take care of the ones with the fatal error now
        if l[0] == 'file:':
            k = l[6]
            dico[str(k)] = file

    nurl = url + '/%s/files' % deposit_id

    r = requests.get(nurl, params={'access_token': key})

    # third step
    # for each of the files
    for i in range(len(r.json())):
        # fetching the necessary information
        file_id = r.json()[i]['filename']
        download_link = r.json()[i]['links']['download']
        file_name = dico[file_id]
        # now, we can finally create the web url
        nurl = download_link + '?access_token='+ key
        # now, let's turn the files into web remotes
        u = os.system('git annex addurl '+ nurl + ' --file=' + file_name + " --relaxed")


# method to disable the remote locally with git rm
def disableremotelocally(deposit_id):
    # use a shell command to remove the remote locally with git rm
    # this could be done with the library that has been previously tested
    # this is the last step to be done after having already published the deposit on Zenodo.

    import os

    # getting the name of the remote
    remote_name= get_remotename(deposit_id)

    # removing the remote locally
    if remote_name == '':
        print("Error while looking for the name of the remote")
    else:
        os.system("git remote remove " + remote_name)


# this function takes care of looking for the ids of the remotes.
# For instance, if there is only one zenodo remote that has been initialized in
# this repository, the program uses that id to disable the remote. If not, we can
# list the ids to the user for them to choose from.
def lookup_depositid():
    import subprocess, shlex

    # reading the file from the other branch without checking into it
    output = subprocess.getoutput("git show git-annex:./remote.log")

    # we can have multiple remotes in one log and they are separated by lines.
    lines = output.splitlines()
    # creating a list where we will be putting the deposit id we found
    l = []
    # going through the remotes
    for line in lines:
        # parsing the output and separating the lines in a list where each element is a file
        s = shlex.split(line, comments=True, posix=False)
        # now, let's go through the list
        for elm in s:
            # looking through the elemnts for the index of the id
            if elm.startswith("deposit_id"):
                id = elm.split("=")[-1]
                # adding the id of the deposit to the list
                l.append(id)
    # printing the ids of the deposits in this directory
    print("The ids of the Zenodo deposits that have been created in this directory are: \n")
    for i in l:
        print(i)
    return l

# prints information about the program and the options that could be used.
def print_info():
    print("------------ Disabling the Zenodo remote ------------")
    print("This program is used to publish a Zenodo deposit and disble the remote locally while keeping a copy of the published files in a web remote. It also keeps an archive so that the user could recover the whole project when they want later on.")
    print("Here are the possible options:")
    print("'-h' : for help.")
    print("'-i' <deposit_id> : this is the id of the deposit. The user can use the option -l to print out the ids that have been stored in this directory.")
    print("'-k' <key> : the access token that was used when creating the deposit. ")
    print("'-f' <path to zenodo.json file> : This is optional, the user could give the path to this file if they want, or they can fill in the information later on in the stdin.")
    print("'-u' <sandbox if used> : If the deposit is on the sandbox, specify that by using this option. If not used, it means the deposit is not on the sandbox.")
    print("'-p' <path to restore_archive.py> : if it's not given, it looks for the file is available in the current directory. ")
    print("'-l' : to list the ids of the deposits in this directory.")
    print("------------------------------------------------------")

# this is the main function
def main(argv):
    url = None
    file_path = None
    deposit_id =''
    try:
        opts, args = getopt.getopt(argv,"hi:k:f:u:p:l",["id=", "key=", "file=", "url=", "path="])
    except getopt.GetoptError:
        print('Problem with the syntax of the command.')
        print_info()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print_info()
            sys.exit()
        elif opt in ("-i", "--id"):
            deposit_id = arg
        elif opt in ("-k", "--key"):
            key = arg
        elif opt in ("-f", "--file"):
            file_path = arg
        elif opt in ("-u", "--url"):
            url= arg
        elif opt in ("-p", "--path"):
            path_restorearchive= arg
        if opt == '-l':
            lookup_depositid()
            sys.exit()

    # setting up the url
    if not url:
        url = 'https://zenodo.org/api/deposit/depositions'
    else:
        url = 'https://sandbox.zenodo.org/api/deposit/depositions'


    # creating an archive and uploading it to a new deposit
    archiving(deposit_id, key, url, path_restorearchive)
    # publishing the deposit
    publish(deposit_id, key, url, file_path)
    # transforming each of the files into web remotes
    transformtoweb(deposit_id, key, url)
    # disabling the remote locally
    disableremotelocally(deposit_id)

if __name__ == "__main__":
    main(sys.argv[1:])