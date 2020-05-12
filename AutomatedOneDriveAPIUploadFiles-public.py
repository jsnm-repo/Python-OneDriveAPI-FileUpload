import os
import requests
import json
import msal

#Configuration
CLIENT_ID = 'xxxxxxxx-xxxxxxx-xxxxxx-xxxxxxx-xxxxxxxxxx'
TENANT_ID = 'xxxxxxxx-xxxxxxx-xxxxxx-xxxxxxx-xxxxxxxxxx'
AUTHORITY_URL = 'https://login.microsoftonline.com/{}'.format(TENANT_ID)
RESOURCE_URL = 'https://graph.microsoft.com/'
API_VERSION = 'v1.0'
USERNAME = 'xxxxxxxxx@xxxxxx.xxx' #Office365 user's account username
PASSWORD = 'xxxxxxxxxxxxxxx'
SCOPES = ['Sites.ReadWrite.All','Files.ReadWrite.All'] # Add other scopes/permissions as needed.

#Creating a public client app, Aquire a access token for the user and set the header for API calls
cognos_to_onedrive = msal.PublicClientApplication(CLIENT_ID, authority=AUTHORITY_URL)
token = cognos_to_onedrive.acquire_token_by_username_password(USERNAME,PASSWORD,SCOPES)
headers = {'Authorization': 'Bearer {}'.format(token['access_token'])}
onedrive_destination = '{}/{}/me/drive/root:/cognos'.format(RESOURCE_URL,API_VERSION)
cognos_reports_source = r"C:\Users\jsnmtr\Desktop\filesToUpload"

#Looping through the files inside the source directory
for root, dirs, files in os.walk(cognos_reports_source):
    for file_name in files:
        file_path = os.path.join(root,file_name)
        file_size = os.stat(file_path).st_size
        file_data = open(file_path, 'rb')
    
        if file_size < 4100000: 
            #Perform is simple upload to the API
            r = requests.put(onedrive_destination+"/"+file_name+":/content", data=file_data, headers=headers)
        else:
            #Creating an upload session
            upload_session = requests.post(onedrive_destination+"/"+file_name+":/createUploadSession", headers=headers).json()
            
            with open(file_path, 'rb') as f:
                total_file_size = os.path.getsize(file_path)
                chunk_size = 327680
                chunk_number = total_file_size//chunk_size
                chunk_leftover = total_file_size - chunk_size * chunk_number
                i = 0
                while True:
                    chunk_data = f.read(chunk_size)
                    start_index = i*chunk_size
                    end_index = start_index + chunk_size
                    #If end of file, break
                    if not chunk_data:
                        break
                    if i == chunk_number:
                        end_index = start_index + chunk_leftover
                    #Setting the header with the appropriate chunk data location in the file
                    headers = {'Content-Length':'{}'.format(chunk_size),'Content-Range':'bytes {}-{}/{}'.format(start_index, end_index-1, total_file_size)}
                    #Upload one chunk at a time
                    chunk_data_upload = requests.put(upload_session['uploadUrl'], data=chunk_data, headers=headers)
                    print(chunk_data_upload)
                    print(chunk_data_upload.json())
                    i = i + 1
                    
        file_data.close()