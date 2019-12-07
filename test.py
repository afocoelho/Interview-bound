import requests
import time
import json
httpaddress = 'http://18.219.203.248/'
'''
This is the test script
This Script is divided into 3 parts each one testing all the 3 actions for a specific scenario:
  1.Scenario - Testing the actions with the desired records - the requests sent are all with the desired format so everything sould run smooth 
  2.Scenario - Testing the actions responses with jsons but with wrong field names - 400 bad request response is expected with the message "Error: Wrong Json Fiels"
  3.Scenario - Testing the actions responses with data that is not in json format - 400 bad request response is expected with the error message "request data was understood as *type* Instead of Json"
'''



############ 1.Scenario ################


print('1.Scenario - Testing the actions with the desired records - 200 response is expected')

## Test /track
httpaddresstrack  = httpaddress + 'track'
user_events = {"userId": "fakeid01","events": [{"eventName": "test","metadata": {"test":1},"timestampUTC": 0}]}
response = requests.post(httpaddresstrack, json=user_events)
if response.status_code == 200:
    print(response)
    print(response.text)
else:
    print(response)
    print('/track is not processing the pretend json format')
    
## Test /alias
httpaddressalias  = httpaddress + 'alias'
originalUserId = 'user01'
new_used_Id  = 'nuser01'
alias_user=  {  "newUserId": new_used_Id,"originalUserId": originalUserId,"timestampUTC": time.time()}
response = requests.post(httpaddressalias, json=alias_user)
if response.status_code == 200:
    print(response)
    print(response.text)
else:
    print(response)
    print('/alias is not processing the pretend json format')

## Test /profile
httpaddressprofile  = httpaddress + 'profile'
user_profile= {   "userId": "string",  "attributes": {},  "timestampUTC": 0 }
response = requests.post(httpaddressprofile, json=user_profile)
if response.status_code == 200:
    print(response)
    print(response.text)
else:
    print(response)
    print('/track is not processing the pretend json format')

    

    
############ 2.Scenario ################


print('2.Scenario - Testing the actions responses with jsons but with wrong field names - 400 bad request response is expected ')

## Test /track
httpaddresstrack  = httpaddress + 'track'
user_events = {"userId123": "fakeid01","events": [{"eventName": "test","metadata": {"test":1},"timestampUTC": 0}]}
response = requests.post(httpaddresstrack, json=user_events)
print(response)
print(response.content)
    
## Test /alias
httpaddressalias  = httpaddress + 'alias'
originalUserId = 'user01'
new_used_Id  = 'nuser01'
alias_user=  {  "newUserId131": new_used_Id,"originalUserId": originalUserId,"timestampUTC": time.time()}
response = requests.post(httpaddressalias, json=alias_user)
print(response)
print(response.content)

## Test /profile
httpaddressprofile  = httpaddress + 'profile'
user_profile= {   "userId131": "string",  "attributes": {},  "timestampUTC": 0 }
response = requests.post(httpaddressprofile, json=user_profile)
print(response)
print(response.content)




############ 3.Scenario ################


print('3.Scenario - Testing the actions responses with data that is not in json format - 400 bad request response is expected')

httpaddresstrack  = httpaddress + 'track'
user_events = "aifbaw egiqedfjvcpal"
response = requests.post(httpaddresstrack, json=user_events)
print(response)
print(response.content)
    
## Test /alias
httpaddressalias  = httpaddress + 'alias'
originalUserId = 'user01'
new_used_Id  = 'nuser01'
alias_user=  "aifbaw egiqedfjvcpal"
response = requests.post(httpaddressalias, json=alias_user)
print(response)
print(response.content)

## Test /profile
httpaddressprofile  = httpaddress + 'profile'
user_profile="aifbaw egiqedfjvcpal"
response = requests.post(httpaddressprofile, json=user_profile)
print(response)
print(response.content)
