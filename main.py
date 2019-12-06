from flask import Flask, request, jsonify
import boto3
import json

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
    user_events = request.get_json()
    
    #Correct Json Format Verification
    if list(user_events.keys())==['userId', 'events']:
        
        #creates a string with the json format of the request
        user_events_json=json.dumps(user_events)
        
        #Sends the string to firehose Delivery Stream projectx-track which will write periodically on amazon S3 on the preffix track
        response = client_firehose.put_record(DeliveryStreamName='projectx-track',Record={'Data': user_events_json})  
        return(str(response['ResponseMetadata']['HTTPStatusCode']))
    return('Error: Wrong Json Format/fiels')
    




###### /alias #####

@app.route('/alias',methods = ['POST'])
def alias():
    alias_user = request.get_json()
    confirmation='false'
    
    #Correct Json Format Verification
    if list(alias_user.keys())==  ["newUserId","originalUserId","timestampUTC"]:
        
        #creates a string with the json format of the request
        alias_user_json=json.dumps(alias_user)
        
        #Sends the string to firehose Delivery Stream projectx-alias which will write periodically on amazon S3 on the preffix alias
        response = client_firehose.put_record(DeliveryStreamName='projectx-alias',Record={'Data': alias_user_json})
        return(str(response['ResponseMetadata']['HTTPStatusCode']))
    return('Error: Wrong Json Format/fiels')




###### /profile #####

@app.route('/profile',methods = ['POST'])
def profile():    
    user_profile = request.get_json()
    confirmation='false'
    
    #Correct Json Format Verification
    if list(user_profile.keys())==  ["userId","attributes","timestampUTC"]:
        
        #creates a string with the json format of the request
        alias_user_json=json.dumps(alias_user)
        
        #Sends the string to firehose Delivery Stream projectx-profile which will write periodically on amazon S3 on the preffix profile
        response= client_firehose.put_record(DeliveryStreamName='projectx-profile',Record={'Data': alias_user_json})
        return(str(response['ResponseMetadata']['HTTPStatusCode']))
    return('Error: Wrong Json Format/fiels')




if __name__ == "__main__":
    app.run(host='0.0.0.0',port=80)
