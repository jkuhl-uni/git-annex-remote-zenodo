#!/usr/bin/env python

import sys, os, errno

from annexremote import Master
from annexremote import ExportRemote
from annexremote import RemoteError, ProtocolError

class NakalaRemote(ExportRemote):

    def upload_tmpfile(self, apikey):
        import tempfile, subprocess

        # creating a temporary directory to store the file in
        dir = tempfile.TemporaryDirectory()

        # setting the path of the file
        path = dir.name + "/tmpfile.txt"

        # creating a simple txt file 
        with open(path, "w+") as f:
            f.write("This is just a temporary file created and uploaded to be used to create a data.")

        # uploading the file into nakala (into the temporary space)
        status, output = subprocess.getstatusoutput("curl -s -X POST 'https://apitest.nakala.fr/datas/uploads' -H 'accept: application/json' -H 'X-API-KEY: "+ apikey +"' -H 'Content-Type: multipart/form-data' -F 'file=@"+ path +";type=file/txt'")
        
        # closing the temporary directory that we used to create the file
        dir.cleanup()

        return output

    # initialize the remote, eg. create the folders
    # raise RemoteError if the remote couldn't be initialized
    def initremote(self):
        import requests, json

        # let's set the url and key first
        url = 'https://api.nakala.fr/datas'
        if not self.annex.getconfig('key'):
            raise RemoteError("You need to give the access key (key=YOUR_KEY)")
        else:
            self.key = self.annex.getconfig('key')
        
        ## NB: maybe we can also ask for the name of the data for the user to give when initializing the remote
        if not self.annex.getconfig('dataname'):
            raise RemoteError("You need to give the name of the data")
        else:
            self.dataname = self.annex.getconfig('dataname')

        # let's create a tmp file and upload it on /datas/uploads
        info_tmpfile = self.upload_tmpfile(self.key)
        file_id = info_tmpfile.split(',')[-1].split(':')[-1]
        
        # setting up the required metadata to crate the new data
        # TODO: take care of the types / title by adding them as arguments
        # when initializing the remote. When the user gives the type they want 
        # (they could either get it directly from nakala or we could print it out 
        # with an option help) we can then send a query to the API /vocabularies/X 
        # to get the actual typeUri to add to the data.
        data = {
            "status": "pending",
            "metas": 
            [{"value": "testing",
              "typeUri": "http://www.w3.org/2001/XMLSchema#string",
              "propertyUri": "http://nakala.fr/terms#title" }, 
            { "value": "http://purl.org/coar/resource_type/c_18cf",
              "typeUri": "http://www.w3.org/2001/XMLSchema#anyURI",
              "propertyUri": "http://nakala.fr/terms#type" }],
            "files": [{"sha1": file_id}]
        }
        # let's send a query to the API to create the new data using the tpm file 
        # that we have previously uploaded via /datas/uploads
    
        #curl -X POST "https://apitest.nakala.fr/datas" -H "accept: application/json" -H "X-API-KEY: 01234567-89ab-cdef-0123-456789abcdef" -H "Content-Type: application/json" -d "{ \"status\": \"pending\", \"metas\": [ { \"value\": \"testing\", \"typeUri\": \"http://www.w3.org/2001/XMLSchema#string\", \"propertyUri\": \"http://nakala.fr/terms#title\" }, { \"value\": \"http://purl.org/coar/resource_type/c_18cf\", \"typeUri\": \"http://www.w3.org/2001/XMLSchema#anyURI\", \"propertyUri\": \"http://nakala.fr/terms#type\" } ], \"files\": [ { \"sha1\": \"2686db4e1a2b40a03c5b891f30278c40d669ddf8\" } ]}"
        
        # setting up the headers
        headers = {"accept": "application/json", "X-API-KEY": self.key, "Content-Type": "application/json"}

        # sending a POST request to the API to create the data using the metadata and the temporary file
        r = requests.post(url, headers=headers, data=json.dumps(data))

        # raising an exception if the data couldn't be created
        if r.status_code > 201:
            self.annex.debug("[error]: failed to send a post query in initremote. Returned code: " + str(r.status_code))
            raise RemoteError('could not send a post query to the API in initremote.')

        # getting the id of the data
        data_id = r.json()['payload']['id']

        # setting up the configs
        self.annex.setconfig('tmpfile_state', 'up')
        self.annex.setconfig('tmpfile_id', file_id)
        self.annex.setconfig('data_id', data_id)

        # finished initializing the remote
        self.show_info("------------ git-annex-remote-nakala------------")
        self.show_info("Finished initializing a Nakala remote successfully.")
        self.show_info("------------------------------------------------")

    # prepare to be used, eg. open TCP connection, authenticate with the server etc.
    # raise RemoteError if not ready to use       
    def prepare(self):
        import requests
        url = "https://apitest.nakala.fr/datas/%s" % self.annex.getconfig('data_id')
        headers = {"accept": "application/json", "X-API-KEY": self.annex.getconfig('key')}
        r = requests.get(url, headers=headers)

        if r.status_code > 200:
            self.annex.debug("[error]: failed to send a get query in prepare. Returned code: " + str(r.status_code))
            raise RemoteError('could not send a get query to the API in prepare.')

        # let's take a look at the list of files to see if the tmp file has been deleted
        tmpfile_state = self.annex.getconfig('tmpfile_state')
        # if the temporary file is still there 
        if tmpfile_state == 'up':
            # let's try to delete it
            r = requests.delete(url, headers=headers)
            if r.status_code == 200:
                # changing the state of the file in the configs
                self.annex.setconfig('tmpfile_state', "deleted")
                self.annex.debug("[info]: temporary file deleted successfully.")
            else:
                # we can't delete a file if it's the only one available in the data
                self.annex.debug("[info]: temporary file couldn't be deleted. Here is the returned message: ")
                self.annex.debug(r.json())


    # store the file in `filename` to a unique location derived from `key`
    # raise RemoteError if the file couldn't be stored
    def transfer_store(self, key, filename):
        # first, we need to upload the file via datas/uploads POST
        # then, we fetch the id of this file
        # then, we transfer it to data via /datas/data_id/files POST
        # we can just give info about the file {sha1: file_id}
        # success code = 200
        import subprocess

        # let's upload the file first to datas/uploads (temporary space where all the files are uploaded)
        status, output = subprocess.getstatusoutput("curl -s -X POST 'https://apitest.nakala.fr/datas/uploads' -H 'accept: application/json' -H 'X-API-KEY: "+ self.annex.getconfig('key') +"' -H 'Content-Type: multipart/form-data' -F 'file=@"+ filename +"'")
        # fetching the file id from the returned message (it's in the form {"sha1":"x"})
        # we want it to be in this form to be able to send it in the post query when we add the file to the data 
        file_info = '{' + output.split(',')[-1]
        
        # adding the file to the data 
        url = "https://apitest.nakala.fr/datas/%s/files" % self.annex.getconfig('data_id')
        # sending a request to the API to add the file
        status, output = subprocess.getoutput('curl -X POST '+ url + ' -H "accept: application/json" -H "X-API-KEY: '+ str(self.annex.getconfig('key')) +'" -H "Content-Type: application/json" -d "'+ file_info + '"')
        
        # getting the returned message to see if the request has been done successfully
        returned_code= output.split(',')[0].split(':')[-1]

        if returned_code != '200':
            self.annex.debug("[error]: failed to send a post query in transfer_store. Returned code: " + str(returned_code))
            raise RemoteError('could not send a post query to the API in transfer_store.')


    # get the file identified by `key` and store it to `filename`
    # raise RemoteError if the file couldn't be retrieved    
    def transfer_retrieve(self, key, filename):
        # we need to send a GET query to /datas/data_id/file_id
        # ex: curl -X GET "https://apitest.nakala.fr/data/10.34847%2Fnkl.bedef1t9/8ba504b7ee513e519f0c3009bf0ed5b41a5e5462" -H "accept: application/json" -H "X-API-KEY: 01234567-89ab-cdef-0123-456789abcdef"
        # we can download it easily with --output file
        # success code = 200
        import requests
        try:
            # setting the url and the headers
            url = "https://apitest.nakala.fr/datas/%s" % self.annex.getconfig('data_id')
            headers = {"accept": "application/json", "X-API-KEY": self.annex.getconfig('key')}
            # sending a get request to the API to get the list of files in this data
            r = requests.get(url, headers=headers)
            
            # seeing if there is a problem with the return msg
            if r.status_code > 200:
                self.annex.debug("[error]: failed to send a get query in transfer_retrieve. Returned code: " + str(r.status_code))
                raise RemoteError('could not send a get query to the API in transfer_retrieve.')

            file_list = r.json()
            # looking in the list of files if the file exists
            for i in range(len(file_list)):
                if file_list[i]['name'] == key:
                    # getting the id of the file that we want to download
                    file_id =  file_list[i]['sha1']
                    # sending a get query to the api to download the file
                    url = url + '/%s' % file_id
                    q = requests.get(url, headers=headers)
                    # checking the returned code to see if there is an error
                    if q.status_code > 200:
                        self.annex.debug("[error]: couldn't retrieve the file from the remote. Returned code: " + str(q.status_code))
                        raise RemoteError('could not send a get query to the API in transfer_retrieve.')
                    # downloading the file
                    f = open(filename, "wb")
                    for chunk in q.iter_content(chunk_size=120): 
                        f.write(chunk)
                    # once we finish writing into the file we can close it
                    f.close()
            
        except Exception as error:
            raise RemoteError(error)
        pass

    # return True if the key is present in the remote
    # return False if the key is not present
    # raise RemoteError if the presence of the key couldn't be determined, eg. in case of connection error        
    def checkpresent(self, key):
        # request GET to /datas/data_id/files to get the list of files
        # or just note this when executing prepare so as to not redo it
        # then, compare the key to the files to see if it's there
        # ex: curl -X GET "https://apitest.nakala.fr/datas/10.34847%2Fnkl.bedef1t9/files" -H "accept: application/json" -H "X-API-KEY: 01234567-89ab-cdef-0123-456789abcdef"
        # success code = 200
        import requests
        try:
            # setting the url and the headers
            url = "https://apitest.nakala.fr/datas/%s/files" % self.annex.getcnnfig('data_id')
            headers = {"accept": "application/json", "X-API-KEY": self.annex.getconfig('key')}
            # sending a get request to the API to get the list of files in this data
            r = requests.get(url, headers=headers)
            
            # seeing if there is a problem with the return msg
            if r.status_code > 200:
                self.annex.debug("[error]: failed to send a get query in checkpresent. Returned code: " + str(r.status_code))
                raise RemoteError('could not send a get query to the API in checkpresent.')

            file_list = r.json()
            # looking in the list of files if the file exists
            for i in range(len(file_list)):
                if file_list[i]['name'] == key:
                    return True
            return False
        except Exception as error:
            raise RemoteError(error)
    
    # remove the key from the remote
    # raise RemoteError if it couldn't be removed
    # note that removing a not existing key isn't considered an error
    def remove(self, key):
        # query DELETE to /datas/data_id/files/file_id 
        # we need the id of the file and so either keep it in a dictionary 
        # or do a request to get the list (like in checkpresent)
        # success_code = 200
        # take care of the case of when there is only one file left in the remote and we want to delete it
        # it can't be done !
        import requests
        try:
            # setting the url and the headers
            url = "https://apitest.nakala.fr/datas/%s/files" % self.annex.getconfig('data_id')
            headers = {"accept": "application/json", "X-API-KEY": self.annex.getconfig('key')}
            # sending a get request to the API to get the list of files in this data
            r = requests.get(url, headers=headers)
            
            # seeing if there is a problem with the return msg
            if r.status_code > 200:
                self.annex.debug("[error]: failed to send a get query in checkpresent. Returned code: " + str(r.status_code))
                raise RemoteError('could not send a get query to the API in checkpresent.')

            file_list = r.json()
            # looking in the list of files if the file exists
            for i in range(len(file_list)):
                if file_list[i]['name'] == key:
                    file_id =  file_list[i]['sha1']
                    url = url + '/%s' % file_id
                    q = requests.delete(url, headers=headers)
                    if q.status_code > 200:
                        self.annex.debug("[error]: couldn't delete the file from the remote. Returned code: " + str(q.status_code))
                        raise RemoteError('could not send a delete query to the API in remove.')
                    break;
        except Exception as error:
            raise RemoteError(error)
        pass

    # store the file located at `local_file` to `remote_file` on the remote
    # raise RemoteError if the file couldn't be stored
    def transferexport_store(self, key, local_file, remote_file):
        self.transfer_store(key, local_file)

    # get the file located at `remote_file` from the remote and store it to `local_file`
    # raise RemoteError if the file couldn't be retrieved
    def transferexport_retrieve(self, key, local_file, remote_file):
        self.transfer_retrieve(key, local_file)

    # return True if the file `remote_file` is present in the remote
    # return False if not
    # raise RemoteError if the presence of the file couldn't be determined, eg. in case of connection error
    def checkpresentexport(self, key, remote_file):
        self.checkpresent(key)

    # remove the file in `remote_file` from the remote
    # raise RemoteError if it couldn't be removed
    # note that removing a not existing key isn't considered an error
    def removeexport(self, key, remote_file):
        self.remove(key)

    # remove the directory `remote_directory` from the remote
    # raise RemoteError if it couldn't be removed
    # note that removing a not existing directory isn't considered an error
    def removeexportdirectory(self, remote_directory):
        # DELETE to /datas/data_id: deletes the whole data
        # there are no directories in nakala and so this won't be needed
        pass

    # move the remote file in `name` to `new_name`
    # raise RemoteError if it couldn't be moved
    def renameexport(self, key, filename, new_filename):
        # PUT /datas/data_id if needed
        # not needed, we won't be changing the names of the files in the remote (will be kept as the git-annex keys)
        pass
    
    def print_info(self, message):
        try:
            self.annex.info(message)
        except ProtocolError:
            print(message)
                    
            
def main():
    # Redirect output to stderr to avoid messing up the protocol
    output = sys.stdout
    sys.stdout = sys.stderr
    
    master = Master(output)
    remote = NakalaRemote(master)
    master.LinkRemote(remote)
    master.Listen()

if __name__ == "__main__":
    main()        


