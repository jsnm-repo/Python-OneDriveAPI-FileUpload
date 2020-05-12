import requests
import json
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import MobileApplicationClient

client_id = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx"
scopes = ['Sites.ReadWrite.All','Files.ReadWrite.All']
auth_url = 'https://login.microsoftonline.com/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx/oauth2/v2.0/authorize'

#OAuth2Session is an extension to requests.Session
#used to create an authorization url using the requests.Session interface
#MobileApplicationClient is used to get the Implicit Grant
oauth = OAuth2Session(client=MobileApplicationClient(client_id=client_id), scope=scopes)
authorization_url, state = oauth.authorization_url(auth_url)

consent_link = oauth.get(authorization_url)
print(consent_link.url)


