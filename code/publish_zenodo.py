    # added methods

    # function to call whenever we can to choose an upload type:
def setting_uploadtype(self):
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
def setting_creators(self):
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
def setting_accessright (self):
        
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

        if access_right == 'embargoed' or access_right == 'open':
            # need to specify the license
            print('Specify the license. Choose one of these options: \n')
            print("0 - Creative Commons Attribution 4.0 International \n")
            print("1 - Creative Commons Attribution 1.0 Generic \n")
            print("2 - Creative Commons Attribution 2.0 Generic \n")
            print("3 - Creative Commons Attribution 3.0 Unported \n")               
            n = int(input('Enter the correspoding number: ')) 
            license = licenses[n]

        if access_right == 'restricted':
            # need to specify access_conditions
            print('Specify the conditions under which you grant users access to the files in your upload. \n')
            access_conditions = input()

    # this is the function that will be used to publish the deposit
def publish(self):
        import json
        # initializing the required metadata
        
        # setting the type of the upload using the choosetype function
        upload_type = self.setting_uploadtype() 
        
        # setting the title of the upload
        title = input('Enter the title of the upload: ')
        
        # setting the description of the upload
        description = input('Enter a basic description of the upload')
        
        # setting the access right of the upload
        access_right = self.setting_accessright()
        
        # getting information about the creators of the publication
        creators = self.setting_creators()
  

    # adding metadata to the deposit
        data = {
            'metadata': {
                'title': title,
                'upload_type': upload_type,
                'description': description,
                'creators': creators,
                'access_right': access_right
            }
        }

        # updating the deposit with the needed metadata
        url = 'https://sandbox.zenodo.org/api/deposit/depositions/%s' % self.deposit_id
        r = self.query('put', url, data=json.dumps(data))

        # publishing
        url = 'https://sandbox.zenodo.org/api/deposit/depositions/%s/actions/publish' % self.deposit_id
        r = self.query('post', url)


