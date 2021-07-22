

def download_archive(deposit_id, key, sandbox_url=None):
    import requests, os, shlex, subprocess
    if not sandbox_url:
        url = 'https://zenodo.org/api/deposit/depositions/%s/files' % deposit_id
    else:
        url = 'https://sandbox.zenodo.org/api/deposit/depositions/%s/files' % deposit_id

    params = {'access_token': key}

    r = requests.get(url, params=params)

    for i in range(len(r.json())):
        url = r.json()[i]['links']['download']
        filename=r.json()[i]['filename']
        q = requests.get(url, params=params, stream=True)
        print(q.status_code)
        # downloading the files
        with open(filename, "wb") as f:
            for chunk in q.iter_content(chunk_size=120):
                f.write(chunk)
        f.close()

    return

def restore(deposit_id, key, sandbox_url=None):
    import requests, os, shlex, subprocess
    # setting the url 
    if not sandbox_url:
        url = 'https://zenodo.org/api/deposit/depositions/%s/files' % deposit_id
    else:
        url = 'https://sandbox.zenodo.org/api/deposit/depositions/%s/files' % deposit_id

    params = {'access_token': key}

    # init the dico 
    dico = {}

	# untaring the archive
    os.system("tar -xf archive.tar")

	# getting the keys of the files (the links are broken so we need to know the keys of the files they used to point to)

	# getting the output from trom the command 
    output = subprocess.getoutput("ls -ltra | grep '\->'")
	# parsing the output and separating the lines in a list where each element is a file
    s = shlex.split(output, comments=True, posix=False)
	

	# fetching the keys of these files 
    for i in range(len(s)):
	    if s[i] == '->':
		    file_name = s[i-1]
		    key_file = s[i+1].split('/')[-1]
		    dico[key_file] = file_name

	# sending a request to the API to get the file 
    r = requests.get(url, params=params)
    
    for i in range(len(r.json())):
	    url = r.json()[i]['links']['download']
	    file_key = r.json()[i]['filename']
	    file_name = dico[file_key]
	    os.system("curl " + url + " --output " + file_name)




def main(argv):
    import sys, getopt

    url = None
    deposit_id =''
    try:
        opts, args = getopt.getopt(argv,"hi:k:u:",["id=", "key=", "url="])
    except getopt.GetoptError:
        print('Problem with the syntax of the command. Please enter the id of the deposit to restore. If the deposit is on the sandbox, enter url=sandbox or -u sandbox \n')
        print ('restore_archive.py -i <deposit_id> -k <access_key> -u <sandbox if used>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('restore_archive.py -i <deposit_id> -k <access_key> -u <sandbox if used>')
            sys.exit()
        elif opt in ("-i", "--id"):
            deposit_id = arg
        elif opt in ("-k", "--key"):
            key = arg
        elif opt in ("-u", "--url"):
            url= arg

    # downloading the archive and the file from the new 
    download_archive(deposit_id, key, url)
    restore(deposit_id, key, url)

if __name__ == "__main__":
    import sys
    main(sys.argv[1:])
	    

