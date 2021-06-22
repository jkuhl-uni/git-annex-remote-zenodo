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
def lookup_metadata(deposit_id, key):
    import requests
    url = 'https://sandbox.zenodo.org/api/deposit/depositions/%s' % str(deposit_id)
    r = requests.get(url, params = {'access_token': key})
    metadata = r.json()['metadata']
    # In Zenodo, we can't change only one of these and save the file since we have to 
    # give all of them (they are required) to be able to save it
    # so, by knowing that one of them is absent, we can know that they all are.
    if 'title' or 'upload_type' or 'description' or 'creators' or 'access_right' not in metadata.keys():
        return False, {}
    return True, metadata


# this is the function that will be used to publish the deposit
def publish(deposit_id, key, pub_file = None, sandbox_url=None):
    import json
    import requests
    # initializing the required metadata if the file is not given
    if not pub_file:
        
        # look to see if the user has already set the metadata in the remote manually.
        # if it's the case, either ask the user if the info is ok and publish directly
        # or make them fill in the information manually on the command line.
        bool, dict = lookup_metadata(deposit_id, key) 
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
            data = fp


    # finishing the publication
    headers = {"Content-Type": "application/json"}
    params = {'access_token': key}
    
    # updating the deposit with the needed metadata
    if not sandbox_url:
        url = 'https://zenodo.org/api/deposit/depositions/%s' % deposit_id
    else:
        url = 'https://sandbox.zenodo.org/api/deposit/depositions/%s' % deposit_id
    r = requests.put(url, params=params, json={}, data=data, headers=headers)
    print(r.json())
    # publishing
    if not sandbox_url:
        url = 'https://zenodo.org/api/deposit/depositions/%s/actions/publish' % deposit_id    
    else:
        url = 'https://sandbox.zenodo.org/api/deposit/depositions/%s/actions/publish' % deposit_id
    r = requests.post(url,params=params, json={}, headers=headers)    
    print(r.json())

    
# this is the main function
def main(argv):
    url = None
    file_path = None
    try:
        opts, args = getopt.getopt(argv,"hi:k:o:u:",["id=", "key=", "file=", "url="])
    except getopt.GetoptError:
        print('Problem with the syntax of the command. Please enter the id of the deposit to publish and/or the path to the file containing information about the publishing or leave it to be done manually. If the deposit is on the sandbox, enter url=sandbox or -u sandbox \n')
        print ('test.py -i <deposit_id> -k <access_key> -f <file_path> -u <sandbox if used>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('test.py -i <deposit_id> -k <access_key> -f <file_path> -u <sandbox if used>')
            sys.exit()
        elif opt in ("-i", "--id"):
            deposit_id = arg
        elif opt in ("-k", "--key"):
            key = arg
        elif opt in ("-f", "--file"):
            file_path = arg
        elif opt in ("-u", "--url"):
            url= arg

    publish(deposit_id, key, file_path, url)

if __name__ == "__main__":
    main(sys.argv[1:])
