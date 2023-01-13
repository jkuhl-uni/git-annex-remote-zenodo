#!/usr/bin/env python

archivedeposit_id=890176
 
remote_name='Myproject'



## function to download the archive from zenodo as well as download the json file containing the info
def download_archive(key, url):
    import requests
    # setting the url to get the list of the files
    url = url + '/' + str(archivedeposit_id) + '/files'
    params = {'access_token': key}

    # sending the request to the API to get the list of files stored in the deposit
    r = requests.get(url, params=params)
    
    # downloading the archive and the info file
    # since the archivename has been set when we wrote the file while archiving
    # we don't need to study the case where the archive hasnt been found because of
    # an error with the name. If we decide to ask the user to pass the name of the archive 
    # as an argument, we need to study that case.
    for i in range(len(r.json())):
        if r.json()[i]['filename'] == "%s.tar.gz" % remote_name or r.json()[i]['filename'] == 'git-annex-info.json':
            url_download = r.json()[i]['links']['download']
            filename=r.json()[i]['filename']
            q = requests.get(url_download, params=params, stream=True)
            # downloading the files
            with open(filename, "wb") as f:
                for chunk in q.iter_content(chunk_size=120):
                    f.write(chunk)
            f.close()
    return  

def restore_files(key, url, restoring_option):
    import os, shlex, json, subprocess

    # extracting the files from the archive.
    # u = os.path.expanduser(dir.name)
    # os.chdir(u)
    os.system("tar -xzf %s.tar.gz" % remote_name)

    # going to the folder where the files are
    u = os.path.expanduser(remote_name)
    os.chdir(u)

    # getting the names of the files in the archive
    u = subprocess.getoutput('ls -1')
    # parsing the output and separating the lines in a list where each element is a file
    s = shlex.split(u, comments=True, posix=False)

    # loading the info in the json file into a dictionary
    f = open('%s/../git-annex-info.json' % os.getcwd())
    dico = json.load(f)

    # let's delete the files from the dico that cannot be downloaded from the remote.
    # when we recover the files, we can only recover the once that are in the remote and 
    # so we delete the ones that we could have had locally when we created the archive with git
    keep = []
    delete = []
    for k, v in dico.items():
        if 'downloadlink' not in v.keys():
            # let's register the keys of the files that we want to delete
            delete.append(k)
        else:
            # let's register the names of the files that are on the remote in a list for later use
            keep.append(v['filename'])
    
    # deleting the keys from the dico
    for e in delete:
        dico.pop(e)

    # now, let's delete these files locally. When we untar the archive, there are some files that
    # aren't on the remote and so we can delete them since they have been locally in the repo when
    # the archive was created. Let's go through the list of files (s) and delete the ones not in dico.
    for element in s:
        if element not in keep:
            os.system("rm "+ element)

    # restoring the files using one of the chosen options.
    if restoring_option == 'simpledownload':
        for k, v in dico.items():
            if v['filename'] in s:
                url = v['downloadlink'] + '?access_token=' + key
                file_name = v['filename']
                # removing the file before downloading it
                os.system("rm " + file_name)
                # downloading the file using the download link
                os.system("curl " + url + " --output " + "./" + file_name)
    elif restoring_option == 'rebuildannex':
        for k, v in dico.items():
            if v['filename'] in s:
                url = v['downloadlink'] + '?access_token=' + key
                file_path = v['contentlocation']
                file_path = "./" + file_path
                # let's create the folders where we want to download the files
                try:
                    os.makedirs(os.path.dirname(file_path))
                except OSError:
                    print ("Failed to create the directory " % file_path)
                os.system("curl " + url + " --output " + file_path)
    elif restoring_option == 'usegitannex':
        os.system("git init")
        os.system("git annex init")
        for k, v in dico.items():
            if v['filename'] in s:
                url = v['downloadlink'] + '?access_token=' + key
                file_name = v['filename']
                # removing the file before downloading it
                os.system("rm " + file_name)
                # downloading the file using the download link
                os.system("curl " + url + " --output " + "./" + file_name)
                # adding the file into the annex
                os.system("git annex add " + file_name)
                # adding the file as a web remote
                os.system("git annex registerurl " + k + " " + url)
            else:    
                print("this is just a test to see if some elements havent been deleted from dico")
    else:
        print("The option that was given is not correct, please enter a correct option (simpledownload - rebuildannex - usegitannex).")

    # once we finish restoring the files, we can remote the archive and the other files if we no longer need them
    u = os.path.expanduser(os.getcwd() + "/..")
    os.chdir(u)
    os.system("rm git-annex-info.json")
    os.system("rm %s.tar.gz" % remote_name)
    os.system("rm restore_archive.py")

def main(argv):
    import sys, getopt

    url = None
    try:
        opts, args = getopt.getopt(argv,"hk:u:o:",["key=", "url=", "option="])
    except getopt.GetoptError:
        print('Problem with the syntax of the command.  If the deposit is on the sandbox, enter url=sandbox or -u sandbox \n')
        print('You need to choose the chosen option: rebuildannex / usegitannex / simpledownload. Enter -h for more help.')
        print ('restore_archive.py -k <access_key> -u <sandbox if used> -o <chosen option>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('restore_archive.py -k <access_key> -u <sandbox if used> -o <chosen option>')
            print('The option for restoring files: \n')
            print("- 'rebuildannex': Rebuild the annex so that the downloaded symbolic links point to the files. \n")
            print("- 'usegitannex': initialize a git-annex and add the restored files into it as well as store them as web remotes. \n")
            print("- 'simpledownload': download the files once we restore them by making them replace the broken symbolic links. ")
            sys.exit()
        elif opt in ("-k", "--key"):
            key = arg
        elif opt in ("-u", "--url"):
            url= arg
        elif opt in ("-o", "--option"):
            option = arg

    if not url:
        zenodo_url = 'https://zenodo.org/api/deposit/depositions'
    else:
        zenodo_url = 'https://sandbox.zenodo.org/api/deposit/depositions'

    # downloading the archive and the file from the new 
    download_archive(key, zenodo_url)
    # restoring the files
    restore_files(key, zenodo_url, option)

if __name__ == "__main__":
    import sys
    main(sys.argv[1:])
        
