from flask import Flask, request, jsonify,abort,make_response
import boto3
import json
'''
This python script should be executed in super user conditions to this execute the command: sudo python3 "folderpath"/main.py  
This scripts will create a http server with an Welcome message and 3 actions /track,/alias,/profile.

The intend of all the actions in this script are only to garantee that data gets stored

############################## /track ##############################

This action expects the data once the method that is defined is POST. The data expect by /track should be
something like this example:
{"userId": "fakeid01","events": [{"eventName": "test","metadata": {"test":1},"timestampUTC": 0}]}

Amazon Firehose Delivery Stream
If everything goes well it will put this record into the firehose delivery stream projectx-track which will write in file track
in amazon S3 after 300 seconds from the first put_record or after the amount of records reach to 5 MB.


############################## /alias ##############################

This action expects the data once the method that is defined is POST. The data expect by /alias should be
something like this example:
alias_user=  {  "newUserId": 'user02',"originalUserId": 'user01',"timestampUTC": 0}

Amazon Firehose Delivery Stream
If everything goes well it will put this record into the firehose delivery stream projectx-alias which will write in file alias
in amazon S3 after 300 seconds from the first put_record or after the amount of records reach to 5 MB.


############################# /profile #############################

This action expects the data once the method that is defined is POST. The data expect by /profile should be
something like this example:
user_profile= {   "userId": "string",  "attributes": {},  "timestampUTC": 0 }

Amazon Firehose Delivery Stream
If everything goes well it will put this record into the firehose delivery stream projectx-profile which will write in file profile
in amazon S3 after 300 seconds from the first put_record or after the amount of records reach to 5 MB.


'''

# Create a Flask applicatiob
app = Flask(__name__)

#Creates a client to interact with firhose
client_firehose = boto3.client('firehose',region_name='us-east-2')


#Welcome Message
@app.route('/')
def begin():
    return ("Welcome, This API as 3 actions track,alias,profile")



####### /track  #####

@app.route('/track',methods = ['POST'])
def track():
    
    ## Verify Json Format and fields
    if request.is_json:
        user_events = request.get_json()

        if type(user_events) ==dict:
            
            #Correct Json Fields Verification
            if list(user_events.keys())==['userId', 'events'] and type(user_events['events']) ==list:
                
                #creates a string with the json format of the request
                user_events_json=json.dumps(user_events)

                #Sends the string to firehose Delivery Stream projectx-track which will write periodically on amazon S3 on the preffix track
                response = client_firehose.put_record(DeliveryStreamName='projectx-track',Record={'Data': user_events_json})  
            
                res_fields = {"Description":'OK'}
                resp=make_response(json.dumps(res_fields),response['ResponseMetadata']['HTTPStatusCode'])
                return resp
            
            else:
                abort(400,'Wrong Json Fiels')
        else:
            abort(400,'request data was understood as '+str(type(user_events))+ ' Instead of Json')
    else:
        abort(400,'API was not able to recognize JSON format')


###### /alias #####

@app.route('/alias',methods = ['POST'])
def alias():
    

    ## Verify Json Format and fields
    if request.is_json:
        alias_user = request.get_json()

        if type(alias_user) ==dict:
            
    
            #Correct Json Fields Verification
            if list(alias_user.keys())==  ["newUserId","originalUserId","timestampUTC"]:

                #creates a string with the json format of the request
                alias_user_json=json.dumps(alias_user)

                #Sends the string to firehose Delivery Stream projectx-alias which will write periodically on amazon S3 on the preffix alias
                response = client_firehose.put_record(DeliveryStreamName='projectx-alias',Record={'Data': alias_user_json})
                res_fields = {"Description":'OK'}
                resp=make_response(json.dumps(res_fields),response['ResponseMetadata']['HTTPStatusCode'])
                return resp
            
            else:
                abort(400,'Error: Wrong Json Fiels')
        else:
            abort(400,'request data was understood as '+str(type(alias_user)) + ' Instead of Json')
    else:
        abort(400,'API was not able to recognize JSON format')


###### /profile #####

@app.route('/profile',methods = ['POST'])
def profile():    

    
    ## Verify Json Format and fields
    if request.is_json:
        user_profile = request.get_json()
        
        if type(user_profile) ==dict:
            
            #Correct Json Fields Verification
            if list(user_profile.keys())==  ["userId","attributes","timestampUTC"]:

                #creates a string with the json format of the request
                user_profile_json=json.dumps(user_profile)

                #Sends the string to firehose Delivery Stream projectx-profile which will write periodically on amazon S3 on the preffix profile
                response= client_firehose.put_record(DeliveryStreamName='projectx-profile',Record={'Data': user_profile_json})
                
                res_fields = {"Description":'OK'}
                resp=make_response(json.dumps(res_fields),response['ResponseMetadata']['HTTPStatusCode'])
                return resp
            else:
                abort(400,'Error: Wrong Json Fiels')
        else:
            abort(400,'request data was understood as '+ str(type(user_profile)) + ' Instead of Json')
    else:
        abort(400,'API was not able to recognize JSON format')



if __name__ == "__main__":
    app.run(host='0.0.0.0',port=80)
