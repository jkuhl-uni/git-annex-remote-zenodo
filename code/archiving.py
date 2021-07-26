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



def archiving():
    import tempfile, json, os, requests, subprocess, shlex 

    deposit_id = '882202'
    headers = {"Content-Type": "application/json"}
    key = 'K1jsyYfSbH3hVfRWpzXkzTL5RDVy1ppQWet2v3DQu8WFDuWbfn4J9rITsQaG'
    params = {'access_token': key}


    # first, going to the test directory
    u = os.path.expanduser("~/test_remote")
    os.chdir(u)

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
    sandbox_url = 'yes'
    if not sandbox_url:
        url = 'https://zenodo.org/api/deposit/depositions/%s/files' % deposit_id
    else:
        url = 'https://sandbox.zenodo.org/api/deposit/depositions/%s/files' % deposit_id
    # since this will be reused, we need to remember it
    r = requests.get(url, params={'access_token': key})
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
    os.system("git archive --output=" + dir.name + "/%s.tar.gz" % remote_name + " --format=tar.gz HEAD --prefix=%s/" % remote_name)


    ########### creating a new deposit on Zenodo ###################
    url= 'https://sandbox.zenodo.org/api/deposit/depositions'

    r = requests.post(url, params=params, json={}, headers=headers)

    # setting the id & the bucket url
    archivedeposit_id = r.json()['id']
    archivedeposit_bucket = r.json()['links']['bucket']

    # setting the id of the new deposit in the restoring script
    # we also need to set the name of the archive
    with open("/home/nubudi/Desktop/Internship/code/restore_archive.py", 'r+') as f:
        f.seek(0, 0)
        f.write("archivedeposit_id=%s" % archivedeposit_id)
        f.write("\n")
        f.write("remote_name='%s'" % remote_name)
        f.write("\n\n")
        f.close()
    
    # uploading the two files into the deposit
    with open("/home/nubudi/Desktop/Internship/code/restore_archive.py", "rb") as fp:
        r = requests.put("%s/%s" % (archivedeposit_bucket, 'restore_archive.py'), params=params, json={}, data=fp)
                        
    with open(dir.name + '/%s.tar.gz' % remote_name, "rb") as fp:
        r = requests.put("%s/%s" % (archivedeposit_bucket, '%s.tar.gz' % remote_name), params=params, json={}, data=fp)

    with open(dir.name + "/git-annex-info.json", "rb") as fp:
        r = requests.put("%s/%s" % (archivedeposit_bucket, 'git-annex-info.json'), params=params, json={}, data=fp)

    # we need to remove the directory when we finish working with it
    dir.cleanup()

    ##########################
    # first, going to the test directory
    u = os.path.expanduser("/home/nubudi/Desktop/test-remote-newver-archive")
    os.chdir(u)

    # retrieving the archive from Zenodo.
    url= 'https://sandbox.zenodo.org/api/deposit/depositions/%s/files' % archivedeposit_id
    r = requests.get(url, params=params)

    # getting the file restore_archive.py from the response
    for i in range(len(r.json())):
        if r.json()[i]['filename'] == 'restore_archive.py':
            url = r.json()[i]['links']['download']
            filename=r.json()[i]['filename']
            q = requests.get(url, params=params, stream=True)
            print(q.status_code)
            # downloading the files
            with open(filename, "wb") as f:
                for chunk in q.iter_content(chunk_size=120):
                    f.write(chunk)
            f.close()





archiving()

