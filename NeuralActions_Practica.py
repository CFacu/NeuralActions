import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials
import requests

#Connecting to the Google SpreadSheet
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)

gss_client = gspread.authorize(credentials)
gss = gss_client.open('NeuralActions Practicas')
sheet = gss.sheet1

#Connecting to NeuralActions
#Login
url = "https://demo.neuralactions.com.ar/api/v1/login"
payload = "email=c.facu98@gmail.com&password=asd123asd123"
headers = {
  'Content-Type': 'application/x-www-form-urlencoded',
  'X-Requested-With': 'XMLHttpRequest'
}

response_login = requests.request("POST", url, headers=headers, data = payload)

#Getting Workspace
url = "https://demo.neuralactions.com.ar/api/v1/workspaces/"

payload = {}
headers = {
  'Content-Type': 'application/json',
  'Authorization': 'Bearer ' + response_login.json()['access_token']
}

response_workspace = requests.request("GET", url, headers=headers, data = payload)

#Searching fo all the network

url = "https://demo.neuralactions.com.ar/api/v1/network"

headers = {
  'Content-Type': 'application/json',
  'Authorization': 'Bearer ' + response_login.json()['access_token']
}

payload = {
    "raw_search_string": "+",
    "page": 1,
    "workspaces": {
        "active_workspace_id": response_workspace.json()['active_workspace_id']
    }
}

response_network = requests.request("POST", url, headers=headers, json = payload)

#Getting all nodes

json_nodes = response_network.json()
nodes = json_nodes['nodes']
print (nodes)
#Writing the nodes into the SpreadSheet
i = 1
for node in nodes:
	sheet.update_cell(i, 1, node.get('node_name'))
	i = i + 1