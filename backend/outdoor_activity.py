import requests

url = "https://api.ambeedata.com/latest/by-city"
querystring = {"city": "Chicago"}
headers = {
    'x-api-key': "146edc53220d165dedd33a57f16abc09d1d214c98bd93eb1cd64e4e9b172d6a0",
    'Content-type': "application/json"
}
response = requests.request("GET", url, headers=headers, params=querystring)
print(response.text)
