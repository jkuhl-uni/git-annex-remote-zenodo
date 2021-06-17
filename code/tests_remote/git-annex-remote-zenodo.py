#!/usr/bin/env python

import sys

from annexremote import Master
from annexremote import ExportRemote
from annexremote import RemoteError, ProtocolError

class ZenodoRemote(ExportRemote):

    def query(self, query_method, url, headers=None, data=None, stream = None):
        # id = key (!= KEY or access token to the API): to be stored in the remote. 
        # In most cases, this is going to be the remote file name. It should be at 
        # least be unambigiously derived from it.
        import requests
        # making sure that the headers are specified before sending the request
        if headers is None:
            headers = {"Content-Type": "application/json"}

        # we use the same access key for all the queries. 
        params = {'access_token': self.key}

        # depending on the query, some of the arguments might be null
        if query_method == 'get':
            # this is for when we want to retrieve and download the file
            if stream == True:
                request = requests.get(url, params = params, stream = True)
            else:
                request = requests.get(url, params = params)
        elif query_method == 'post':
            request = requests.post(url, params=params, json={}, headers=headers)
        elif query_method == 'put':
            request = requests.put(url, params=params, json={}, data=data)
        else:
            request = requests.delete(url, params)
            
        # informing the user of the currint state of the operation        
        print("finished the " + query_method + " operation. Here is the returned message \n")
        #returning the resulting request for later uses
        print(request.status_code)
        return request


    def create_newversion(self, oldrecord_id):
        import requests

        # making sure that the given id for the old record is correct
        url = self.url + '/' + str(oldrecord_id) 
        r = self.query('get', url)

        # raise error if there is a problem (the success code is 200)
        if r.status_code != 200:
            raise RemoteError('error while retrieving the old deposit')
        
        # making the post request to create the new version
        url = self.url + '/' +  str(oldrecord_id) + '/actions/newversion'
        r = self.query('post', url)
        
        # raise error if there is a problem (the success code is 201)
        if r.status_code != 201:
            raise RemoteError('error while creating the newversion')

        # fetching the deposition id of the new version
        # we can only access it this way because it's not given as a field
        newdeposit_id = r.json()['links']['latest_draft'].split('/')[-1]

        # making a new get request to get the information about this reposit and returning the response
        url = self.url + '/' + str(newdeposit_id) 
        r = self.query('get', url)
        return r

    def initremote(self):
        # getting the url of the remote (Zenodo or Sandbox)
        # the user would need the key for both of them and it's created on the website of the one they chose
        url = self.annex.getconfig('url')
        if url is None:
            self.url = 'https://zenodo.org/api/deposit/depositions'
        else:
            self.url = 'https://sandbox.zenodo.org/api/deposit/depositions'
        
        #self.url = 'https://sandbox.zenodo.org/api/deposit/depositions'

        # the key is passed as an argument when using the commant initremote (ex: key='')
        # if it's not been added as an argument, we raise an 
        if not self.annex.getconfig('key'):
            raise RemoteError("You need to add the access token (key=TOKEN)")
        else:
            # need to get the key by using the getconfig method
            self.key = self.annex.getconfig('key')

        
        # now, we need to create an empty upload that we will be using from now on
        # it's either a new version of a deposit or a brand new one
        newversion= self.annex.getconfig('newversion')
        if not newversion:
            r = self.query('post', self.url)
        else:   
            r = self.create_newversion(self.annex.getconfig('newversion'))
        
        #r = self.query('post', self.url)

        # making sure that we got the correct success response for creating a new deposit
        if r.status_code != 201:
            print("error while preparing the remote: cannot communicate with the remote " + str(r.status_code))
            raise RemoteError('could not send a post query to the API')

        self.annex.setconfig('deposit_id', r.json()['id'])
        
        # other settings
        self.annex.setconfig('deposit', r)
        self.annex.setconfig('url', self.url)
        self.annex.setconfig('key', self.key)
        # setting the id for this deposit
        self.annex.setconfig('deposit_id', r.json()['id'])
        self.annex.setconfig('deposit_bucket', r.json()['links']['bucket'])
        
                
    def prepare(self):
        import json
        self.key = self.annex.getconfig('key')
        self.url = 'https://sandbox.zenodo.org/api/deposit/depositions'

        r = self.query('get', self.url)
        if r.status_code != 200:
            print("error while preparing the remote: cannot communicate with the remote" + str(r.status_code))
            raise RemoteError('could not send a get query to the API')


        self.deposit_id = self.annex.getconfig('deposit_id')
        

   
    def transfer_store(self, key, filename):
        try:
            # fetching the url of the bucket
            URL_BUCKET = self.deposit_bucket

            # and then we upload it
            # extracting the filename and the path from filename
            # the argument filename of the function contains the full path to the path.
            # we  can get the name of the file by using the function rsplit to split 
            # the string at the specified separator '/' and we can get the filename by 
            # getting the lest element of the file.
            list = filename.rsplit("/")
            file = list[-1]
            path = filename

            # The target URL is a combination of the bucket link with the desired filename
            # seperated by a slash.
            with open(path, "rb") as fp:
                r = self.query('put', "%s/%s" % (self.url, filename), key, data=fp)
            
            if r.status_code < 400:
                print("finished exporting the file... \n")
            else:
                raise RemoteError ('error while exporting the file... \n')

        except Exception as error:
            raise RemoteError(error)        


    def transfer_retrieve(self, key, filename):
        import json
        
        # getting the information on the files that are in the deposit
        url = self.url + str(self.deposit_id) + '/files'
        r = self.query('get', url)

        # going through the list of the files in this deposit
        for i in range(len(r.json())):
            # checking if the file exists by comparing the key/filename
            # sending a get request to check information on the file
            if r.json()[i]['filename'] == key:
                # getting the id of the file that we want to download
                file_id =  r.json()[i]['id']
                # getting the download link of the file
                url = r.json()[i]['links']['download']
                r = self('get', url, stream = True)        
                r.raise_for_status()
                # storing the file in the path given in filename
                # this is done by reading the content of the file and writing it in the new file
                # if the files are very large, we can make the chunk size bigger 
                with open(filename, "wb") as f:
                    for chunk in r.iter_content(chunk_size=120): 
                        f.write(chunk)
                # once we finish writing into the file we can close it
                f.close()

        if r.status_code > 204:
            print("error while fetching the file from the remote" + str(r.status_code))
            raise RemoteError('could not send a get query to the API')
     

    def checkpresent(self, key):
        try:
            url = self.url + str(self.deposit_id) + '/files'
            r = self.query('get', url)
            # going through the list of the files in this deposit
            for i in range(len(r.json())):
                if r.json()[i]['filename'] == key:
                    print('Yes, this file exists in the remote: ' + key )
                    return True
            return False             
        except Exception as error:
            raise RemoteError(error)


    def remove(self, key):
        # checking if the key exists in the remote deposit
        url = self.url + str(self.deposit_id) + '/files'
        r = self.query('get', url)
        # going through the list of the files in this deposit
        file_id = None
        for i in range(len(r.json())):
            if r.json()[i]['filename'] == key:
                file_id = r.json()[i]['id']

        # if the key is non existing, we shouldn't raise an exception        
        if file_id is None:
            return
        
        # Delete an existing deposition file resource. Note, only deposition 
        # files for unpublished depositions may be deleted.

        # first, we update the url so as to use it to delete the file
        url = url + '/' + str(file_id)
        # we then make the query to delete the file
        r = self.query('delete', url)

        # raising RemoteError if there is a problem with the removal of the file
        if r.status_code > 204:
            print("error while deleting the file from the remote" + str(r.status_code))
            raise RemoteError('could not send a delete query to the API')


    ## Export methods
    def transferexport_store(self, key, local_file, remote_file):
        return self.transfer_store(key, local_file)


    def transferexport_retrieve(self, key, local_file, remote_file):
        return self.transfer_retrieve(key, local_file)


    def checkpresentexport(self, key, remote_file):
        return self.checkpresent(key)


    def removeexport(self, key, remote_file):
        return self.remove(key)


    def removeexportdirectory(self, remote_directory):
        url = self.url + str(self.deposit_id) + '/files'
        r = self.query('get', url)
        # going through the list of the files in this deposit
        file_id = None
        # manipulating each of the files in this deposit
        for i in range(len(r.json())):
            file_id = r.json()[i]['id']
            if file_id is not None:     
                # Delete an existing deposition file resource. Note, only deposition 
                # files for unpublished depositions may be deleted.
                # first, we update the url so as to use it to delete the file
                url = url + '/' + str(file_id)
                # we then make the query to delete the file
                r = self.query('delete', url)
                # for each of the files
                # raising RemoteError if there is a problem with the removal of the file
                if r.status_code > 204: 
                    print("error while deleting the " + str(i) + " file from the remote" + str(r.status_code))
                    raise RemoteError('could not send a delete query to the API')

    # not needed
    def renameexport(self, key, filename, new_filename):
        """
        import json
        # when it's not published we can simply edit the name with the edit function
        url = self.url + '%s/files' % self.deposit_id
        r = self.query('get, url')

        for i in range(len(r.json())):
            if r.json()[i]['filename'] == filename:
                id = r.json()[i]['id']

        data = {"name": new_filename}
        url = url + '/' + str(id)    
        r = self.query('put', url, data=json.dumps(data))   

        if r.status_code != 200:
            raise RemoteError('Failed to rename the file')
        """
        pass
        
    def _info(self, message):
        try:
            self.annex.info(message)
        except ProtocolError:
            print(message)
            
def main():

    # Redirect output to stderr to avoid messing up the protocol
    output = sys.stdout
    sys.stdout = sys.stderr
    
    master = Master(output)
    remote = ZenodoRemote(master)
    master.LinkRemote(remote)
    master.Listen()

if __name__ == "__main__":
    main()        

