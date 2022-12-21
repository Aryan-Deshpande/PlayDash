# doesnt have central storage for session, each route has its own checking

from backend import app, r
from backend.midware import checkuser, createBooking, pageFunc, pageFuncs, checkbooking
from backend.midware import register as registering

from flask import request, jsonify, make_response, render_template, redirect

import secrets
import json

# Tested, it should register following user, and create session for that user
@app.route('/register',methods=['POST'])
def register():

    if request.method == 'POST':

        # registers the user and returns the userid if successful
        register_status = registering(request.form.get('username'),request.form.get('password'))
        print(register_status)

        # if the user is registered, then it creates a session for the user
        if register_status != None or register_status != False:
            
            # generates the sessionId for the user
            sessionId = secrets.token_hex(16)
            #print(sessionId + "session id")

            # creates a session for the user
            session_data = {'name': register_status}

            # serializes the session data
            session_serialize = json.dumps(session_data)

            # sets the session data to expire in 1 hour
            r.expire(sessionId, 3600)

            # sets the session data to the sessionId in the redis database
            r.set(sessionId, session_serialize)

            return jsonify({'result':True, 'sessionId':sessionId})
        else:
            return jsonify({'result':False})

# Tested, it should login a user and redirect to a url
@app.route('/login',methods=['POST'])
def login():

    if request.method == 'POST':
                                    
        # checks if the user exists and returns the userid if successful
        login_status = checkuser(request.form['username'],request.form['password'])
        print(login_status, "login status")

        # if the user exists, then it creates a session for the user
        if login_status !=False:

            # generates the sessionId for the user
            sessionId = secrets.token_hex(16)

            # creates a session for the user
            print(sessionId + "session id")

            # creates a session for the user
            session_data = {'name': login_status}

            # serializes the session data
            session_serialize = json.dumps(session_data)

            # sets the session data to expire in 1 hour
            r.expire(sessionId, 3600)

            # sets the session data to the sessionId in the redis database
            r.set(sessionId, session_serialize)

            return jsonify({'result':True, 'sessionId':sessionId})
        else:
            return jsonify({'result':False})

# Tested, should logout user / set user value in session to be None, then redirect user
@app.route('/logout',methods=['POST'])
def logout():

    if request.method == 'POST':
        
        # remove sessions from redis
        sessionId = request.headers.get('sessionId')
        r.delete(sessionId)

        return jsonify({'result':True})

# Tested, create a booking for a particular event
@app.route('/event/Booking',methods=['POST'])
def booking():

    if request.method == "POST":

        # retrieval of the session id from the header
        sessionId = request.headers.get('sessionId')

        # check if the session id is valid
        if not r.get(sessionId):
            return jsonify({'error':'Unauthorized'}), 400

        else:

            # retrieval of the value of the sessionId key
            session_data = r.get(sessionId)

            # deserialization of the session data
            session = json.loads(session_data)

            eventId, eventName, userId = request.json['eventId'], request.json['eventName'], session['name']

            # create booking, and return the status of the booking
            booking_status = createBooking(userId, eventId, eventName)
            #print(booking_status)

            if booking_status == True:
                return jsonify({'result':True})

            else:
                return jsonify({'result':False})

# Tested, list all the events available
@app.route('/events',methods=['GET'])
def events():

    # JSON object to be appended and returned to the URI call
    eventObject = [] 

    # Queries the postgres database with all the necessary details
    eventPages = pageFuncs()

    # Creates a new dict key with the following event details
    for i,event in enumerate(eventPages): 

        (eventId,eventName,eventDate) = event
        eventObject.append({'eventId':eventId,'eventName':eventName,'eventDate':eventDate})    
    
    #print({'events':f'{eventObject}'})
    return eventObject  

# Tested, specific event page info
@app.route('/event/<string:eventName>', methods=['GET'])
def eventPage(eventName):

    # get sessionId from the header of the response
    sessionId = request.headers.get('sessionId')

    # if the sessionId key does not exist in the Redis cache, then return error
    if not r.get(sessionId):
            return jsonify({'error':'Unauthorized'}), 400

    # if the sessionId key does exist in the redis cache
    else:

            # retrieval of the value of the sessionId key
            session_data = r.get(sessionId)

            # deserialization of the value
            session = json.loads(session_data)
    
            # retrieval of the event content based on url parameters
            event_content = pageFunc(eventName) 

            # if the event content is not None, then return the event content
            if event_content is not None:
                print(event_content , "event content")
                eventId,eventName,eventDate = event_content[0],event_content[1],event_content[2]

                # check if the user has already booked the event through postgreSQL querying
                # returns TRUE or FALSE bade on the query
                if checkbooking(session['name'],eventId) == True:
                    return jsonify({'eventId':eventId,'eventName':eventName,'eventDate':eventDate,'booked':True})
                else:
                    return jsonify({'eventId':eventId,'eventName':eventName,'eventDate':eventDate,'booked':False})

            # if no content for the event is returned, then return error
            else:
                return jsonify({'error':'event not found'}), 400

# Only for testing 
@app.route('/',methods=['GET'])
def test():
    return jsonify({'res':'this works right here'})

